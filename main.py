'''
Patrick
3/13/2024
'''
from gcal import gcal_event_creation, delete_event
from helper import time_conversion, update_history
from gmailReader import gmail_extraction

def main():
    user = ''
    password = ''
    specificSender = ''
    tennisCalendarId = ''

    # Extract all created and deleted emails from inbox
    email_list = gmail_extraction(user, password, specificSender)
    addedMatches = 0
    deletedMatches = 0

    # Iterate through created emails
    for i in email_list:
        if i['Status'] == "Created":
            print("Creating Event:")
            location = i['Facility']
            participants = i['Participants']
            startTime, endTime = time_conversion(i['Date and Time'])
            gcal_event_creation(location, participants, startTime, endTime, tennisCalendarId)
            print("Event Created!")
            addedMatches += 1
        else:
            print('Deleting Event:')
            delete_event(i, tennisCalendarId)
            deletedMatches += 1
            print('Event Deleted!')
    update_history('time.txt', addedMatches, deletedMatches)

if __name__ == '__main__':
    main()