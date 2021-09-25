#!/usr/bin/env python3

# Create a file with the most recent API docs for all Azure services (data-plane and mgmt-plane)

from datetime import date
import json

# services is a dict where the "key" is a "service component" as defined by having its own 
# "preview" or "stable" directory under `specifications`. The value is also a dict with the following:
# - stable: the current stable version of the component
# - stableDir: the "stable" directory for the current stable version of the component
# - preview: the current preview version but only if more recent than stable
# - previewDir: the "preview" directory of the current preview version

with open('services.json', 'r') as fp:
    services = json.load(fp)

print(f'Found {sum("stable" in x for x in services.values())} stable services')

print(f'Found {sum("preview" in x for x in services.values())} preview services')

# preview services with no stable release
no_stable = [x for x in services.values() if 'stable' not in x]
print(f'Found {len(no_stable)} preview services with no stable release')

# Recent preview services with no stable release
one_year_ago = date.today().replace(year=date.today().year - 1).strftime('%Y-%m-%d')
recent_preview_no_stable = [x for x in no_stable if x['preview'] > one_year_ago]
print(f'Found {len(recent_preview_no_stable)} recent preview services with no stable release')
