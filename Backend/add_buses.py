import os
from flask import Flask
from models import db, Route, Service, Vehicle, Stop, TimetableEntry

def create_app():
    app = Flask(__name__)
    _db_url = os.getenv('DATABASE_URL', '')
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    if not _db_url:
        _db_url = 'sqlite:///apsrtc_local.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = _db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def seed_new_buses():
    app = create_app()
    with app.app_context():
        # Check if they are already added
        if Route.query.filter_by(route_name='RK Beach → Gajuwaka').first():
            print("New buses already seeded.")
            return

        print("Adding 3 new realistic buses...")

        # 1. RK Beach to Gajuwaka
        r4 = Route(route_name='RK Beach → Gajuwaka', from_station='RK Beach', to_station='Gajuwaka')
        # 2. NAD Junction to Maddilapalem
        r5 = Route(route_name='NAD Junction → Maddilapalem', from_station='NAD Junction', to_station='Maddilapalem')
        # 3. Siripuram to RTC Complex
        r6 = Route(route_name='Siripuram → RTC Complex', from_station='Siripuram', to_station='RTC Complex')
        
        db.session.add_all([r4, r5, r6])
        db.session.commit()

        # Services
        s4 = Service(service_no='500', route_id=r4.route_id, service_type='Metro Ex', ticket_price=40)
        s5 = Service(service_no='38Y', route_id=r5.route_id, service_type='Express', ticket_price=25)
        s6 = Service(service_no='10K', route_id=r6.route_id, service_type='City Ordinary', ticket_price=15)
        
        db.session.add_all([s4, s5, s6])
        db.session.commit()

        # Vehicles
        v4 = Vehicle(vehicle_no='AP31 GH 2021', service_id=s4.service_id, status='Running')
        v5 = Vehicle(vehicle_no='AP31 IJ 3032', service_id=s5.service_id, status='Running')
        v6 = Vehicle(vehicle_no='AP31 KL 4043', service_id=s6.service_id, status='Running')
        
        db.session.add_all([v4, v5, v6])
        db.session.commit()

        # Stops for Route 4 (RK Beach -> Gajuwaka)
        # Assuming coordinates roughly based in Visakhapatnam
        st4_1 = Stop(route_id=r4.route_id, stop_name='RK Beach', lat=17.7145, lng=83.3235, stop_order=1)
        st4_2 = Stop(route_id=r4.route_id, stop_name='Siripuram', lat=17.7262, lng=83.3151, stop_order=2)
        st4_3 = Stop(route_id=r4.route_id, stop_name='RTC Complex', lat=17.7282, lng=83.3001, stop_order=3)
        st4_4 = Stop(route_id=r4.route_id, stop_name='Gajuwaka', lat=17.6908, lng=83.2185, stop_order=4)

        # Stops for Route 5 (NAD Junction -> Maddilapalem)
        st5_1 = Stop(route_id=r5.route_id, stop_name='NAD Junction', lat=17.7493, lng=83.2505, stop_order=1)
        st5_2 = Stop(route_id=r5.route_id, stop_name='Kancharapalem', lat=17.7370, lng=83.2750, stop_order=2)
        st5_3 = Stop(route_id=r5.route_id, stop_name='Maddilapalem', lat=17.7350, lng=83.3130, stop_order=3)

        # Stops for Route 6 (Siripuram -> RTC Complex)
        st6_1 = Stop(route_id=r6.route_id, stop_name='Siripuram', lat=17.7262, lng=83.3151, stop_order=1)
        st6_2 = Stop(route_id=r6.route_id, stop_name='Dutt Island', lat=17.7275, lng=83.3080, stop_order=2)
        st6_3 = Stop(route_id=r6.route_id, stop_name='RTC Complex', lat=17.7282, lng=83.3001, stop_order=3)

        db.session.add_all([st4_1, st4_2, st4_3, st4_4, st5_1, st5_2, st5_3, st6_1, st6_2, st6_3])
        db.session.commit()

        # Timetable Entries
        # Route 4
        tt1 = TimetableEntry(service_id=s4.service_id, stop_id=st4_1.stop_id, arrival_time='08:00')
        tt2 = TimetableEntry(service_id=s4.service_id, stop_id=st4_2.stop_id, arrival_time='08:10')
        tt3 = TimetableEntry(service_id=s4.service_id, stop_id=st4_3.stop_id, arrival_time='08:25')
        tt4 = TimetableEntry(service_id=s4.service_id, stop_id=st4_4.stop_id, arrival_time='08:50')

        # Route 5
        tt5 = TimetableEntry(service_id=s5.service_id, stop_id=st5_1.stop_id, arrival_time='09:00')
        tt6 = TimetableEntry(service_id=s5.service_id, stop_id=st5_2.stop_id, arrival_time='09:15')
        tt7 = TimetableEntry(service_id=s5.service_id, stop_id=st5_3.stop_id, arrival_time='09:30')

        # Route 6
        tt8 = TimetableEntry(service_id=s6.service_id, stop_id=st6_1.stop_id, arrival_time='10:00')
        tt9 = TimetableEntry(service_id=s6.service_id, stop_id=st6_2.stop_id, arrival_time='10:05')
        tt10 = TimetableEntry(service_id=s6.service_id, stop_id=st6_3.stop_id, arrival_time='10:15')

        db.session.add_all([tt1, tt2, tt3, tt4, tt5, tt6, tt7, tt8, tt9, tt10])
        db.session.commit()

        print("Successfully added 3 new buses!")

if __name__ == '__main__':
    seed_new_buses()
