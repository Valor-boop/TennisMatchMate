'''
Patrick
3/13/2024
'''
from datetime import datetime, timedelta
import re

def time_conversion(time):
    '''
    Converts a date and time string to a specific format and calculates the end time.

    Parameters:
        time (str): The input date and time string in the format '%A %B %d, %Y at %I:%M %p'.

    Returns:
        Tuple[str, str]: A tuple containing the start and end date and time strings 
        in the format '%Y-%m-%dT%H:%M:%S'.
    '''
    # Input date and time string
    input_date_time_str = time

    # Convert the input string to a datetime object
    input_datetime = datetime.strptime(input_date_time_str, '%A %B %d, %Y at %I:%M %p')

    # Convert the datetime object to the desired format
    start_output_date_time_str = input_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    end_date_time = input_datetime + timedelta(hours=1)
    end_output_date_time_str = end_date_time.strftime('%Y-%m-%dT%H:%M:%S')
    return start_output_date_time_str, end_output_date_time_str

def update_history(file_path, added_matches, deleted_matches):
    '''
    Updates a .txt file  with the current run details (including time of execution,
    number of matches added, number of matches deleted and total matches).

    Parameters:
        file_path (string): A file path representing the locaiton of 'time.txt', the
        txt file that contains the execution history of the project
        added_matches (int): The number of matches added for the current project run
        deleted_matches (int): The number of matches deleted for the current project run 
    
    Returns: 
        None
    '''
    # Read the existing contents of the file if it exists
    try:
        with open(file_path, 'r') as file:
            existing_data = file.read()
    except FileNotFoundError:
        existing_data = ''
    
    # Get current time 
    current_time = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
    # Calculate the total matches value as the difference between the added and deleted matches 
    matches = re.findall(r'Total Matches: (\d+)', existing_data)
    total_matches = int(matches[0]) if matches else 0
    total_matches += added_matches - deleted_matches

    # Delete old Total Matches line in order to replace it with new value
    existing_data = re.sub(r'Total Matches: (\d+)', '', existing_data)
    
    # Prepare the updated data with the total matches at the top
    updated_data = f"Total Matches: {total_matches}\n\n"
    updated_data += f"RunTime: {current_time}\n"
    updated_data += f"Added Matches: {added_matches}\n"
    updated_data += f"Deleted Matches: {deleted_matches}\n"
    
    # Append the existing data (if any)
    updated_data += existing_data

    # Write the updated data to the file
    with open(file_path, 'w') as file:
        file.write(updated_data)