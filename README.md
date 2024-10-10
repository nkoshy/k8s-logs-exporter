# K8s Logs Streamer

Stream logs from pods in selected namespaces on a Kubernetes cluster via WebSocket.

## Overview

K8s Logs Streamer is a tool designed to facilitate real-time log streaming from pods in specified namespaces within a Kubernetes cluster. This project leverages WebSocket technology to provide a seamless and efficient log streaming experience.

## Prerequisites

Before getting started, ensure you have the following:

- Access to a Kubernetes cluster
- `kubectl` configured to communicate with your cluster
- Necessary permissions to create and manage Kubernetes resources

## Setup

1. **Identify Target Namespaces**
   - Determine the namespaces containing the pods you want to stream logs from.

2. **Configure Namespaces**
   - Add the target namespaces to the ConfigMap in the `k8s-yaml/configmap.yaml` file.

3. **Set Up RBAC**
   For each namespace, you need to create:
   - A ServiceAccount
   - A ClusterRole
   - A RoleBinding
   
   Use the YAML files provided in the `k8s-yaml` directory as templates.

4. **Deploy the Service**
   - Apply the YAML files in the `k8s-yaml` directory to deploy your service:
     ```
     kubectl apply -f k8s-yaml/
     ```

## Usage

Once deployed, you can connect to the WebSocket endpoint to start streaming logs. The exact method of connection will depend on how you've exposed the service (e.g., through an Ingress or LoadBalancer).

## Configuration

Modify the ConfigMap in `k8s-yaml/configmap.yaml` to adjust settings such as:
- Target namespaces

## Troubleshooting

If you encounter issues:
1. Check that all RBAC resources are correctly applied.
2. Verify that the ServiceAccount has the necessary permissions in the target namespaces.
3. Examine the logs of the K8s Logs Streamer pod for any error messages.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

