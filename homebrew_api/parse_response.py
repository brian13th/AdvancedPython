#!/usr/bin/env python
import json
import requests
import time

with open('json_response.json') as f:
    packages = json.load(f)


data = []
i=0
for package in packages:
    r = requests.get(f'https://formulae.brew.sh/api/formula/{package["name"]}.json')
    # print(r.json())
    package_installations = r.json()['analytics']['install']['30d'][f'{package["name"]}']
    package_build_errors = r.json()['analytics']['build_error']['30d'][f'{package["name"]}']
    package_description = r.json()['desc']
    package_homepage = r.json()['homepage']
    info = {
        'name': package["name"],
        'description': package_description,
        'homepage':package_homepage,
        'info':{
            'installations': package_installations,
            'errors': package_build_errors
        }
    }
    data.append(info)
    print(f'Package {package["name"]} downloaded in {r.elapsed.total_seconds()} seconds.')
    time.sleep(r.elapsed.total_seconds())
    i+=1
    if i>100:
        break


with open('package_info.json', 'w') as f:
    json.dump(data, f, indent=2)
