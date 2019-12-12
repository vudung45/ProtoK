"""
Custom Resource Controller
"""
import json
import yaml
from kubernetes import client, config, watch
import os
from payload import ServerlessDeploymentPayload,ServicePayload
import requests
DOMAIN = "stable.protok.com"


if __name__ == "__main__":
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
        definition = './CRD/protok.yaml'
    else:
        config.load_kube_config()
        definition = './CRD/protok.yaml'
    configuration = client.Configuration()
    configuration.assert_hostname = False
    api_client = client.api_client.ApiClient(configuration=configuration)
    crds = client.CustomObjectsApi(api_client)

    print("Listening to changes in /apis/stable.protok.com/v1/namespaces/default/serverlessfunctions")
    resource_version = ''
    while True:
        stream = watch.Watch().stream(crds.list_cluster_custom_object, DOMAIN, "v1", "serverlessfunctions", resource_version=resource_version)
        for event in stream:
          data = event["object"]
          service_to_deploy = data["metadata"]["name"]
          service_payload = ServicePayload(service_to_deploy).generate_payload()
          print(requests.post("http://127.0.0.1:8091/api/v1/namespaces/default/services", 
                       data=json.dumps(service_payload), 
                      headers={"Content-Type": "application/json"}).json())
          deployment_payload = ServerlessDeploymentPayload(service_to_deploy, type=data["spec"]["trigger_type"]).generate_payload_from_crd(data)
          print(requests.post("http://127.0.0.1:8091/apis/apps/v1/namespaces/default/deployments", 
                       data=json.dumps(deployment_payload), 
                      headers={"Content-Type": "application/json"}).json())
