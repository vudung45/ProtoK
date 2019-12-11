# ProtoK

A framework for Kubernetes that allows running serverless functions.
Serverless functions made easy for Kubernetes through a beautiful UI.

## Requirements
1. [NPM](https://www.npmjs.com/) - For managing Node Packages.
2. [Python3](https://www.python.org/download/releases/3.0/) - For managing the Controller Backend.
3. [Git](https://git-scm.com/) - Source control.

## Installation
### Setup Kubernetes Infra
1. `sh ./setup.sh` -- to apply all the necessary yaml configurations
2. `cd protok_controller; ./crd_controller.py` to run python CRD controller
3. `cd protok_controller; ./app.py` to run python CRD controller
4. Now Protok Kubernetes infrastructure should be fully setup if all of these go through

### Setup Web Frontend/Backend
1. Clone the repository 
```sh
$git clone https://github.com/dprasse/ProtoK.git
```

2. Install the required depenendencies from the main folder.
```sh
$npm install
```

3. Run the startup script that will install the dependencies and launch the frontend and backend server.
```sh
$npm start
```

4. You should now be able to access the frontend through your localhost url `http://localhost:8080/`


## Demo:
### Simple helloworld() demo
1. `curl -k -v -XPOST -H "Content-Type: application/json" -d@./protok_controller/templates/controller_create_function.json http://127.0.0.1:5000/apis/stable.protok.com/v1/namespaces/default/serverlessfunctions` -- to create a helloworld function that prints 2 input strings
2. `kubectl get serverlessfunctions` -- you should be able to see the newly created function here
3. `kubectl get pods` -- make sure that the pods is running
4. `curl -X POST --data '{"message1": "ok", "message2": "ok"}' http://127.0.0.1:8091/api/v1/namespaces/default/services/helloworld:http-function-port/proxy/ -H "Content-Type: application/json"`

## Info
`TODO: Info Section / Pictures / Demo`



## Credit
1. [Kubernetes](https://kubernetes.io/) - Container Orchestration.
2. [Dr. Vijay Chidambaram](http://www.cs.utexas.edu/~vijay/) - CS378 Virtualization Class
3. [VueJS](https://vuejs.org/) - Frontend Framework.
4. [BootstrapVue](https://bootstrap-vue.js.org/) - Frontend Framework. 
5. [CreativeTim](https://www.creative-tim.com/) - Portions of Dashboard Templating.
6. [ExpressJS](https://expressjs.com/) - Web Backend Framework.
7. [Flask](https://www.fullstackpython.com/flask.html) - Python Backend Framework.