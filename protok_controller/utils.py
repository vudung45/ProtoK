import os
import subprocess
from yaml_generator import YamlGenerator

class Deployment(object):
  deployment_name = ""
  dep_type = "NodePort"
  yaml_file = ""

  def __init__(self, deployment_name: str, yaml_file: str, dep_type: str ="NodePort") -> None:
    self.deployment_name = deployment_name
    self.dep_type = dep_type
    self.yaml_file = yaml_file

  def create(self) -> bool:
    out = subprocess.Popen(['kubectl', 'apply', '-f', self.yaml_file], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    print(stdout.decode("utf-8"))
    create = f"{self.deployment_name} created" in stdout.decode("utf-8")

  def expose(self):
    out = subprocess.Popen(['kubectl', 'expose', 'deployment', self.deployment_name, f"--type={self.dep_type}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    print(stdout.decode("utf-8"))
    exposed = f"{self.deployment_name} exposed" in stdout.decode("utf-8")

  def delete(self):
    out = subprocess.Popen(['kubectl', 'delete', 'deployment', self.deployment_name], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    print(stdout.decode("utf-8"))
    out = subprocess.Popen(['kubectl', 'delete', 'service', self.deployment_name], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    print(stdout.decode("utf-8"))
    deleted =  f"{self.deployment_name} deleted" in stdout.decode("utf-8")




class ServerlessFunction:
  environment_type = "python3.7"
  dependencies: str
  deployment: Deployment
  function_name: str
  function_content: str
  init_config = False
  deployed = False

  def __init__(self, function_name: str, function_content: str, dependencies: str, environment_type = "python3.7") -> None:
    self.function_name =function_name
    self.dependencies = dependencies
    self.environment_type = environment_type
    self.function_content = function_content
  

  def init_config(self, yaml_storage = "./yaml_storage", autogen_yaml = True, yaml_content = None) -> bool:
    if autogen_yaml:
      try:
        YamlGenerator.generate(self.function_name, self.dependencies, self.function_content, f"{yaml_storage}/{self.function_name}.yaml")
        self.init_config = True
      except Exception as e:
        # poorman error handling
        print(e)
        self.init_config = False
    else:
      try:
        YamlGenerator.generate(self.function_name, f"{yaml_storage}/{self.function_name}.yaml")
        self.init_config = True
        return True
      except Exception as e:
        # poorman error handlin
        print(e)
        self.init_config = False

    return self.init_config


  def init_deployment(self, yaml_storage = "./yaml_storage") -> None:
    # will have to first init config
    assert(self.init_config)
    self.deployment = Deployment(self.function_name, f"{yaml_storage}/{self.function_name}.yaml")
    print("Creating deployment...")
    self.deployment.create()
    print(f"Exposing {self.function_name} type NodePort..")
    self.deployment.expose()
    deployed = True

if __name__ == "__main__":
  test_function = ServerlessFunction("foo", "if __name__ == '__main__': print('Hello world')", "")
  test_function.init_config()
  test_function.init_deployment()
  test_function.deployment.delete() 







    

