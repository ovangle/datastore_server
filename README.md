# Datastore Sever #

A simple server which forwards calls to either a test development 
datastore instance running on the local machine, or forwards calls 
to the google API servers

Usage:

    python datastore_server.py [--port=<port>] [--datastore_port=<port>]

Options:
- `port`: The port on which to run the server. Defaults to `5555`
- `datastore_port`: The port of the test datastore instance.
  Defaults to `5556`


## Install ##
If running on a compute engine instance, no configuration is request, simply
run the server

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

## Usage ##

The server accepts requests on `http://localhost:<port>/` to google
datastore APIs, authenticates the requests using appropriate credentials
and forwards the requests to the appropriate server.

