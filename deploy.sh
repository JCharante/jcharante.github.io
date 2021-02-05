#!/bin/bash
docker build -t jcharante/jyanz-com . && docker push jcharante/jyanz-com && docker-machine ssh nyc-drone-1 'docker service create -p 3401:3401 --name jyanz-com --with-registry-auth jcharante/jyanz-com'
