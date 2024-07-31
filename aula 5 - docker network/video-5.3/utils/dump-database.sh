# /bin/bash

docker run --rm -it --network mynetwork -v .:/data mongodb-tools sh -c 'mongodump --uri="mongodb://root:root@mongodb/finance" --authenticationDatabase=admin'
