#!/usr/bin/env python3
import requests
import json
import time
import logging
import random
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_posts.log'),
        logging.StreamHandler()
    ]
)

class APIClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {'Content-Type': 'application/json'}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def post_data(self, endpoint, data):
        """Post data to API endpoint"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.request("POST", url, headers={'Content-Type': 'application/json'}, data=data, timeout=10)
            response.raise_for_status()
            logging.info(f"POST successful: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"POST failed: {e}")
            return None

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
  
 

def generate_sample_data(id):
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
      #print(item.get("id"), item.get("sensorObjectValue").get("value"))
  data2={}
  data2['sensorObjects'] = data1
  print(json.dumps(data2))
  return json.dumps(data2)
count=[1,2,3,4,5]
def main():
    # Configuration
    API_BASE_URL = "http://mysql-server-tailscale.tailb51a53.ts.net:5000"  # Replace with your API
    ENDPOINT = "/v/value"
    LOOP_INTERVAL = 60  # seconds between requests
    MAX_REQUESTS = 10  # Set to None for infinite loop
    
    # Optional: Add authentication headers
    headers = {
        'Content-Type': 'application/json',
        # 'Authorization': 'Bearer your-token-here',
        # 'X-API-Key': 'your-api-key-here'
    }
    
    # Initialize API client
    client = APIClient(API_BASE_URL, headers)
    
    request_count = 0
    logging.info("Starting API POST loop...")
    
    try:
        while True:
            # Generate or prepare your data
            for i in count:
              
              
              logging.info(f"Preparing data for sensor ID {i} (Request #{request_count})")
              # Generate sample data
              data = generate_sample_data(i)
            
              # Post data to API
              result = client.post_data(ENDPOINT, data)
            
              if result:
                logging.info(f"Response: {result}")           
              time.sleep(2)
            
            # Wait before next request
              logging.info(f"Waiting {LOOP_INTERVAL} seconds before next request...")
            time.sleep(LOOP_INTERVAL)
            
    except KeyboardInterrupt:
        logging.info("Loop interrupted by user. Exiting...")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        logging.info(f"Total requests made: {request_count}")

if __name__ == "__main__":
    main()