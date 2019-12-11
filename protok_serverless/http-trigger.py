from flask import Flask, request, jsonify
import json
import requests
import time
import os
import sys
from io import StringIO

DEFAULT_LOG_DEST = f"./logs/{os.environ['HOSTNAME'].split('-')[0]}.json"
class Logger:
  log_dest = DEFAULT_LOG_DEST
  log_data = {}

  def __init__(self, log_dest = DEFAULT_LOG_DEST):
    self.log_dest = DEFAULT_LOG_DEST

  def log(self, stdout, stderr):
    self.log_data[int(time.time())] = {"stdout": stdout, "stderr": stderr}

  def write(self):
    with open(self.log_dest, "w+") as f:
      f.write(json.dumps(self.log_data))


app = Flask(__name__)
LOGGER = Logger()

CONFIG = {}
with open("data/config.json", "r") as f:
  CONFIG = json.loads(f.read())

LOGGER = Logger()


@app.route('/', methods=['POST'])
def main():
  function_args = dict(request.get_json())
  old_stdout, old_stderr  = sys.stdout, sys.stderr
  sys.stdout, sys.stderr = StringIO(),  StringIO()
  try:
    exec(f"{target_function}(**function_args)")
    LOGGER.log(sys.stdout.getvalue(),  sys.stderr.getvalue())
    output_json = jsonify({"stdout": sys.stdout.getvalue(), "stderr": sys.stderr.getvalue()})
  except Exception as e:
    LOGGER.log(sys.stdout.getvalue(), repr(e))
    output_json = jsonify({"stdout": sys.stdout.getvalue(), "stderr": repr(e)})

  LOGGER.write()
  sys.stdout, sys.stderr = old_stdout, old_stderr
    
  return output_json
 


if __name__ == "__main__":
  # install dependencies if there are any
  if "dependencies" in CONFIG: 
      os.system(f"echo {CONFIG['dependencies']} > dependencies.txt")
      os.system("pip install -r dependencies.txt")
  function_content = CONFIG["content"]
  target_function = CONFIG["target_function"]

  try:
    exec(function_content) # inject function content to the runtime environment
  except Exception as e:
    LOGGER.log(self, "", repr(e))
    LOGGER.write()

  app.run(host='0.0.0.0',port=8080)