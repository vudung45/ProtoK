
# setup ServerlessFunction custom resource
kubectl apply -f protok_controller/CRD/protok.yaml

# setup Kafka and zookeeper services
kubectl apply -f kafka/kafka-broker.yml
kubectl apply -f kafka/kafka-service.yml
kubectl apply -f kafka/zookeeper.yaml

