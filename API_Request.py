import requests
import json

response = requests.get("https://data.norfolk.gov/resource/cab7-wvn5.json")

print(response.status_code)

print(response.json())

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(response.json())