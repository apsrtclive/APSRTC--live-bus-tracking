import sqlite3
import os

def insert_data():
    db_path = 'instance/apsrtc_local.db'
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return
        
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check if already added
    c.execute("SELECT * FROM routes WHERE route_name='RK Beach → Gajuwaka'")
    if c.fetchone():
        print("Data already seeded.")
        return
        
    print("Seeding SQLite DB directly...")
    
    # Insert Routes
    c.execute("INSERT INTO routes (route_name, from_station, to_station) VALUES (?, ?, ?)", 
              ('RK Beach → Gajuwaka', 'RK Beach', 'Gajuwaka'))
    r4_id = c.lastrowid
    
    c.execute("INSERT INTO routes (route_name, from_station, to_station) VALUES (?, ?, ?)", 
              ('NAD Junction → Maddilapalem', 'NAD Junction', 'Maddilapalem'))
    r5_id = c.lastrowid
    
    c.execute("INSERT INTO routes (route_name, from_station, to_station) VALUES (?, ?, ?)", 
              ('Siripuram → RTC Complex', 'Siripuram', 'RTC Complex'))
    r6_id = c.lastrowid
    
    # Insert Services
    c.execute("INSERT INTO services (service_no, route_id, service_type, ticket_price) VALUES (?, ?, ?, ?)",
              ('500', r4_id, 'Metro Ex', 40))
    s4_id = c.lastrowid
    
    c.execute("INSERT INTO services (service_no, route_id, service_type, ticket_price) VALUES (?, ?, ?, ?)",
              ('38Y', r5_id, 'Express', 25))
    s5_id = c.lastrowid
    
    c.execute("INSERT INTO services (service_no, route_id, service_type, ticket_price) VALUES (?, ?, ?, ?)",
              ('10K', r6_id, 'City Ordinary', 15))
    s6_id = c.lastrowid
    
    # Insert Vehicles
    c.executemany("INSERT INTO vehicles (vehicle_no, service_id, status) VALUES (?, ?, ?)", [
        ('AP31 GH 2021', s4_id, 'Running'),
        ('AP31 IJ 3032', s5_id, 'Running'),
        ('AP31 KL 4043', s6_id, 'Running')
    ])
    
    # Insert Stops
    stops_r4 = [
        (r4_id, 'RK Beach', 17.7145, 83.3235, 1),
        (r4_id, 'Siripuram', 17.7262, 83.3151, 2),
        (r4_id, 'RTC Complex', 17.7282, 83.3001, 3),
        (r4_id, 'Gajuwaka', 17.6908, 83.2185, 4)
    ]
    stops_r5 = [
        (r5_id, 'NAD Junction', 17.7493, 83.2505, 1),
        (r5_id, 'Kancharapalem', 17.7370, 83.2750, 2),
        (r5_id, 'Maddilapalem', 17.7350, 83.3130, 3)
    ]
    stops_r6 = [
        (r6_id, 'Siripuram', 17.7262, 83.3151, 1),
        (r6_id, 'Dutt Island', 17.7275, 83.3080, 2),
        (r6_id, 'RTC Complex', 17.7282, 83.3001, 3)
    ]
    
    # Add stops and get IDs for timetable
    def add_stops(stop_list, s_id):
        tt_stops = []
        for stop in stop_list:
            c.execute("INSERT INTO stops (route_id, stop_name, lat, lng, stop_order) VALUES (?, ?, ?, ?, ?)", stop)
            tt_stops.append(c.lastrowid)
        return tt_stops
        
    tt_r4 = add_stops(stops_r4, s4_id)
    tt_r5 = add_stops(stops_r5, s5_id)
    tt_r6 = add_stops(stops_r6, s6_id)
    
    # Insert Timetable
    times_r4 = ['08:00', '08:10', '08:25', '08:50']
    for st_id, tm in zip(tt_r4, times_r4):
        c.execute("INSERT INTO timetable (service_id, stop_id, arrival_time) VALUES (?, ?, ?)", (s4_id, st_id, tm))
        
    times_r5 = ['09:00', '09:15', '09:30']
    for st_id, tm in zip(tt_r5, times_r5):
        c.execute("INSERT INTO timetable (service_id, stop_id, arrival_time) VALUES (?, ?, ?)", (s5_id, st_id, tm))
        
    times_r6 = ['10:00', '10:05', '10:15']
    for st_id, tm in zip(tt_r6, times_r6):
        c.execute("INSERT INTO timetable (service_id, stop_id, arrival_time) VALUES (?, ?, ?)", (s6_id, st_id, tm))
        
    conn.commit()
    conn.close()
    print("Seed complete via pure sqlite3!")

if __name__ == '__main__':
    insert_data()
