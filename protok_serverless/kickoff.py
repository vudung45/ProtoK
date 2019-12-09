import subprocess
import os

if __name__ == "__main__":
  #get env info
  if 'DEPENDENCIES' in os.environ:
    dependencies: str = os.environ['DEPENDENCIES']
    with open("dependencies.txt", "w+") as f:
      f.write(dependencies)
      out = subprocess.Popen(['pip', 'install', '-r', "dependencies.txt"])
      stdout, stderr = out.communicate()
      print(stdout, stderr)

  if 'FUNCTION_CONTENT' in os.environ:
    dependencies: str = os.environ['FUNCTION_CONTENT']
    exec(dependencies)
  #print(stdout.decode("utf-8"))