from sys import argv
import json
if __name__ == "__main__":
  function_content = None
  dependencies = None
  service_name = None
  target_function = None
  for i, arg in enumerate(argv):
    if "--" not in arg:
      continue
    if arg == "--from-file":
      with open(argv[i+1], "r") as f:
        function_content = f.read()

    elif arg == "--dependencies":
      with open(argv[i+1], "r") as f:
        dependencies = f.read()
    elif arg == "--name":
      service_name = argv[i+1]
    elif arg == "--target":
      target_function = argv[i+1]
    else:
      raise Exception(f"Invalid argument {arg}")
  if any(x for x in (function_content, dependencies, service_name, target_function) if x is None):
    raise Exception("Missing argument")

  with open("output.json", "w+") as f:
    f.write(json.dumps({
      "name" : service_name,
      "func_name": target_function,
      "content": function_content,
      "dependencies": dependencies
    }))