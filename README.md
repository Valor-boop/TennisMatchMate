# Tennis Match Mate

Tennis Match Mate is an automated solution designed to streamline your tennis scheduling process. By seamlessly integrating with your Gmail and Google Calendar, it ensures that you never miss a match again. Here's an overview of the project components:

## Project Structure

### main.py
The heart of the project, `main.py` orchestrates all functionalities by coordinating interactions between various modules.

### gmail_extraction.py
This module facilitates communication with Gmail, parsing through emails to extract crucial tennis-related information. The `gmail_extraction()` function efficiently retrieves tennis match details and compiles them into a structured list.

### gcal.py
Interfacing with the Google Calendar API, `gcal.py` empowers the creation and deletion of tennis events. With `gcal_event_creation()` and `delete_event()` functions, this module seamlessly integrates match scheduling and management into your Google Calendar. The use of a `token.json` file ensures secure and uninterrupted access to Google Calendar.

### helper.py
`helper.py` offers invaluable support with two essential functions:

- `time_conversion()`: This function converts timestamps into a standardized format, enhancing consistency and compatibility across platforms.
- `update_history()`: Tracking the project's performance, `update_history` maintains a detailed record of successful runs, including execution times, added matches, deleted matches, and total matches recorded. This information is stored in `time.txt` for easy reference and analysis.

### time.txt
A comprehensive log of project execution history, `time.txt` meticulously documents each successful run, providing insights into project performance and evolution over time.

## Functionality
Tennis Match Mate operates on a daily schedule, executing at 7 am to process emails from the previous day. Leveraging advanced email parsing and Google Calendar integration, it automatically creates corresponding events in your tennis calendar, ensuring prompt scheduling and effortless organization of matches.

With Tennis Match Mate, managing your tennis schedule has never been more efficient or hassle-free. Say goodbye to missed matches and scheduling headaches, and embrace the simplicity and convenience of automated tennis match coordination.
