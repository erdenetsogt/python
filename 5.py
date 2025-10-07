from datetime import datetime, timedelta, timezone
import time
runs_per_hour = 6
print(datetime.now(timezone.utc).isoformat())
interval_minutes = 60 / runs_per_hour
#now = datetime.now()
now = datetime.strptime("2025-10-07 21:00:00", "%Y-%m-%d %H:%M:%S").time()
schedule_start = now.replace(minute=0, second=0, microsecond=0)
print(f"start: {schedule_start}")
# Calculate how many minutes have passed since the hour started
minutes_in_hour = now.minute + (now.second / 60)
print(f"minutes_in_hour: {minutes_in_hour}")
# Find the next scheduled run slot
# This finds which slot we're currently in or past
current_slot = int(minutes_in_hour / interval_minutes)
next_slot = current_slot
print(f"next_slot: {next_slot}")
# Calculate the next run time
next_run_minute = int(next_slot * interval_minutes)

# If next run would be in the next hour, adjust
if next_run_minute >= 60:
    next_run_time = schedule_start + timedelta(hours=1)
    schedule_start = next_run_time  # Start schedule from next hour
else:
    next_run_time = schedule_start.replace(minute=next_run_minute, second=0, microsecond=0)

# Calculate end time (1 hour from when schedule starts)
#end_time = schedule_start + timedelta(hours=1)

# Calculate how many runs were missed
#missed_runs = current_slot

print(f"next_run_time: {next_run_time}")
if next_run_time > now:
    wait_seconds = (next_run_time - now).total_seconds()
    print(f"Waiting {wait_seconds:.1f} seconds...\n")
    time.sleep(wait_seconds)

                