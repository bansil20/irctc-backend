🚆 IRCTC Backend Clone

A simplified backend system inspired by IRCTC that supports user authentication, train management, booking functionality, and search analytics.
This project demonstrates backend design using Django REST Framework with MySQL for transactional data and MongoDB for logging and analytics.

🔧 Tech Stack
Python 3.x
Django
Django REST Framework
MySQL
MongoDB
JWT Authentication (SimpleJWT)
PyMongo

i also add requirments.txt get every thing that need to install with version also.

📌 Features
User Registration & Login (JWT Based)
Role-based access (Admin / User)
Train Creation & Update (Admin only)
Train Search with optional date filter
Ticket Booking with transaction safety
View user bookings
MongoDB-based search logging
Top 5 most searched routes (Analytics)

Install Python dependencies:
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install mysqlclient
pip install pymongo
pip install python-dotenv

🗄 Database Setup
MySQL
Create a database:
CREATE DATABASE irctc_db;
also i provide a .sql file just need to import in irctc_db.

MongoDB
No manual database creation required.
MongoDB will automatically create irctc_logs_db database when first search log is inserted.

Create virtual environment:
python -m venv env
env\Scripts\activate

Run migrations:
python manage.py makemigrations
python manage.py migrate

Start the server:
python manage.py runserver

Server will run at:
http://127.0.0.1:8000/

🔐 Authentication
JWT-based authentication is used.
After login, include the access token in headers:
Authorization: Bearer <access_token>
All APIs except register and login require authentication.

📡 API Flow
1️⃣ User Registration
POST /api/register/
Request:
{
  "username": "rahul",
  "email": "rahul@gmail.com",
  "password": "password123"
}
Response:
Returns access & refresh JWT tokens.

Returns access & refresh JWT tokens.

2️⃣ Login
POST /api/login/
Request:
{
  "email": "rahul@gmail.com",
  "password": "password123"
}
Response:
Returns JWT tokens.
Use access token in headers for further APIs.

🚆 Train APIs
3️⃣ Create Train (Admin Only)
POST /api/trains/
Admin users only.
Creates train with:
Train number
Name
Source
Destination
Departure & Arrival time
Total seats
Available seats

4️⃣ Update Train (Admin Only)
PUT /api/trains/<id>/
Only admin can modify train details.

5️⃣ Search Train
GET /api/trains/search/?source=Delhi&destination=Mumbai&date=2026-02-25
Features:
Case-insensitive matching
Optional date filter
Logs every search in MongoDB
Stores execution time for analytics
MongoDB log example:
{
  "endpoint": "/api/trains/search/",
  "user_id": 3,
  "params": {
    "source": "Delhi",
    "destination": "Mumbai"
  },
  "execution_time_ms": 15.23
}

🎟 Booking APIs
6️⃣ Book Ticket
POST /api/bookings/
Request:
{
  "train": 3,
  "seats_booked": 2
}
Booking logic:
Validates seats > 0
Locks train row (select_for_update)
Checks seat availability
Deducts seats
Creates booking
Uses transaction.atomic to prevent partial updates
Prevents race conditions.

7️⃣ View My Bookings
GET /api/bookings/my/
Returns:
[
  {
    "id": 1,
    "seats_booked": 2,
    "booking_time": "...",
    "train": {
      "train_number": "12345",
      "source": "Delhi",
      "destination": "Mumbai"
    }
  }
]

📊 Analytics API (MongoDB)
8️⃣ Top 5 Most Searched Routes
GET /api/analytics/top-routes/
Uses MongoDB aggregation pipeline:
Groups by source & destination
Counts occurrences
Sorts descending
Returns top 5
Example Response:
[
  {
    "source": "Delhi",
    "destination": "Mumbai",
    "search_count": 12
  }
]

If no searches exist:
{
  "message": "No search data available"
}



📂 Project Structure Overview
accounts/   → Authentication & custom user model
trains/     → Train management & search
bookings/   → Ticket booking logic
analytics/  → MongoDB logging & aggregation
