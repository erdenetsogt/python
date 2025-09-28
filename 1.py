import requests
import json
import random


def setSensorValue(val, id):
  match id:
    case 1: #
      return setValue(80,96,val)
    case 2: #
      return setValue(70,86,val)
    case 3: #
      return setValue(75,85,val)
    case 4: #      
      return setValue(50,68,val)
    case 5: #
      return setValue(6.5,9.6,val)
    case 6: #
      return setValue(5.2,7.6,val)
    case 7: #
      return setValue(3.2,4.5,val)
    case _: #
      return setValue(2.8,4.0,val)
  
  
def setValue(min,max,val1):
  val = float(val1)
  print("val1: ",val)
  a = random.uniform(0,9)
  b = round(a)
  print("ytga: ",b)
  if(b<3):
    val = val + 0.1
    if(val>max):
      val = val - 0.1
    #return val
  if(b>7):
    val = val - 0.1
    if(val<min):
      val = val + 0.1
    #return val
  val = round(val,1)
  print("val: ",val)
  return val
  
def getValue(id):

  url = "http://mysql-server-tailscale.tailb51a53.ts.net:5000/v/m/current/"+str(id)


  headers = {
    'Content-Type': 'application/json',
    
  }
  response = requests.request("GET", url, headers=headers)
  json_data = json.loads(response.text)
  data1 = []
  data = {}
  for item in json_data.get("sensorObject"):
      data['sensorObjectId'] = item.get("id")
      data['value'] = setSensorValue(item.get("sensorObjectValue").get("value"),item.get("id"))    
      data1.insert(len(data1),data.copy())
      print(item.get("id"), item.get("sensorObjectValue").get("value"))
     

  print(json.dumps(data1))

count=[1,2,3,4,5]

for i in count:
  getValue(i)


