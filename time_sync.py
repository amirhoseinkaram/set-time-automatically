import requests
import os
import subprocess
from datetime import datetime
import pyuac

def main():
    print("Do stuff here that requires being run as an admin.")
    # The window will disappear as soon as the program exits!
    input("Press enter to close the window. >")

def get_time_for_city(city):
    # URL of the website to get the current time for a specific city
    time_api_url = f"http://worldtimeapi.org/api/timezone/{city}"
    
    # Get the current time from the website
    response = requests.get(time_api_url)
    if response.status_code == 200:
        current_time_data = response.json()
        return current_time_data['datetime']
    else:
        print("Failed to get the current time from the API.")
        return None

def set_system_time(current_time, os_type):
    # Parse the time and format it for the system time command
    current_time_obj = datetime.fromisoformat(current_time[:19])
    if os_type == 'Windows':
        formatted_time = current_time_obj.strftime('%#H:%M:%S')
    else:
        formatted_time = current_time_obj.strftime('%-H:%M:%S')
    
    formatted_date = current_time_obj.strftime("%m/%d/%Y")
    
    am_pm = current_time_obj.strftime("%p")
    if os_type == 'Windows':
        date_time_command = f"Set-Date '{formatted_date} {formatted_time} {am_pm}'"
        print(f"Setting system time with command: {date_time_command}")
        subprocess.run(['powershell', '-Command', date_time_command], shell=True)
    else:
        print('This program cannot run on your operating system.')

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:
        main()
        
        city = input("Enter the city (e.g., Asia/Tehran): ")
        current_time = get_time_for_city(city)
        
        if current_time:
            print(f"Current time in {city}: {current_time}")
            os_type = 'Windows' if os.name == 'nt' else 'Linux'
            set_system_time(current_time, os_type)
