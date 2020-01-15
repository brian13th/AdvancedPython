#!/usr/bin/env python
import requests
import json

r = requests.get('https://formulae.brew.sh/api/formula.json')
packages_json = r.json()

with open('json_response.json', 'w') as f:
    json.dump(packages_json, f, indent=2)
