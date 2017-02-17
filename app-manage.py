#!/usr/bin/env python2.7
# Accesses the Marathon REST api, downloads all running apps and saves them
# as YAML.

import argparse

import urlparse
import requests
import os
import os.path
import sys

import ruamel.yaml as yaml

os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(
    '/etc/ssl/certs/',
    'ca-certificates.crt')

# Fields which get returned from the API, but which can't be set.
removeableFields = set([
    "version",
    "versionInfo",
    "tasksStaged",
    "tasksRunning",
    "tasksHealthy",
    "tasksUnhealthy",
    "deployments"
])

def delete(args):
    appsToDelete = None
    if args.app is not None:
        appsToDeploy = tuple(args.app)
    delUriBase = urlparse.urljoin(args.marathon_api, "/v2/apps")
    for root, dirs, files in os.walk(args.state_dir):
        for fname in files:
            appPath = os.path.join(root, fname)

            if ('/' + os.path.relpath(appPath, start=args.state_dir)) in appsToDeploy or args.all:
                if os.path.isfile(appPath):
                    appJson = yaml.load(open(appPath, 'r'))
                    if appJson['id'][:1] != "/":            
                        appJson['id'] = '/' + appJson['id']
                    print("Deleting app: {}".format(appJson['id']))
                    delUri = delUriBase + appJson['id']
                    r = requests.delete(delUri, json=appJson)
                    if not r.ok:
                        print(r)
                        print(r.text)           
    
def post(args):
    appsToDeploy = None
    if args.app is not None:
        appsToDeploy = tuple(args.app)
    postUri = urlparse.urljoin(args.marathon_api, "/v2/apps")
    for root, dirs, files in os.walk(args.state_dir):
        for fname in files:
            appPath = os.path.join(root, fname)

            if ('/' + os.path.relpath(appPath, start=args.state_dir)) in appsToDeploy or args.all:
                if os.path.isfile(appPath):
                    appJson = yaml.load(open(appPath, 'r'))
                    if appJson['id'][:1] != "/":            
                        appJson['id'] = '/' + appJson['id']
                    print("Adding app configuration: {}".format(appJson['id']))
                    
                    r = requests.post(postUri, json=appJson)
                    if not r.ok:
                        print(r)
                        print(r.text)


def get(args):
    updateUri = urlparse.urljoin(args.marathon_api, "/v2/apps/")
    r = requests.get(updateUri)
    processed = []
    for app in r.json()['apps']:
        for fld in removeableFields:
            del app[fld]
        processed.append(app)

    oncluster = set()
    for app in processed:
        appJson = os.path.join(args.state_dir, app['id'][1:].replace("/","_") + ".yml")
        appJsonDir = os.path.dirname(appJson)
        try:
            os.makedirs(appJsonDir)
        except OSError as e:
            pass
        with open(appJson, "w") as f:
            yaml.dump(app, f, Dumper=yaml.RoundTripDumper, default_flow_style=False)
            print("Downloaded app configuration: {}".format(app['id']))
        oncluster.add(appJson)

    # Delete non-existent apps
    ondisk = set()
    for root, dirs, files in os.walk(args.state_dir):
        for f in files:
            ondisk.add(os.path.join(root,f))
    # Get the list to remove
    toremove = ondisk.difference(oncluster)
    
    for jsonpath in toremove:
        print("Removing deleted app: {}".format(jsonpath))
        os.unlink(jsonpath)
    
    print("Update complete.")

parser = argparse.ArgumentParser(description="Updates or Pushes the Marathon JSON configurations")
parser.add_argument("--marathon-api", required=True, help="Marathon Endpoint")
parser.add_argument("--state-dir", default="yaml", help="Directory to save configuration too")

subparsers = parser.add_subparsers(title="Commands")

update_parser = subparsers.add_parser('get', help='Pull down the current marathon configuration')
update_parser.set_defaults(which=get)

put_parser = subparsers.add_parser('post', help='Post the stored marathon configuration back')
put_parser.set_defaults(which=post)
put_parser.add_argument("--all", action='store_true', help='Deploy all apps in the app directory')
put_parser.add_argument("app", nargs="*", metavar="APP", help='Put a specific app or set of apps')

del_parser = subparsers.add_parser('delete', help='Post the stored marathon configuration back')
del_parser.set_defaults(which=delete)
del_parser.add_argument("--all", action='store_true', help='Deploy all apps in the app directory')
del_parser.add_argument("app", nargs="*", metavar="APP", help='Put a specific app or set of apps')

args = parser.parse_args()

args.which(args)
