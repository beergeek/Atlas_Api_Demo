## Create Cluster

The cluster creator script is a basic Python Flask application used to create new projects and clusters within an organisation in MongoDB Atlas. The application provides the ability to select a subset of cloud vendors and instances sizes for the clusters.

The configuration file must reside in the same directory as the Python script and is name `creater.conf`.

The following is the basic configuration:

```shell
[Atlas]
connection_string=mongodb://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/?replicaSet=<REPLICA_SET_NAME>&<OTHER_OPTIONS>
baseurl=https://cloud.mongodb.com/api/atlas/v1.0
orgID=<ORG ID>
username=<API PUBLIC KEY>
token=<API PRIVATE KEY>

[general]
debug=<BOOLEAN_VALUE>
```

Example:

```shell
[Atlas]
baseurl=https://cloud.mongodb.com/api/atlas/v1.0
orgID=5a05659cd303ad74f1cdd047
username=RVWUHKGN
token=2ebfef5a-be6e-41f9-34cc-7d955e72a98c

[general]
debug=false
```

The application listens on localhost on port 5000 via HTTP, the script can be modified manually to change network device, port and use HTTPS if desired.

### Setup

The script can run on any Linux node that has access to the Audit DB.

The following non-standard Python modules are required (and dependancies):

* [configparser](https://pypi.org/project/configparser/)
* [flask](https://pypi.org/project/Flask/)

The script and config file must be located in the same directory.

The Flask application can be run standalone for via a setup with a web server and WSGI (see Flask documentation).

The application is contained within the `flask directory` and can be run in the foreground with `python3 /data/scripts/flask/reporter.py`.

The website can be reached via `http://localhost:8000/ (if defaults are used).