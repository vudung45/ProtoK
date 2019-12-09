
yaml_template = "apiVersion: v1 \nkind: Pod  \nmetadata:  \n  name: {service_name}  \nspec:  \n  selector:  \n    matchLabels: \n      app: {service_name} \n  replicas: 1  \n  template: \n    metadata: \n      labels: \n        app: {service_name} \n    spec: \n      containers: \n        - name: {service_name} \n          image: protok_serverless \n          ports: \n          - containerPort: 8080"

class YamlGenerator(object):
  @classmethod
  def generate(cls, service_name, output_yaml):
    yaml_content = yaml_template.format(service_name = service_name)
    cls.manual_generate(yaml_content, output_yaml)

  @classmethod
  def manual_generate(cls, yaml_content, output_yaml):
     with open(output_yaml, "w+") as f:
      f.write(yaml_content)




# unit tests
if __name__ == '__main__':
	YamlGenerator.generate("test_service", "test.yaml")

