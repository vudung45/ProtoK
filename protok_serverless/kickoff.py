import subprocess
import os
import json

if __name__ == "__main__":
  with open("data/config.json", "r") as f:
    config = json.loads(f.read())
    if "content" in config:
      function_content = config["content"]
      target_function = config.get("target_function")
      exec(f"{function_content}\n{target_function}()")
