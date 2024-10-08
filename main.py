from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from kubernetes import client, config, watch
from fastapi.templating import Jinja2Templates
import os
from typing import List
import asyncio
import threading

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load Kubernetes configuration
config.load_incluster_config()

# Create Kubernetes API client
kube_client = client.CoreV1Api()

# Read allowed namespaces from environment variable (set via ConfigMap)
ALLOWED_NAMESPACES = os.getenv("ALLOWED_NAMESPACES", "").split(",")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    namespaces = ALLOWED_NAMESPACES
    return templates.TemplateResponse("index.html", {"request": request, "namespaces": namespaces})

@app.get("/pods", response_model=List[str])
async def get_pods(namespace: str):
    pods = kube_client.list_namespaced_pod(namespace=namespace)
    pod_names = [pod.metadata.name for pod in pods.items]
    return pod_names

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Receive initial data with namespace and pod
        data = await websocket.receive_json()
        namespace = data.get("namespace")
        pod = data.get("pod")
        if not namespace or not pod:
            await websocket.send_text("Namespace and pod are required.")
            await websocket.close()
            return

        # Get the current event loop from the main thread
        loop = asyncio.get_event_loop()

        # Function to stream logs
        def stream_logs():
            w = watch.Watch()
            try:
                for log_line in w.stream(
                    kube_client.read_namespaced_pod_log,
                    name=pod,
                    namespace=namespace,
                    tail_lines=250,
                    follow=True
                ):
                    line = log_line.rstrip('\n')
                    # Schedule the coroutine to send the log line
                    asyncio.run_coroutine_threadsafe(websocket.send_text(line), loop)
            except Exception as e:
                # Schedule the coroutine to send the error message
                asyncio.run_coroutine_threadsafe(
                    websocket.send_text(f"Error fetching logs: {e}"), loop
                )
                asyncio.run_coroutine_threadsafe(websocket.close(), loop)

        # Start streaming logs in a new thread
        log_thread = threading.Thread(target=stream_logs)
        log_thread.start()

        # Keep the connection open
        while True:
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_text(f"Error: {e}")
        await websocket.close()
