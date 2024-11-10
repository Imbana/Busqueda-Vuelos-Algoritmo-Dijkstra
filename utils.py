


from datetime import datetime, timedelta
from typing import List, Dict


def get_arrival_time(flight) -> datetime:
    return flight.departure_time + flight.duration_minutes


def calculate_waiting_times(flights) -> Dict[str, timedelta]:
    """Calcula los tiempos de espera en cada aeropuerto de conexion"""
    waiting_times = {}
    for i in range(len(flights) - 1):
        try:
            connection_airport = flights[i].destination
            wait_time = flights[i + 1].departure_time - get_arrival_time(flights[i])
            waiting_times[connection_airport] = wait_time
        except AttributeError as e:
            # En caso de que los vuelos no tengan la información necesaria
            raise ValueError(f"Error al calcular el tiempo de espera para la ruta entre. Detalles: {e}")
    
    return waiting_times


def format_flight(flight) -> str:
    weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return (f"Vuelo : {flight.origin} -> {flight.destination}\n"
            f"Día: {weekdays[flight.weekday]}\n"
            f"Salida: {flight.departure_time.strftime('%H:%M')}\n"
            f"Llegada: {get_arrival_time(flight).strftime('%H:%M')}\n"
            f"Duración: {flight.duration_minutes}")

def format_route(route) -> str:

    result = [f"Duración total: {route.total_duration}"]
    
    for i, flight in enumerate(route.flights):
        result.append(f"\n{format_flight(flight)}")

        if i < len(route.flights) - 1:
            connection_airport = flight.destination
            wait_time = route.waiting_times.get(connection_airport, timedelta(0))
            if wait_time > timedelta(0):
                days = wait_time.days
                hours = wait_time.seconds // 3600
                minutes = (wait_time.seconds % 3600) // 60
                wait_str = f"{days}d " if days else ""
                wait_str += f"{hours}h {minutes}m"
                result.append(f"Tiempo de espera en {connection_airport}: {wait_str}")
    return "\n".join(result)



def is_valid_departure_time(flight, search_date: str)-> bool:
    """Verifica si la hora de salida del vuelo es despues de la hora de busqueda"""
    
    return flight.departure_time <=   search_date
     
def is_valid_connection(flight1, 
                       flight2, 
                       min_connection_time: timedelta,
                       max_connection_time: timedelta) -> bool:
    
    """Verifica si la conexion entre dos vuelos es valida"""

    connection_time = flight2.departure_time - get_arrival_time(flight1)
    return (flight1.destination == flight2.origin and 
            min_connection_time <= connection_time <= max_connection_time)


def not_exist_connection(flight1, flight2, max_connection_time:datetime) -> bool:

    """Verifica solo si esta buscando rutas futuras fuera del rango minimo"""

    connection_time = flight2.departure_time - get_arrival_time(flight1)
    return (flight1.destination == flight2.origin and connection_time >= max_connection_time)
