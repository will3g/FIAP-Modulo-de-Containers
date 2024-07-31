# /bin/bash

docker run --rm -it --network bridge_network -v ./dump:/data mongodb-tools sh -c 'mongorestore --uri="mongodb://root:root@mongodb/finance" . --authenticationDatabase=admin'
