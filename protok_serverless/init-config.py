import os

with open("data/config.json", "w+") as f:
  f.write(os.environ["SERVERLESS_CONFIG"])