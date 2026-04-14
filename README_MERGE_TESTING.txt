
Easy Ticket integrated test build

What this zip does:
- Keeps the current master project structure (django_project + easy_ticket_app)
- Brings in Isaac's implemented ticket CRUD/account features from the test branch
- Preserves the master home/search/login templates and wires them to the working ticket system

How to test locally:
1. Open a terminal in this project folder
2. Install Django if needed:
   python -m pip install django
3. Run migrations:
   python manage.py migrate
4. Start the server:
   python manage.py runserver
5. Open the local address shown in the terminal
6. On the login page, create an account with Sign Up
7. After login, verify:
   - home page loads
   - search page loads
   - create ticket works
   - ticket detail works
   - edit ticket works
   - delete ticket works
   - account page works
   - logout works

Important:
- If this works locally, upload these files to a new GitHub branch first.
- Do not upload __pycache__ files.


Styling update: Home, search, and login/signup were restyled to match the Isaac-testing visual theme more closely while preserving the master branch folder structure.
