import os
import sys
import json
import time
from io import StringIO
from kafka import KafkaConsumer

KAFKA_ADVERTISED_HOST_NAME = os.environ["KAFKA_ADVERTISED_HOST_NAME"]
KAFKA_ADVERTISED_PORT= os.environ["KAFKA_ADVERTISED_PORT"]

DEFAULT_LOG_DEST = f"./logs/{os.environ['HOSTNAME'].split('-')[0]}.json"
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

CONFIG = {}
with open("data/config.json", "r") as f:
  CONFIG = json.loads(f.read())

LOGGER = Logger()


if __name__ == "__main__":
  # install dependencies if there are any
  if "dependencies" in CONFIG: 
      os.system(f"echo {CONFIG['dependencies']} > dependencies.txt")
      os.system("pip install -r dependencies.txt")
  function_content = CONFIG["content"]
  target_function = CONFIG["target_function"]
  service_name = CONFIG["name"]

  try:
    exec(function_content) # inject function content to the runtime environment
  except Exception as e:
    LOGGER.log(self, "", repr(e))
    LOGGER.write()
    raise e

  #Kafka Comsumer
  consumer = KafkaConsumer(service_name, bootstrap_servers=f"{KAFKA_ADVERTISED_HOST_NAME}:{KAFKA_ADVERTISED_PORT}")
  for msg in consumer:
    # get function arguments from Kafka topic
    old_stdout, old_stderr  = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = StringIO(),  StringIO()
    # inject the code into function runtime environment
    try:
      exec(f"{target_function}({msg})")
      LOGGER.log(sys.stdout.getvalue(),  sys.stderr.getvalue())
    except Exception as e:
      LOGGER.log(sys.stdout.getvalue(), repr(e))

    LOGGER.write()
    sys.stdout, sys.stderr = old_stdout, old_stderr
      