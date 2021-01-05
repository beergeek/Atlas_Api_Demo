try:
  import requests
  import configparser
  import json
  import re
  import sys
  from flask import Flask, render_template, request
  from requests.auth import HTTPDigestAuth
except ImportError as e:
  print(e)
  sys.exit(1)

app = Flask(__name__)
config = configparser.ConfigParser()
config.read(sys.path[0] + '/creator.conf')
BASEURL = config.get('Atlas','baseurl')
ORGID = config.get('Atlas','orgID')
USERNAME = config.get('Atlas', 'username')
TOKEN = config.get('Atlas','token')
DEBUG = config.getboolean('general', 'debug', fallback=False)

AWS_REGION = "AP_SOUTHEAST_2"
GCP_REGION = "AUSTRALIA_SOUTHEAST_1"
CLUSTER_TEMPLATE = {
  "name": "cluster_name",
  "diskSizeGB": 40,
  "numShards": 1,
  "providerSettings": {
    "providerName": "PROVIDER",
    "diskIOPS": 300,
    "volumeType": "PROVISIONED",
    "instanceSizeName": "SIZE",
    "regionName": "REGION"
  },
  "clusterType" : "REPLICASET",
  "replicationFactor": 3,
  "backupEnabled": False,
  "providerBackupEnabled" : False,
  "autoScaling": {
    "diskGBEnabled": False
  },
  "mongoDBMajorVersion": "4.4"
}

def get(endpoint):
  resp = requests.get(BASEURL + endpoint, auth=HTTPDigestAuth(USERNAME, TOKEN), timeout=10)
  if resp.status_code == 200:
    group_data = json.loads(resp.text)
    return group_data
  else:
    print("GET response was %s, not `200`" % resp.status_code)
    print(resp.text)
    raise requests.exceptions.RequestException

def post(endpoint, config, code):
  header = {'Content-Type': 'application/json'}
  resp = requests.post(BASEURL + endpoint, auth=HTTPDigestAuth(USERNAME, TOKEN), timeout=10, data=json.dumps(config), headers=header)
  if resp.status_code == code:
    return resp
  else:
    print("PUT response was %s, not `200`" % resp.status_code)
    print(resp.text)
    raise requests.exceptions.RequestException

@app.route("/")
def start():
  projects = get("/orgs/%s/groups" % ORGID)
  return render_template('index.html', projects=projects['results'])

@app.route("/", methods=['POST'])
def create_new_cluster():
  projectID = 0
  try:
    if DEBUG:
      print(request.args)
    if re.search("^[a-f,0-9]{24}$", request.form['project']):
      projectID = request.form['project']
      if DEBUG:
        print("Project exists")
    else:
      project_data = post("/groups", {"name": request.form['project'], "orgId": ORGID}, 201)
      projectID = project_data.json()['id']
      if DEBUG:
        print("Project did not exist")
    if request.form['provider'] == 'AWS':
      region = AWS_REGION
    else:
      region = GCP_REGION
    x = {
      "name": request.form['cluster'],
      "providerSettings": {
        "providerName": request.form['provider'],
        "instanceSizeName": request.form['clusterSize'],
        "regionName": region
      }
    }
    cluster_config = CLUSTER_TEMPLATE
    cluster_config.update(x)
    if DEBUG:
      print(cluster_config)
    new_cluster = post("/groups/%s/clusters" % projectID, cluster_config, 201)
    return render_template('cluster.html', data=new_cluster.json())
  except Exception as e:
    print(e)

@app.route("/cluster.html")
def show_cluster():
  try:
    if DEBUG:
      print(request.args)
    status = get("/groups/%s/clusters/%s" %(request.args.get('group'), request.args.get('cluster')))
    if DEBUG:
      print(status)
    return render_template('cluster.html', data=status)
  except Exception as e:
    print(e)

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=5000, debug=DEBUG)