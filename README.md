
# To-Do List App with User Authentication

## Overview
This is a To-Do List application with integrated user authentication, featuring login and signup pages. The app includes task management with customizable themes, reminders, and a visually appealing interface. The signin and signup functionalities are powered by MSSQL using pymysql for database operations.

## Features

- User Authentication: Login and signup pages with password reset functionality.
- Task Management: Add, edit, sort, complete, uncomplete, and delete tasks with categories, importance levels, deadlines, and reminders.
- Themes: Switch between Purple, Blue, Green, and Orange modes.
- Reminders: Audio and pop-up reminders for task deadlines.
- Visuals: Custom images and a welcoming design.

## Technologies Used

- Frontend: Tkinter, ttk, PIL (for image handling), tkcalendar (for date selection)
- Backend: MSSQL (via pymysql for signin/signup)
- Audio: Pygame (for reminder and checkmark sounds)
- Data Storage: JSON (for completed tasks)
- Styling: Custom CSS-like configurations with Tkinter

## Prerequisites

- Python 3.x
- Required libraries:
  - tkinter
  - ttk
  - tkcalendar
  - PIL (Pillow)
  - pygame
  - pymysql
- MSSQL server with a database named `userdata`
- MySQL credentials (default: host = localhost, user = root, password = 1234)

## Setup

1. Clone the repository:
   ```
   git clone <repo-url>
   ```

2. Install required packages:
   ```
   pip install tkcalendar Pillow pygame pymysql
   ```

3. Set up the MSSQL database:
   - Create a database named `userdata`.
   - Create a table named `data` with the following columns:
     - `username` (varchar)
     - `password` (varchar)

4. Update the database connection in `login.py` if your MSSQL credentials differ (host, user, password).

5. Run the application:
   ```
   python login.py
   ```

## Usage

- Login/Signup: Use the login page to authenticate or sign up for a new account. Reset password if needed.
- Task Management: Add tasks with deadlines and reminders, edit or sort them by category, deadline, importance, or completion status.
- Themes: Click the palette icon to switch themes.
- Reminders: Set a deadline; the app will notify you with a sound and pop-up.
                          |

## App Screenshots

### Signup Screen
![Signup](imagee/Signup.png)

### Login Screen
![Login](imagee/Login.png)

### Main Interface
![Main](imagee/main.png)

## Contributing

Feel free to fork this repository and submit pull requests. Suggestions for improvements are welcome.
