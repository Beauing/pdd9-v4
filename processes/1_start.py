import re
from datetime import datetime
import subprocess
import time

# Define the format_datetime function
def format_datetime(timestamp):
    datetime_obj = datetime.fromtimestamp(float(timestamp))
    date_str = datetime_obj.strftime('%Y-%m-%d')
    time_str = datetime_obj.strftime('%H:%M:%S')
    return date_str, time_str

input_path = 'openarena_20240523_11.35.log'
output_path = 'processes/processed_logs/start.log'

# Read the input file
with open(input_path, 'r') as file:
    lines = file.readlines()

# Process the file and write to the output file
with open(output_path, 'w') as output_file:
    for line in lines:
        if '\\x08Kill' in line or '\\x08PlayerScore' in line:
            # Extract timestamp and format it
            parts = line.split(': ', 1)
            timestamp = parts[0]
            date_str, time_str = format_datetime(timestamp)
            formatted_line = f"{date_str} {time_str}: {parts[1].strip()}"
            output_file.write(formatted_line + '\n')
        elif 'Network egress latency:' in line or '\\x08loaded maps' in line:
            # Extract timestamp and format it
            parts = line.split(': ', 1)
            timestamp = parts[0]
            date_str, time_str = format_datetime(timestamp)
            formatted_line = f"{date_str} {time_str}: {parts[1].strip()}"
            output_file.write(formatted_line + '\n')
        else:
            print(f"No match: {line.strip()}")