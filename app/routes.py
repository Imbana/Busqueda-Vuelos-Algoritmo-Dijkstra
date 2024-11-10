from flask import Blueprint, render_template, request, jsonify

from datetime import datetime, timedelta

from main import busqueda_total_rutas_validas


main_bp = Blueprint('main', __name__)

main_bp = Blueprint('main', __name__)


CITIES = [
    {'code': 'BOG', 'name': 'Bogotá', 'country': 'Colombia'},
    {'code': 'CLO', 'name': 'Cali', 'country': 'Colombia'},
    {'code': 'MDE', 'name': 'Medellín', 'country': 'Colombia'},
    {'code': 'CTG', 'name': 'Cartagena', 'country': 'Colombia'},
    {'code': 'BGA', 'name': 'Bucaramanga', 'country': 'Colombia'},
    {'code': 'SMR', 'name': 'Santa Marta', 'country': 'Colombia'}
]

@main_bp.route('/')
def index():
    return render_template('index.html', cities=CITIES)



@main_bp.route('/search-flights', methods=['POST'])
def search_flights():
    data = request.json

    date_str = data.get('date')
    WEEKDAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    fecha_dada = datetime.strptime(date_str, "%Y-%m-%d").date()
    fecha_actual = datetime.now().date()

    if fecha_dada == fecha_actual:
        search_date = datetime.now()
    else:
        search_date = datetime.combine(fecha_dada, datetime.min.time())

    origin_airport_code = data.get('origin')  #  origen
    destination_airport_code = data.get('destination')  # destino
    min_connection_interval: timedelta = timedelta(minutes=40)  # Tiempo mínimo 
    max_connection_interval: timedelta = timedelta(hours=13) # Tiempo máximo 
        
    try:

        # Busqueda de todas las rutas posibles
        total_routes = busqueda_total_rutas_validas(
            origin_airport_code,
            destination_airport_code,
            search_date,
            min_connection_interval,
            max_connection_interval
        ) 


        # Convertir resultados a formato JSON
        flights_data = []
        for route in total_routes:
            list_flights = route.flights
            print(list_flights)
 
            total_segundos = int(route.total_duration.total_seconds())
            horas = total_segundos // 3600
            minutos = (total_segundos % 3600) // 60




            flights_data.append({
                'departure_time': list_flights[0].departure_time.strftime('%I:%M %p') +  " - " + list_flights[0].origin,
                'arrival_time': (list_flights[-1].departure_time + list_flights[-1].duration_minutes).strftime('%I:%M %p') +  " - " + list_flights[-1].destination ,
                'duration': f"{horas}h {minutos}m",
                'price': f"{(len(list_flights) *99.99):.2f}",
                'tags': ['primero'] ,
                'stops': f"{'Directo' if len(list_flights) == 1 else  str(len(list_flights)-1)+' Paradas' }",
                'operator': "Punto Pago",
                'routes': [ {
                    "origin": flight.origin , 
                    "destination": flight.destination , 
                    "arrival_time": (flight.departure_time + flight.duration_minutes).strftime('%I:%M %p'), 
                    "departure_time": flight.departure_time.strftime('%I:%M %p'), 
                    "duration_minutes": str(flight.duration_minutes),
                    "weekdays": WEEKDAYS[flight.weekday],
                    "wait_time":  str((route.waiting_times.get(flight.destination, timedelta(0)).seconds // 3600)) + "h "  + str((route.waiting_times.get(flight.destination, timedelta(0)).seconds % 3600) // 60 ) + "m",
                    } for flight in list_flights],
                    
            })

        return jsonify({
            'status': 'success',
            'flights': flights_data
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400