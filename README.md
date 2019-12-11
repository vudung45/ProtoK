# ProtoK

A serverless framework for Kubernetes that allows running functions.
Serverless functions made easy for Kubernetes through a beautiful UI.

## Installation
### Setup Kubernetes Infra
1. `sh ./setup.sh` -- to apply all the necessary yaml configurations
2. `cd protok_controller; ./crd_controller.py` to run python CRD controller
3. `cd protok_controller; ./app.py` to run python CRD controller
4. Now Protok Kubernetes infrastructure should be fully setup if all of these go through

### Setup Web Frontend&Backend



## Demo:
### Simple helloworld() demo
1. `curl -k -v -XPOST -H "Content-Type: application/json" -d@./protok_controller/templates/controller_create_function.json http://127.0.0.1:5000/apis/stable.protok.com/v1/namespaces/default/serverlessfunctions` -- to create a helloworld function that prints 2 input strings
2. `kubectl get serverlessfunctions` -- you should be able to see the newly created function here
3. `kubectl get pods` -- make sure that the pods is running
4. `curl -X POST --data '{"message1": "ok", "message2": "ok"}' http://127.0.0.1:8091/api/v1/namespaces/default/services/helloworld:http-function-port/proxy/ -H "Content-Type: application/json"`

## Info
`TODO: Info Section / Pictures / Demo`

## Credit
`TODO: link to any credits`