import http.client
import random
import json

def randTemp():
    a = random.uniform(1, 80)
    return round(a,2)
def randPressure():
    a = random.uniform(1, 10)
    return round(a,2)

conn = http.client.HTTPConnection("mysql-server-tailscale.tailb51a53.ts.net", 5000)
a = 3.6
payload = json.dumps({
  "sensorObjects": [
    {
      "sensorObjectId": 9,
      "value": randTemp()
    },
    {
      "sensorObjectId": 10,
      "value": randTemp()
    },
    {
      "sensorObjectId": 11,
      "value": randPressure()
    },
    {
      "sensorObjectId": 12,
      "value": randPressure()
    },
    {
      "sensorObjectId": 13,
      "value": randTemp()
    },
    {
      "sensorObjectId": 14,
      "value": randTemp()
    },
    {
      "sensorObjectId": 15,
      "value": randPressure()
    },
    {
      "sensorObjectId": 16,
      "value": randPressure()
    }
  ]
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZW1haWwiOiJlcmRlbmV0c29ndEBnbWFpbC5jb20iLCJwZW9wbGVJZCI6MiwiY29tcGFueUlkIjoyLCJpYXQiOjE3NTcwMDE3MzIsImV4cCI6MTc1NzAwMzUzMn0.aYxI8TLq6fEUX2ogt4sF_2nxv45g2drqAtY_kq9zT18'
}
try:
    conn.request("POST", "/v/value1", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))    
except Exception as e:
    print(e)

