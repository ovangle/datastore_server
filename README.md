# Datastore Sever #

A simple server which forwards calls to either a test development 
datastore instance running on the local machine, or forwards calls 
to the google API servers

Usage:

    python datastore_server.py --port=[PORT] --datastore_port=[PORT]

`PORT` -- the port on the local machine to run the server. 
    defaults to `5555`

`DATASTORE_PORT` -- the port of the test datastore instance on 
    the local machine. Defaults to `5556`

## Usage ##
If running on a compute engine, no configuration is provided, simply
run 
    python development_server.py

If connecting to the google cloud datastore remotely, set environment
variables
 
    DATASTORE_SERVICE_ACCOUNT -- The id of the service account to connect
    DATASTORE_PRIVATE_KEY_FILE -- The `pem` file associated with the service account

It is also possible to run a test development instance without establishing 
a connection to the remote datastore. Install the [gcd][] tool and setup
a datstore directory on the local machine and unset any `DATASTORE_*`
environment variables.

Execute the local datastore using the comand

    bash gcd.sh start [DATASTORE_DIR] --port=5556

and run the request forwarding server
