# K8s Logs Streamer
Stream logs from pods in selected namespaces on a k8s cluster via web socket


Before you start:

Identify the namespaces that you need logs from.

Add the namespaces where your target pods are running to config map.

Add a Service account, Cluster role and Rolebinding for each namespace.

Use the yamls in k8s-yaml directory to deploy your service.
