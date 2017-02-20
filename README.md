# coco.registredService

A simple webservice with python and tornado, that binds to coco.registry

### Requirements

To run this service, you need to have :

* `conda` and `supervisord` installed. See [coco.main](https://github.com/factornado/coco.main)
* A service `coco.registry` than is up and running. See [coco.registry](https://github.com/factornado/coco.registry)


### Installation

Clone the repository somewhere.

    git clone https://github.com/factornado/coco.registeredService

Run the `deploy.sh` script and specify where you want to set the service
and what will be it's name and version:

    ./coco.registeredService/deploy.sh ./coco.main/services/myservice myservice v1

Build the service environment etc:

    ./coco.main/services/myservice/make.sh

Edit the `config.yml` and tune the parameters.
(You may eventually need to replace the registry url if it's not listening at `http://localhost:8800`.)

Restart supervisor:

    cd coco.main
    source activate supervisor
    supervisorctl reload
    supervisorctl start all

You should be able to test your service through the registry:

    curl http://localhost:8800/myservice/foo

    > Hello from service myservice. You've asked for uri foo
