docker build -t jcharante/jyanz-com . && docker push jcharante/jyanz-com && docker-machine ssh nyc-drone-1 'docker service update --with-registry-auth --image jcharante/jyanz-com jyanz-com'
