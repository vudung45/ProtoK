kubectl delete serverlessfunctions $1
kubectl delete services $1
kubectl delete deployments $1
kubectl get pods