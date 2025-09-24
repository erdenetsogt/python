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
def randTemp():
    a = random.uniform(1, 80)
    return round(a,2)
def randPressure():
    a = random.uniform(1, 10)
    return round(a,2)
def generate_sample_data():
    """Generate sample data for posting"""
    return json.dumps({
  "sensorObjects": [
    {
      "sensorObjectId": 1,
      "value": randTemp()
    },
    {
      "sensorObjectId": 2,
      "value": randTemp()
    },
    {
      "sensorObjectId": 3,
      "value": randPressure()
    },
    {
      "sensorObjectId": 4,
      "value": randPressure()
    },
    {
      "sensorObjectId": 5,
      "value": randTemp()
    },
    {
      "sensorObjectId": 6,
      "value": randTemp()
    },
    {
      "sensorObjectId": 7,
      "value": randPressure()
    },
    {
      "sensorObjectId": 8,
      "value": randPressure()
    }
  ]
})
    

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
            data = generate_sample_data()
            
            # Post data to API
            result = client.post_data(ENDPOINT, data)
            
            if result:
                logging.info(f"Response: {result}")           
            
            
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