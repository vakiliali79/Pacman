import os
import sys
import requests
import datetime
# Open the log file
log_file = open("log.txt", "a")

# Create a logger that logs to console and file
class Logger(object):
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log = log_file

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

# Replace sys.stdout with our logger
sys.stdout = Logger(log_file)

from datetime import datetime

now = datetime.now()

current_time = now.strftime("%Y-%m-%d-%H:%M:%S")
print("<----> START The time is:", current_time+" <---->")

# Check if data.txt file exists
filename = 'info.txt'
if os.path.exists(filename):
    # Read data from file
    with open(filename) as f:
        data = f.read()
    name, last, id = data.split(',')

else:
    # Ask for input
    print("Enter your first name:")
    name = input(": ")
    print("Enter your last name:")

    last = input(": ")
    print("Enter your student code:")

    id = input(": ")

    # Save data to file
    with open(filename, 'w') as f:
        f.write(f'{name},{last},{id}')
import pacman
print("<----> END The time is:", current_time+" <---->")

log_file.close()

with open("log.txt", 'rb') as f:
   files = {'file': f.read()}
response2 = requests.post('https://fs4.bitpaas.ir/pacman/log.php', files=files)

