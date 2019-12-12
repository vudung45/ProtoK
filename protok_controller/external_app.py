"""
Expose internal Kubernetes ServerlessFunction APIs to external network
"""
from flask import Flask, request, jsonify
import json
import requests
from payload import ServerlessDeploymentPayload
from flask_cors import CORS, cross_origin
app = Flask(__name__)

# template payload
new_custom_object_payload = {
    "apiVersion": "stable.protok.com/v1",
    "kind": "ServerlessFunction",
    "metadata": {
        "name": None
    },
    "spec": {
        "name" : "",
        "dependencies": "",
        "content": "",
        "target_function": "",
        "kafka_server" : "",
        "trigger_type" : ""
    }
}


@app.route('/create', methods=['POST'])
@cross_origin()
def create_rest():
  try:
    data = request.get_json()
    custom_object_payload = dict(new_custom_object_payload)
    custom_object_payload["metadata"]["name"] = data["name"]
    custom_object_payload["spec"]["name"] = data["name"]
    custom_object_payload["spec"]["content"] = data["content"]
    custom_object_payload["spec"]["dependencies"] =  data.get("dependencies","")
    custom_object_payload["spec"]["target_function"] = data["func_name"]
    custom_object_payload["spec"]["kafka_server"] = data.get("kafka_server")
    custom_object_payload["spec"]["trigger_type"] = data.get("trigger_type", "http-trigger")

    resp_custom_object = requests.post("http://127.0.0.1:8091/apis/stable.protok.com/v1/namespaces/default/serverlessfunctions", 
                        data=json.dumps(custom_object_payload), 
                        headers={"Content-Type": "application/json"}).json()
    print(resp_custom_object)
    return jsonify({"/apis/stable.protok.com/v1/namespaces/default/serverlessfunctions": resp_custom_object}), 201
  except Exception as e:
    return jsonify({'success': False, 'error': str(e)}), 503


@app.route('/get_all', methods=['GET'])
@cross_origin()
def get_all():
  try:
    resp_get_all = requests.get("http://127.0.0.1:8091/apis/stable.protok.com/v1/namespaces/default/serverlessfunctions").json()
    return jsonify({"/apis/stable.protok.com/v1/namespaces/default/serverlessfunctions": resp_get_all}), 200
  except Exception as e:
    return jsonify({ 'success': False, 'error': str(e)}), 503

@app.route('/get_log', methods=['GET'])
def get_log():
  try:
    data = request.args
    service_to_get = data["name"]
    servlfunc_obj = requests.get(f"http://127.0.0.1:8091/apis/stable.protok.com/v1/namespaces/default/serverlessfunctions/{service_to_get}").json()
    if 'kind' in servlfunc_obj and servlfunc_obj['kind'] == 'ServerlessFunction':
      with open(f"function_logs/{service_to_get}.json", 'r') as f:
        return jsonify(json.loads(f.read()))
      return jsonify({})
    else:
      return jsonify({"success": False, "error": f"function name {service_to_get} does not exist"}), 503

  except Exception as e:
    return jsonify({ 'success': False, 'error': str(e)}), 503


if __name__ == "__main__":
  app.run(host='0.0.0.0')