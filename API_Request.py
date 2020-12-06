import requests
import json
import pprint

response = requests.get("")


print(response.status_code)

print(response.json())

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    #how many crimes do we have data on
    text_list = list(text)
    print(len(text_list))

#jprint(response.json())
pprint.pprint(response.json())
#for d in response.json():


