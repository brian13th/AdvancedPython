#!/usr/bin/env python
import json
import pandas as pd

with open('package_info.json') as f:
    data = json.load(f)
data = json.dumps(data)
# data = json.loads(data)
df = pd.read_json(data)
print(data[0])
print(type(data))
print('=======================')
print(df.columns)
