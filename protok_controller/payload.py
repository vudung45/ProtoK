import requests
import json
with open("templates/http_trigger_deployment_template.json", "r") as f:
	new_deployment_payload = json.loads(f.read())

with open("templates/http_trigger_service_template.json", "r") as f:
	new_service_payload = json.loads(f.read())

class ServerlessDeploymentPayload:
	service_name = ""
	def __init__(self, service_name, type="http_trigger"):
		self.service_name = service_name
		self.type = type

	def generate_payload(self):
		deployment_payload = dict(new_deployment_payload)
		servlfunc_object = requests.get(f"http://127.0.0.1:8091/apis/stable.protok.com/v1/namespaces/default/serverlessfunctions/{self.service_name}").json()
		print(new_deployment_payload)
		deployment_payload["metadata"]["name"] = servlfunc_object["metadata"]["name"]
		deployment_payload["metadata"]["labels"]["app"] = servlfunc_object["metadata"]["name"]
		deployment_payload["spec"]["selector"]["matchLabels"]["app"] = servlfunc_object["metadata"]["name"]
		deployment_payload["spec"]["template"]["metadata"]["labels"]["app"] = servlfunc_object["metadata"]["name"]
		deployment_payload["spec"]["template"]["spec"]["initContainers"][0]["env"][0]["value"] = json.dumps(servlfunc_object["spec"])
		return deployment_payload

	def generate_payload_from_crd(self, servlfunc_object):
		deployment_payload = dict(new_deployment_payload)
		deployment_payload["metadata"]["name"] = servlfunc_object["metadata"]["name"]
		deployment_payload["metadata"]["labels"]["app"] = servlfunc_object["metadata"]["name"]
		deployment_payload["spec"]["selector"]["matchLabels"]["app"] = servlfunc_object["metadata"]["name"]
		deployment_payload["spec"]["template"]["metadata"]["labels"]["app"] = servlfunc_object["metadata"]["name"]
		deployment_payload["spec"]["template"]["spec"]["initContainers"][0]["env"][0]["value"] = json.dumps(servlfunc_object["spec"])
		return deployment_payload

class ServicePayload:
	service_name = ""
	def __init__(self, service_name):
		self.service_name = service_name

	def generate_payload(self):
		service_payload = dict(new_service_payload)
		service_payload["metadata"]["labels"]["app"], service_payload["metadata"]["name"], \
			service_payload["spec"]["selector"]["app"] = self.service_name, self.service_name, self.service_name
		return service_payload


