#!/usr/bin/env python3
import requests
import json
import time
import logging
import random
from datetime import datetime, timedelta, timezone

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
  
 

def generate_sample_data(id,date): 
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
  data2['date'] = date
  print(json.dumps(data2))
  return json.dumps(data2)
count=[1,2,3,4,5]
def main():
    # Configuration
    API_BASE_URL = "http://mysql-server-tailscale.tailb51a53.ts.net:5000"  # Replace with your API
    ENDPOINT = "/v/value"
    #LOOP_INTERVAL = 600  # seconds between requests
    MAX_REQUESTS = 10  # Set to None for infinite loop
    
    # Optional: Add authentication headers
    headers = {
        'Content-Type': 'application/json',
        # 'Authorization': 'Bearer your-token-here',
        # 'X-API-Key': 'your-api-key-here'
    }
    runs_per_hour = 6  # Number of runs per hour
    # Initialize API client
    client = APIClient(API_BASE_URL, headers)
    
    request_count = 0
    logging.info("Starting API POST loop...")
    
    try:
        while True:
            # Generate or prepare your data
            interval_minutes = 60 / runs_per_hour
            now = datetime.now()
            schedule_start = now.replace(minute=0, second=0, microsecond=0)
    
            # Calculate how many minutes have passed since the hour started
            minutes_in_hour = now.minute + (now.second / 60)
            
            # Find the next scheduled run slot
            # This finds which slot we're currently in or past
            current_slot = int(minutes_in_hour / interval_minutes)
            next_slot = current_slot + 1
            
            # Calculate the next run time
            next_run_minute = int(next_slot * interval_minutes)
            
            # If next run would be in the next hour, adjust
            if next_run_minute >= 60:
                next_run_time = schedule_start + timedelta(hours=1)
                schedule_start = next_run_time  # Start schedule from next hour
            else:
                next_run_time = schedule_start.replace(minute=next_run_minute, second=0, microsecond=0)
            
            # Calculate end time (1 hour from when schedule starts)
            end_time = schedule_start + timedelta(hours=1)
            
            # Calculate how many runs were missed
            missed_runs = current_slot
            
            print(f"Current time: {now.strftime('%H:%M:%S')}")
            print(f"Schedule: Every {interval_minutes:.0f} minutes (runs per hour: {runs_per_hour})")
            print(f"Schedule runs from: {schedule_start.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
            
            if missed_runs > 0:
                print(f"Missed runs this hour: {missed_runs}")
            
            print(f"Next scheduled run: {next_run_time.strftime('%H:%M:%S')}")
            
            # Wait until next scheduled time
            wait_seconds = (next_run_time - now).total_seconds()
            if wait_seconds > 0:
                print(f"Waiting {wait_seconds:.1f} seconds...\n")
                time.sleep(wait_seconds)
            
            print(f"Starting scheduled runs until {end_time.strftime('%H:%M:%S')}...\n")
            
            run_count = 0
            
            # Run the function at scheduled intervals
            
            current_time = datetime.now(timezone.utc).isoformat()
            
            # Check if we've passed the end time
            #if current_time >= end_time:
                #break
            
            for i in count:             
          
              logging.info(f"Preparing data for sensor ID {i} (Request #{request_count})")
              # Generate sample data
              data = generate_sample_data(i,current_time)
            
              # Post data to API
              result = client.post_data(ENDPOINT, data)
            
              if result:
                logging.info(f"Response: {result}")           
              time.sleep(1)
            run_count += 1
            
            # Calculate next scheduled run
            next_run_time += timedelta(minutes=interval_minutes)
            
            # Check if next run would be past end time
            #if next_run_time >= end_time:
                #break
            
            # Wait until next scheduled time
            sleep_seconds = (next_run_time - datetime.now()).total_seconds()
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
            
            
            
            # Wait before next request
            #logging.info(f"Waiting {LOOP_INTERVAL} seconds before next request...")
            #time.sleep(LOOP_INTERVAL)
            
            
    except KeyboardInterrupt:
        logging.info("Loop interrupted by user. Exiting...")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        logging.info(f"Total requests made: {request_count}")

if __name__ == "__main__":
    main()