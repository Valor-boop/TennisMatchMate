'''
Patrick
3/13/2024
'''
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import re

def gmail_extraction(user, password, specificSender):
    '''
    Extracts booking information from Gmail inbox.

    Parameters: 
        user (str): The user's Gmail address. 
        password (str): The password used to access the user's Gmail account. 
        specificSender (str): The email address of the sender whose emails will be processed. 

    Returns:
        List[Dict]: A list of dictionaries containing booking information, 
        including participants, date and time, facility, and status (created or deleted).
    '''
    imapServer = 'imap.gmail.com'

    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(imapServer)

    # Log in to the email account
    mail.login(user, password)

    # Select the mailbox that you want to work with (in this case the 'INBOX')
    mailboxName = 'INBOX'
    mail.select(mailboxName)

    # Define the date from which you want to search (in this case past 2 days )
    since_date = (datetime.now() - timedelta(days=0)).strftime("%d-%b-%Y")

    # Search for emails sent since the specified date and sender
    searchCriteria = f'SINCE {since_date} FROM "{specificSender}"'

    # Perform search within the mailbox we selected using the search criteria 
    status, emailIds = mail.search(None, searchCriteria)

    # Patterns for extraction from email body
    participantsPattern = r"Participants: <b>(.*?)</b>"
    datePattern = r"Date and Time: <b>(.*?)</b>"
    facilityPattern = r"Facility: <b>(.*?)</b>"

    emailDataList = []
    if status =='OK':
        emailIdList = emailIds[0].split()
        print(f'Emails from {specificSender} sent since {since_date}:')
        for emailId in emailIdList:
            # Fetch the email by its ID
            status, emailData = mail.fetch(emailId, '(RFC822)')
            if status == 'OK':
                # Extract email bytes 
                rawEmail = emailData[0][1]
                msg = email.message_from_bytes(rawEmail)

                # Handle encoding and decoding excpetions for the subject 
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode = True).decode()
                        # Extract participants using the regular expression
                        participantsMatch = re.search(participantsPattern, body)
                        participants = participantsMatch.group(1) if participantsMatch else None
                        
                        # Extract date and time using the regular expression
                        dateTimeMatch = re.search(datePattern, body)
                        dateTime = dateTimeMatch.group(1) if dateTimeMatch else None
                        
                        # Extract location using the regular expression
                        facilityMatch = re.search(facilityPattern, body)
                        facility = facilityMatch.group(1) if facilityMatch else None

                        if "Deleted" in subject:
                            status = "Deleted"
                        elif "Created" in subject:
                            status = "Created"
                        else:
                            print("Not a booking email")

                        # Store the email data in a dictionary
                        emailData = {
                            "Participants": participants,
                            "Date and Time": dateTime,
                            "Facility": facility,
                            "Status": status
                        }
    
                        emailDataList.append(emailData)                
    # Close mailbox and logout 
    mail.close()
    mail.logout()
    return emailDataList