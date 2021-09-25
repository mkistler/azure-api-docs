#!/usr/bin/env python3

# Create a "services" file containing all the Azure services (data-plane and mgmt-plane)

from datetime import date
import glob
import json
import os
import re

# Pull in the latest version of the Azure API docs (shallow clone)
# os.system('rm -rf azure-rest-api-specs')
# os.system('git clone --depth 1 https://github.com/Azure/azure-rest-api-specs.git')

# services is a dict where the "key" is a "service component" as defined by having its own 
# "preview" or "stable" directory under `specifications`. The value is also a dict with the following:
# - stable: the current stable version of the component
# - stableDir: the "stable" directory for the current stable version of the component
# - preview: the current preview version but only if more recent than stable
# - previewDir: the "preview" directory of the current preview version
services = {}

data_plane_stable = glob.glob('azure-rest-api-specs/specification/*/data-plane/**/stable', recursive=True)
mgmt_plane_stable = glob.glob('azure-rest-api-specs/specification/*/resource-manager/**/stable', recursive=True)

for service in data_plane_stable + mgmt_plane_stable:
    # Find the current stable version for this service -- assume it is the last one in sorted order
    stable_dir = sorted(glob.glob(service + '/*'), key=lambda x: x.split('/')[-1])[-1]
    version = stable_dir.split('/')[-1]
    # Save the stable version info
    key = '/'.join(stable_dir.split('/')[2:-2])
    services[key] = {
        'stable': version,
        'stableDir': re.sub('^azure-rest-api-specs/', '', stable_dir)
    }

data_plane_preview = glob.glob('azure-rest-api-specs/specification/*/data-plane/**/preview', recursive=True)
mgmt_plane_preview = glob.glob('azure-rest-api-specs/specification/*/resource-manager/**/preview', recursive=True)

for service in data_plane_preview + mgmt_plane_preview:
    # Find the current preview version for this service -- assume it is the last one in sorted order
    preview_dir = sorted(glob.glob(service + '/*'), key=lambda x: x.split('/')[-1])[-1]
    version = preview_dir.split('/')[-1]
    # Save the preview version info if newer than stable
    key = '/'.join(preview_dir.split('/')[2:-2])
    vers = re.sub('-((private)?[Pp]review|beta).*$', '', version)
    if key in services and vers <= services[key]['stable']:
        continue
    if key not in services:
        services[key] = {}
    services[key]['preview'] = version
    services[key]['previewDir'] = re.sub('^azure-rest-api-specs/', '', preview_dir)

with open('services.json', 'w') as fp:
    json.dump(services, fp, sort_keys=True)
