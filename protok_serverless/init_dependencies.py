import subprocess
import os
import json


if __name__ == "__main__":
  with open("data/config.json", "r") as f:
    config = json.loads(f.read())
    if "dependencies" in config:
	    os.system(f"echo {config['dependencies']} > dependencies.txt")
	    os.system("pip install -r dependencies.txt")
	    