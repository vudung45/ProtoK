import os
import sys
import json
import time
from io import StringIO
from kafka import KafkaConsumer


CONFIG = {}
with open("data/config.json", "r") as f:
  CONFIG = json.loads(f.read())
service_name = CONFIG['name']

DEFAULT_LOG_DEST = f"./logs/{service_name}.json"
class Logger:
  log_dest = DEFAULT_LOG_DEST
  log_data = {}

  def __init__(self, log_dest = DEFAULT_LOG_DEST):
    self.log_dest = log_dest

  def log(self, stdout, stderr):
    self.log_data[int(time.time())] = {"stdout": stdout, "stderr": stderr}

  def write(self):
    with open(self.log_dest, "w+") as f:
      f.write(json.dumps(self.log_data))

LOGGER = Logger()


if __name__ == "__main__":
  # install dependencies if there are any
  if "dependencies" in CONFIG: 
      os.system(f"echo {CONFIG['dependencies']} > dependencies.txt")
      os.system("pip install -r dependencies.txt")
  function_content = CONFIG["content"]
  target_function = CONFIG["target_function"]
  service_name = CONFIG["name"]
  kafka_server = CONFIG["kafka_server"]

  try:
    exec(function_content) # inject function content to the runtime environment
  except Exception as e:
    LOGGER.log(self, "", repr(e))
    LOGGER.write()
    raise e

  #Kafka Comsumer
  consumer = KafkaConsumer(service_name, bootstrap_servers=kafka_server)
  for msg in consumer:
    value = msg.value
    # get function arguments from Kafka topic
    old_stdout, old_stderr  = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = StringIO(),  StringIO()
    # inject the code into function runtime environment
    try:
      exec(f"{target_function}({value})")
      LOGGER.log(sys.stdout.getvalue(),  sys.stderr.getvalue())
    except Exception as e:
      LOGGER.log(sys.stdout.getvalue(), repr(e))

    LOGGER.write()
    sys.stdout, sys.stderr = old_stdout, old_stderr
      