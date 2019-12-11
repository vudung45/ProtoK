import subprocess
import os
import sys
import json
import time
from io import StringIO
from kafka import KafkaConsumer

KAFKA_ADVERTISED_HOST_NAME = os.environ["KAFKA_ADVERTISED_HOST_NAME"]
KAFKA_ADVERTISED_PORT= os.environ["KAFKA_ADVERTISED_PORT"]

if __name__ == "__main__":
  config = {}
  with open("data/config.json", "r") as f:
    config = json.loads(f.read())

  #Kafka Comsumer
  service_name = config["name"]
  consumer = KafkaConsumer(service_name, bootstrap_servers=f"{KAFKA_ADVERTISED_HOST_NAME}:{KAFKA_ADVERTISED_PORT}")
  for msg in consumer:
    print(msg.value.decode('utf-8'))
    # get function arguments from Kafka topic
    function_args = dict(json.loads(msg.value.decode('utf-8')))
    if "content" in config:
      function_content = config["content"]
      target_function = config["func_name"]
      old_stdout, old_stderr  = sys.stdout, sys.stderr
      sys.stdout, sys.stderr = StringIO(),  StringIO()
      # inject the code into function runtime environment
      exec(f"{function_content}\n{target_function}(**function_args)")
      r_out, r_err = sys.stdout.getvalue(), sys.stderr.getvalue()
      log_data = {}
      try:
        with open(f"logs/{service_name}.json", "r") as f:
          log_data = json.loads(f.read())
      except Exception as e:
        pass
        
      log_data[int(time.time())] =  {
          "stdout" : r_out,
          "stderr" : r_err
      }
      with open(f"logs/{service_name}.json", "w+") as f:
        f.write(json.dumps(log_data))


