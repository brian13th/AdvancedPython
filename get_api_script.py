#!/usr/bin/env python
import requests
import json

r = requests.get('https://formulae.brew.sh/api/formula.json')
packages_json = r.json()

packages_json = json.dumps(packages_json, indent=2)
print(packages_json[1][0])
