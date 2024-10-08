# k8s-logs-exporter
Stream logs from pods selected namespaces on a k8s cluster via web sockets


Before you start:

Identify the namespaces that you need logs from.

Add the namespaces where your target pods are running to config map.

Add a Service account, Cluster role and Rolebinding for each namespace.

Use the yamls in k8s-yaml directory to deploy your service.
