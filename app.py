from flask import Flask, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Mock data (replace with database later)
tickets = [
    {
        "id": 1,
        "title": "Computer not turning on",
        "description": "Power button does nothing",
        "created_at": datetime(2026, 3, 28, 10, 30)
    },
    {
        "id": 2,
        "title": "WiFi not working",
        "description": "Cannot connect to network",
        "created_at": datetime(2026, 3, 29, 9, 15)
    },
    {
        "id": 3,
        "title": "Blue screen error",
        "description": "System crashes randomly",
        "created_at": datetime(2026, 3, 27, 14, 5)
    }
]


@app.route("/")
def home():
    # Sort tickets by newest first
    sorted_tickets = sorted(tickets, key=lambda x: x["created_at"], reverse=True)
    return render_template("home.html", tickets=sorted_tickets)


@app.route("/search")
def search():
    return "<h2>Search Page (to be implemented)</h2>"


@app.route("/tickets")
def view_tickets():
    return "<h2>All Tickets Page (to be implemented)</h2>"


if __name__ == "__main__":
    app.run(debug=True)
