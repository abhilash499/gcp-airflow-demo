import yaml
import json

with open('./workflow/workflow_data_cleaner.yaml') as f:
    dataMap = yaml.safe_load(f)
    with open('out.json', 'w') as outfile:
        json.dump(dataMap, outfile)
    # print(dataMap)
