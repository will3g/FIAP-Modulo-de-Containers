# /bin/bash

docker run --rm -it --network bridge_network -v .:/data mongodb-tools sh -c 'mongodump --uri="mongodb://root:root@mongodb/finance" --authenticationDatabase=admin'
