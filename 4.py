import time
from datetime import datetime, timedelta

def scheduled_runner(runs_per_hour=12):
    """
    Run a function on a fixed schedule synced to the clock.
    Automatically determines the schedule based on current time and skips to next slot.
    
    Args:
        runs_per_hour: Number of times to run per hour (default: 12 = every 5 minutes)
    
    Examples:
        - 12 runs/hour = every 5 minutes (on :00, :05, :10, :15, :20, :25, :30, :35, :40, :45, :50, :55)
        - If current time is 1:23, next run is 1:25
        - If current time is 1:33, next run is 1:35
        - Automatically syncs to clock (always runs on the 5-minute marks)
    """
    
    def main_function():
        """The function that runs periodically"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Running main function...")
        # Add your code here
        
    def completion_function():
        """The function that runs when time is done"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Time's up! Running completion function...")
        print("All scheduled runs completed!")
        # Add your completion code here
    
    # Calculate interval between runs (in minutes)
    interval_minutes = 60 / runs_per_hour
    
    now = datetime.now()
    
    # Determine the schedule start time (beginning of current hour at minute 0)
    schedule_start = now.replace(minute=0, second=0, microsecond=0)
    
    # Calculate how many minutes have passed since the hour started
    minutes_in_hour = now.minute + (now.second / 60)
    
    # Find the next scheduled run slot
    # This finds which slot we're currently in or past
    current_slot = int(minutes_in_hour / interval_minutes)
    next_slot = current_slot + 1
    
    # Calculate the next run time
    next_run_minute = int(next_slot * interval_minutes-1)
    
    # If next run would be in the next hour, adjust
    if next_run_minute >= 59:
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
    while True:
        current_time = datetime.now()
        
        # Check if we've passed the end time
        if current_time >= end_time:
            break
        
        main_function()
        run_count += 1
        
        # Calculate next scheduled run
        next_run_time += timedelta(minutes=interval_minutes)
        
        # Check if next run would be past end time
        if next_run_time >= end_time:
            break
        
        # Wait until next scheduled time
        sleep_seconds = (next_run_time - datetime.now()).total_seconds()
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)
    
    # Run completion function
    completion_function()
    print(f"Total runs completed: {run_count}")

# Example usage
if __name__ == "__main__":
    # Runs 12 times per hour (every 5 minutes on :00, :05, :10, :15, :20, :25, :30, :35, :40, :45, :50, :55)
    # If you start at 1:23, it automatically waits until 1:25
    # If you start at 1:33, it automatically waits until 1:35
    scheduled_runner(runs_per_hour=12)
    
    # For 6 runs per hour (every 10 minutes on :00, :10, :20, :30, :40, :50)
    # scheduled_runner(runs_per_hour=6)
    
    # For 4 runs per hour (every 15 minutes on :00, :15, :30, :45)
    # scheduled_runner(runs_per_hour=4)