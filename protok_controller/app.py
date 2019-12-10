from flask import Flask, request, jsonify
import json
import requests
from payload import ServerlessDeploymentPayload
app = Flask(__name__)

# template payload
new_custom_object_payload = {
    "apiVersion": "stable.protok.com/v1",
    "kind": "ServerlessFunction",
    "metadata": {
        "name": None
    },
    "spec": {
        "dependencies": "",
        "content": "",
        "target_function": ""

    }
}

new_deployment_payload = {
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": "foo",
    "labels": {
      "app": "foo"
    }
  },
  "spec": {
    "replicas": 1,
    "selector": {
      "matchLabels": {
        "app": "foo"
      }
    },
    "template": {
      "metadata": {
        "labels": {
          "app": "foo"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "foo",
            "image": "davidvu98/protok_serverless:latest",
            "command": [
              "sleep",
              "3000"
            ],
            "env": [
              {
                "name": "SERVERLESS_CONFIG",
                "value": ""
              }
            ]
          }
        ]
      }
    }
  }
}

@app.route('/create', methods=['POST'])
def create_rest():
  try:
    data = request.get_json()
    custom_object_payload = dict(new_custom_object_payload)
    custom_object_payload["metadata"]["name"] = data["name"]
    custom_object_payload["spec"]["content"] = data["content"]
    custom_object_payload["spec"]["dependencies"] =  data["dependencies"]
    custom_object_payload["spec"]["target_function"] = data["target_function"]
    resp_custom_object = requests.post("http://127.0.0.1:8080/apis/stable.protok.com/v1/namespaces/default/serverlessfunctions", 
                       data=json.dumps(custom_object_payload), 
                      headers={"Content-Type": "application/json"}).json()
    return jsonify({"/apis/stable.protok.com/v1/namespaces/default/serverlessfunctions": resp_custom_object})
  except Exception as e:
    return jsonify({'success': False, 'error': str(e)})

@app.route('/deploy', methods=['GET'])
def deploy():
  try:
    data = request.args
    print(data)
    service_to_deploy = data["name"]
    deployment_payload = ServerlessDeploymentPayload(service_to_deploy).generate_payload()
    resp_new_deployment = requests.post("http://127.0.0.1:8080/apis/apps/v1/namespaces/default/deployments", 
                       data=json.dumps(deployment_payload), 
                      headers={"Content-Type": "application/json"}).json()
    return jsonify({"/apis/apps/v1/namespaces/default/deployments": resp_new_deployment})
  except Exception as e:
    return jsonify({ 'success': False, 'error': str(e)})



if __name__ == "__main__":
  app.run()