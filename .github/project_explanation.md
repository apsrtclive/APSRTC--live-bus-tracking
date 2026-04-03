# 🚍 APSRTC Live Bus Tracking — Complete Project Explanation

> **Final Year Project** | Built for Visakhapatnam (Vizag) City Commuters  
> **Live Demo**: [https://apsrtc-vizag.onrender.com](https://apsrtc-vizag.onrender.com)

---

## 🧠 What Does This Project Do?

This is a **Real-Time Bus Tracking Web Application** for APSRTC (Andhra Pradesh State Road Transport Corporation) buses operating in Visakhapatnam city.

It has **two types of users**:
1. **Commuters (Passengers)** — Open the website, search for a bus route, track it live on a map, and check timetables.
2. **Drivers** — Open the driver portal on their phone, log in, and tap "Start Tracking" to share their GPS location with the server in real time.

---

## 📂 Complete Project Structure (Every File Explained)

```
APSRTC--live-bus-tracking/
│
├── 📄 README.md              ← Project overview & setup guide
├── 📄 DEPLOY.md              ← Step-by-step guide to deploy on Render.com
├── 📄 requirements.txt       ← All Python libraries the project needs
├── 📄 runtime.txt            ← Tells Render which Python version to use
├── 📄 .gitignore             ← Files Git should NOT upload (e.g., .env, database)
│
├── 📁 .github/
│   └── 📁 workflows/         ← GitHub Actions (CI/CD automation, if any)
│
└── 📁 Backend/               ← Everything that runs on the SERVER
    ├── 📄 backend.py         ← MAIN FILE: The entire Flask web server
    ├── 📄 models.py          ← Database table definitions (the schema)
    ├── 📄 init_db.py         ← Script to create DB tables & insert sample data
    ├── 📄 Procfile           ← Tells Render how to START the app
    ├── 📄 optimize_db.py     ← Adds database indexes for faster queries
    ├── 📄 run_migration.py   ← Updates DB structure without deleting data
    ├── 📄 check_db_schema.py ← Utility to verify DB table structure
    ├── 📄 fix_db_close.py    ← Fixes a specific database connection bug
    ├── 📄 update_coords.py   ← Script to update GPS coordinates in DB
    ├── 📄 test_password.py   ← Testing script for password hashing
    ├── 📄 err.log / error.txt← Error log files (debugging records)
    ├── 📄 startup.sh         ← Shell script to start the app on Linux servers
    ├── 📄 pyrightconfig.json ← Python type-checker configuration
    │
    ├── 📁 templates/         ← HTML pages (the visual part)
    │   ├── 📄 index.html         ← 🏠 Main commuter dashboard page
    │   ├── 📄 user_login.html    ← 👤 User login & registration page
    │   ├── 📄 driver.html        ← 🚌 Driver dashboard (GPS tracking)
    │   └── 📄 driver_login.html  ← 🔑 Driver login & registration page
    │
    └── 📁 static/            ← CSS, JS, Images (sent directly to browser)
        ├── 📄 style.css          ← All custom styling (glassmorphism, animations)
        ├── 📄 main_bundle.js     ← All JavaScript logic (map, API calls, etc.)
        └── 📁 images/            ← Image assets used in the app
```

---

## 🛠️ Technology Stack (What Tools Were Used & Why)

| Layer | Technology | Why It Was Chosen |
|---|---|---|
| **Backend Language** | Python | Easy to learn, powerful for web servers |
| **Web Framework** | Flask | Lightweight Python framework, perfect for projects |
| **Database** | PostgreSQL (via SQLAlchemy) | Reliable, cloud-compatible SQL database |
| **Map Library** | Leaflet.js | Free, open-source interactive maps |
| **Map Tiles** | OpenStreetMap | Free map data (no API key needed) |
| **Frontend CSS** | Bootstrap 5 + Custom CSS | Ready-made responsive components |
| **Deployment** | Render.com | Free cloud hosting for Python apps |
| **Security** | Flask-Talisman, Flask-Limiter, Werkzeug | Protects against attacks |

---

## 🗄️ Database Design — `models.py` (The Heart of the Data)

This file defines **all the database tables** using Python classes (called ORM models). Think of each class as one table in the database.

### Table Relationships Diagram
```
Route (routes)
 └──► Service (services)  [A route has many services/bus numbers]
       └──► Vehicle (vehicles)  [A service runs on a vehicle/bus]
             └──► LiveLocation (live_location)  [A bus has one live GPS location]
 └──► Stop (stops)  [A route has many stops]
       └──► TimetableEntry (timetable)  [Each stop has arrival times per service]

Driver (drivers)  [Separate table for driver login accounts]
User (users)      [Separate table for passenger login accounts]
```

### Table-by-Table Explanation

#### 1. `Route` — Bus Routes
```
route_id   | route_name              | from_station | to_station
1          | Gajuwaka → Beach Road   | Gajuwaka     | Beach Road
2          | Maddilapalem → Simhac.. | Maddilapalem | Simhachalam
```
Stores the **path** a bus travels — from where to where.

#### 2. `Service` — Bus Service Numbers
```
service_id | service_no | route_id | service_type | ticket_price
1          | 28A        | 1        | Express      | 30
2          | 6K         | 2        | Metro        | 20
```
A **service** is like a specific bus number (e.g., "28A"). It runs on a route and has a type (Express/Metro/Deluxe) and ticket price.

#### 3. `Vehicle` — Physical Buses
```
vehicle_id | vehicle_no      | service_id | status
1          | AP31 AB 1234    | 1          | Running
```
Each physical **bus** (identified by registration number like `AP31 AB 1234`) is linked to a service.

#### 4. `Stop` — Bus Stops on a Route
```
stop_id | route_id | stop_name    | lat   | lng   | stop_order
1       | 1        | Gajuwaka     | 17.72 | 83.30 | 1
2       | 1        | Maddilapalem | 17.73 | 83.31 | 2
3       | 1        | Beach Road   | 17.75 | 83.33 | 3
```
Each **stop** has GPS coordinates (lat/lng) so it can be pinned on the map.

#### 5. `TimetableEntry` — Scheduled Arrival Times
```
time_id | service_id | stop_id | arrival_time
1       | 1 (28A)    | 1       | 10:00
2       | 1 (28A)    | 2       | 10:20
3       | 1 (28A)    | 3       | 10:45
```
Tells commuters when bus "28A" will reach each stop.

#### 6. `LiveLocation` — Real-Time GPS Data ⭐ (The Key Innovation)
```
bus_id | lat     | lng     | speed | updated_at
1      | 17.731  | 83.305  | 35    | 2025-04-01 14:30:00
```
This table is updated **every few seconds** when a driver is tracking. The passenger's browser reads this to show the moving bus on the map.

#### 7. `Driver` — Driver Accounts
```
id | username | password (hashed)
1  | driver01 | pbkdf2:sha256:...
```

#### 8. `User` — Passenger Accounts
```
id | username | password (hashed)
1  | abhiram  | pbkdf2:sha256:...
```

---

## ⚙️ Backend Server — `backend.py` (The Brain)

This is the **most important file** — it contains all the server logic. It runs 24/7 on the cloud and responds to every request from browsers.

### How Flask Works (Simply Explained)
```
Browser (User's phone)  →  Sends Request  →  backend.py  →  Checks DB  →  Sends Response
```

### All API Endpoints (URLs the server handles)

#### 🔐 Authentication (Login/Registration)
| URL | Method | Who Uses It | What It Does |
|---|---|---|---|
| `/` | GET | Commuter | Shows main dashboard (redirects to login if not logged in) |
| `/login` | GET | Commuter | Shows the login page |
| `/api/user/register` | POST | Commuter | Creates a new account (limited to 3 times/hour) |
| `/api/user/login` | POST | Commuter | Checks username+password, creates a session |
| `/api/user/logout` | POST | Commuter | Clears session, logs out |
| `/driver/login` | GET | Driver | Shows driver login page |
| `/api/driver/register` | POST | Driver | Creates driver account |
| `/api/driver/login` | POST | Driver | Driver login |
| `/driver` | GET | Driver | Shows driver GPS dashboard |

#### 🔍 Bus Search & Info
| URL | Method | What It Does |
|---|---|---|
| `/api/search?from=X&to=Y` | GET | Finds all buses between two stations |
| `/api/service/<service_no>` | GET | Gets details of one service (e.g., "28A") |
| `/api/vehicle/<vehicle_no>` | GET | Gets details of one bus by registration number |
| `/api/timetable?from=X&to=Y` | GET | Gets scheduled arrival times |
| `/api/route_details/<service_no>` | GET | Gets all stops of a route with GPS coordinates |
| `/api/routes` | GET | Lists all routes (cached for 10 min) |
| `/api/stations` | GET | Lists all station names (for search autocomplete) |

#### 📍 Live Tracking (The Core Feature)
| URL | Method | What It Does |
|---|---|---|
| `/api/update_location` | POST | **Driver sends GPS** → server saves to DB |
| `/api/live/<service_no>` | GET | **Passenger reads GPS** ← server sends latest location |
| `/api/eta/<service_no>` | GET | Calculates estimated time of arrival |

#### 📊 Dashboard & Admin
| URL | Method | What It Does |
|---|---|---|
| `/api/dashboard` | GET | Returns total routes, services, vehicles, running buses |
| `/api/admin/add_route` | POST | Adds a new route |
| `/api/admin/add_service` | POST | Adds a new service |
| `/api/admin/add_vehicle` | POST | Adds a new vehicle |
| `/api/debug` | GET | Shows last 20 server log entries (for debugging) |

### 🔒 Security Features in backend.py
- **Rate Limiting**: Registration is limited to 3 attempts/hour, login to 10/min — prevents hackers from trying millions of passwords
- **Password Hashing**: Passwords are never stored as plain text — stored as a scrambled hash using `werkzeug`
- **Session Management**: Login sessions expire after 7 days (or on logout)
- **Flask-Talisman**: Adds security headers to every HTTP response
- **Parameterized Queries (via SQLAlchemy)**: Prevents SQL Injection attacks
- **CORS**: Allows the browser (different origin) to communicate with the API

---

## 📁 Database Setup — `init_db.py`

This script is run **once** when deploying to a new server. It:
1. Creates all the database tables (routes, services, vehicles, stops, timetable, etc.)
2. Inserts **sample data** for testing:
   - 3 routes (Gajuwaka→Beach Road, Maddilapalem→Simhachalam, RTC Complex→Railway Station)
   - 3 services (28A, 6K, 400K)
   - 3 vehicles with real registration number formats
   - Stop coordinates on the Vizag map
   - Sample timetable entries

---

## 🖥️ Frontend Pages — `templates/` folder

Flask uses **Jinja2 templating** — these are HTML files with some Python-like variables.

### 1. `index.html` — Main Commuter Dashboard
This is what passengers see after logging in. It has 3 sections:
- **🎫 Find Bus** — Search boxes for "From" and "To" stations + service type filter
- **📡 Live Tracking** — Input a service number and see it on a map
- **🗺️ Explore Routes** — Load all available routes
- Has a **sticky bottom navigation bar** for mobile phones
- Has a **time-based greeting** ("Good morning!", "Good evening!")
- Has **Google Analytics** tracking (ID: G-R3EQ517P1S) to see how many people visit

### 2. `user_login.html` — Passenger Login Page
- Login form with "Remember Me" checkbox
- Registration form (toggle between login/register)
- Glassmorphism design with a Vizag background

### 3. `driver.html` — Driver Dashboard
- Mobile-first UI (designed for use on a phone while driving)
- **Start Tracking** / **Stop Tracking** button
- Reads GPS from the browser's built-in `navigator.geolocation` API
- Sends GPS coordinates to `/api/update_location` every 5 seconds
- Shows visual indicator (green/red) for active/inactive status

### 4. `driver_login.html` — Driver Login Page
- Separate login portal for drivers

---

## 📦 Static Files — `static/` folder

### `style.css` — All Styling (12 KB)
Contains all the custom CSS for the entire website:
- Glassmorphism card effect (blurred, semi-transparent cards)
- Color variables (primary, secondary, gradient)
- Sticky bottom navigation for mobile
- Fade-in animations
- Responsive design for phones & desktops

### `main_bundle.js` — All JavaScript (27 KB)
This is the biggest front-end file. It contains:
- **Map initialization** (using Leaflet.js + OpenStreetMap)
- **Bus marker** that moves on the map when tracking
- **API call functions** (fetch calls to all the backend endpoints)
- **Search functionality** — sends search requests, renders results
- **Timetable display** logic
- **Toast notifications** (small popup messages like "Bus found!")
- **Station autocomplete** (loads all station names for search dropdown)

---

## 🚀 Deployment Files

### `requirements.txt` — Python Dependencies
```
flask==3.0.0          ← Web framework
flask-cors==4.0.0     ← Allow browser to talk to server
gunicorn==21.2.0      ← Production-grade web server (not Flask's built-in)
python-dotenv         ← Load .env secrets file
flask-talisman        ← Security headers
flask-limiter         ← Rate limiting
flask-caching==2.1.0  ← Caching to reduce DB load
Flask-SQLAlchemy==3.1.1 ← Database ORM
psycopg2-binary==2.9.9  ← PostgreSQL adapter for Python
```

### `Procfile` — How Render Starts the App
```bash
web: gunicorn Backend.backend:app --workers 4 --threads 2 --worker-class gthread --timeout 120 --preload --log-level info
```
- `gunicorn` = production web server (like a more powerful version of Flask's dev server)
- `--workers 4` = handle 4 simultaneous requests
- `--threads 2` = each worker can handle 2 threads
- `--timeout 120` = a request can take up to 120 seconds

### `runtime.txt`
Specifies which Python version Render should use (e.g., `python-3.11.x`).

### `DEPLOY.md` — Deployment Guide
Step-by-step instructions to:
1. Push code to GitHub
2. Create a Render.com account
3. Connect the GitHub repo
4. Configure build settings
5. Initialize the database

---

## 🔄 How the Live Tracking Works (End-to-End Flow)

```
1. DRIVER opens /driver on their phone
2. DRIVER clicks "Start Tracking"
3. Browser asks "Allow location access?" → Driver clicks Allow
4. Every 5 seconds: JavaScript reads GPS → sends POST to /api/update_location
5. SERVER receives { service_no, lat, lng, speed }
6. SERVER updates the LiveLocation table in PostgreSQL
7. ─────────────────────────────────────────────────────
8. PASSENGER opens /  and types "28A" in the Track box
9. JavaScript sends GET to /api/live/28A
10. SERVER reads LiveLocation table → returns { lat, lng, speed }
11. JavaScript moves the bus marker on the Leaflet map to the new position
12. Steps 9-11 repeat every 5 seconds (polling)
```

---

## 📊 Current Project Status

### ✅ What Is Complete
- [x] Full backend with all APIs (search, tracking, timetable, ETA, dashboard)
- [x] PostgreSQL database with proper schema and sample data
- [x] User authentication (register, login, logout, sessions)
- [x] Driver authentication (separate portal)
- [x] Real-time GPS location update from driver
- [x] Live map tracking for commuters (Leaflet.js)
- [x] Bus search by route (from/to stations)
- [x] Timetable lookup
- [x] Route stop details with GPS pins on map
- [x] ETA calculation (basic: based on speed and distance)
- [x] Mobile-friendly responsive design
- [x] Glassmorphism UI design
- [x] Security: Rate limiting, password hashing, secure sessions
- [x] Caching (routes and stations cached for 10 minutes to reduce DB load)
- [x] Deployed live on Render.com
- [x] Google Analytics integrated
- [x] GitHub repository connected

### ⚠️ What Could Be Improved (For Viva / Enhancement)
- [ ] **ETA is hardcoded** — `distance = 5` km is fixed, should calculate real remaining distance from bus position to destination
- [ ] **Admin panel** — No web UI to add routes/services (currently requires API calls directly)
- [ ] **No WebSocket** — Currently uses polling (checks every 5 sec), WebSocket would be smoother
- [ ] **Driver-service linking** — Drivers aren't linked to specific services in the DB; any driver can update any service
- [ ] **Map stops display** — Route stops should be displayed on map when tracking
- [ ] **Notification system** — "Bus is 2 stops away" push notification
- [ ] **Offline support** — PWA (Progressive Web App) for offline access

---

## 💡 Key Concepts to Explain in Your Viva

### 1. What is REST API?
Your backend exposes **REST APIs** — URLs that other programs (your frontend JS) can call to get or send data. Example:
- `GET /api/search?from=Gajuwaka&to=Beach+Road` → returns list of buses in JSON format

### 2. What is ORM (Object Relational Mapping)?
Instead of writing raw SQL like `SELECT * FROM routes`, you write Python like `Route.query.all()`. SQLAlchemy converts it to SQL automatically.

### 3. What is Session?
When a user logs in, the server creates a **session** — a small encrypted cookie stored in the browser. Every future request carries this cookie so the server knows you're still logged in.

### 4. What is Gunicorn?
Flask's built-in server handles only 1 request at a time. Gunicorn is a production server that handles multiple requests simultaneously using multiple workers.

### 5. What is Caching?
Some data (like the list of all routes) doesn't change often. Instead of querying the database every time, the server remembers the result for 10 minutes and returns it instantly. This reduces database load.

---

*Made with ❤️ for Vizag Commuters — Final Year Project*
