
yaml_template = "apiVersion: apps/v1 \nkind: Deployment  \nmetadata:  \n  name: {service_name}  \nspec:  \n  selector:  \n    matchLabels: \n      app: {service_name} \n  replicas: 1  \n  template: \n    metadata: \n      labels: \n        app: {service_name} \n    spec: \n      containers: \n        - name: {service_name} \n          image: davidvu98/protok_serverless:basic\n          env: \n            - name: DEPENDENCIES\n              value: \"{dependencies}\"\n            - name: FUNCTION_CONTENT\n              value: \"{function_content}\"\n          ports: \n          - containerPort: 8080"

class YamlGenerator(object):
  @classmethod
  def generate(cls, service_name, dependencies, function_content, output_yaml):
    dependencies= dependencies.replace('"', '\"')
    function_content = function_content.replace('"', '\"')
    yaml_content = yaml_template.format(service_name = service_name, dependencies = dependencies, function_content = function_content)
    cls.manual_generate(yaml_content, output_yaml)

  @classmethod
  def manual_generate(cls, yaml_content, output_yaml):
     with open(output_yaml, "w+") as f:
      f.write(yaml_content)




# unit tests
if __name__ == '__main__':
  YamlGenerator.generate("test_service", "test.yaml")

