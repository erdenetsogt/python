import requests
import json

url = "http://mysql-server-tailscale.tailb51a53.ts.net:5000/v/m/current/1"

payload = json.dumps({
  "sensorObjects": [
    {
      "sensorObjectId": 9,
      "value": 2.4
    },
    {
      "sensorObjectId": 10,
      "value": 2.4
    },
    {
      "sensorObjectId": 11,
      "value": 2.4
    },
    {
      "sensorObjectId": 12,
      "value": 2.4
    },
    {
      "sensorObjectId": 13,
      "value": 2.4
    },
    {
      "sensorObjectId": 14,
      "value": 2.4
    },
    {
      "sensorObjectId": 15,
      "value": 2.4
    },
    {
      "sensorObjectId": 16,
      "value": 2.4
    }
  ]
})

headers = {
  'Content-Type': 'application/json',
  
}

response = requests.request("GET", url, headers=headers, data=payload)
json_data = json.loads(response.text)

print(json_data.get("name"))