import os
import subprocess
from yaml_generator import YamlGenerator

class Deployment(object):
	deployment_name = ""
	dep_type = "NodePort"
	exposed = False
	yaml_file = ""
	created = False

	def __init__(self, deployment_name: str, yaml_file: str, dep_type: str ="NodePort") -> None:
		self.deployment_name = deployment_name
		self.dep_type = dep_type
		self.exposed = False
		self.yaml_file = yaml_file

	def create(self) -> bool:
		out = subprocess.Popen(['kubectl', 'apply', '-f', self.yaml_file], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
		stdout,stderr = out.communicate()
		print(stdout)
		create = f"service {self.deployment_name} created" in str(stdout)
		return create

	def expose(self):
		out = subprocess.Popen(['kubectl', 'expose', 'deployment', self.deployment_name, f"--type={dep_type}"], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
		stdout,stderr = out.communicate()
		exposed = f"service {self.deployment_name} exposed" in str(stdout)
		return exposed

	def delete(self):
		out = subprocess.Popen(['kubectl', 'delete', 'deployment', self.deployment_name], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
		stdout,stderr = out.communicate()
		deleted =  f"deployment {self.deployment_name} deleted" in str(stdout)
		return deleted




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
				YamlGenerator.generate(self.function_name, f"{self.function_name}.yaml")
				self.init_config = True
			except Exception as e:
				# poorman error handling
				print(e)
				self.init_config = False
		else:
			try:
				YamlGenerator.generate(self.function_name, f"{self.function_name}.yaml")
				self.init_config = True
				return True
			except Exception as e:
				# poorman error handlin
				print(e)
				self.init_config = False

		return self.init_config


	def init_deployment(self, yaml_storage = "./yaml_storage") -> bool:
		# will have to first init config
		assert(self.init_config)
		deployment = Deployment(self.function_name, f"{yaml_storage}/{self.function_name}")
		print("Creating deployment...")
		if not deployment.create():
			print("Failed to create deployment")
			return False
		print("Exposing environment_type type NodePort")
		if not deployment.expose():
			print("Failed to create deployment")
			return False
		deployed = True
		return deployed


if __name__ == "__main__":
	test_function = ServerlessFunction("foo", "def foo(): pass", "")
	test_function.init_config()
	test_function.init_deployment()






		

