
from datetime import datetime, timedelta
from typing import List, Dict, NamedTuple

from utils import get_arrival_time, is_valid_connection, not_exist_connection




# Diccionario de vuelos
# Cada vuelo está representado por un diccionario con los siguientes campos:
# - "origin": código del aeropuerto de origen (por ejemplo, "BOG" para Bogotá)
# - "destination": código del aeropuerto de destino (por ejemplo, "BGA" para Bucaramanga)
# - "departure_time": hora de salida en formato HH:MM
# - "duration_minutes": duración del vuelo en minutos
# - "weekday": día de la semana en que el vuelo opera (Lunes = 0, Martes = 1, ..., Domingo = 6)


weekly_flight_routes = [
    # Rutas Lunes
    {"origin": "BOG", "destination": "MDE", "departure_time": "05:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "MDE", "departure_time": "15:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "SMR", "departure_time": "07:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "SMR", "departure_time": "16:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "CTG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "CTG", "departure_time": "18:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "CLO", "departure_time": "07:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "CLO", "departure_time": "22:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "EOH", "departure_time": "09:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BOG", "destination": "EOH", "departure_time": "14:50", "duration_minutes": 69, "weekday": 0},
  
    {"origin": "MDE", "destination": "BOG", "departure_time": "07:29", "duration_minutes": 69, "weekday": 0},
    {"origin": "BAQ", "destination": "BOG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "BGA", "destination": "BOG", "departure_time": "12:29", "duration_minutes": 69, "weekday": 0},
    {"origin": "SMR", "destination": "BOG", "departure_time": "13:50", "duration_minutes": 69, "weekday": 0},
    {"origin": "CTG", "destination": "BOG", "departure_time": "08:29", "duration_minutes": 69, "weekday": 0},
    {"origin": "CLO", "destination": "BOG", "departure_time": "06:29", "duration_minutes": 69, "weekday": 0},
    {"origin": "EOH", "destination": "BOG", "departure_time": "18:29", "duration_minutes": 69, "weekday": 0},

    # # Rutas Martes
    {"origin": "BOG", "destination": "MDE", "departure_time": "05:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "MDE", "departure_time": "15:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "SMR", "departure_time": "07:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "SMR", "departure_time": "16:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "CTG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "CTG", "departure_time": "18:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "CLO", "departure_time": "07:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "CLO", "departure_time": "22:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "EOH", "departure_time": "09:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BOG", "destination": "EOH", "departure_time": "14:50", "duration_minutes": 69, "weekday": 1},
  
    {"origin": "MDE", "destination": "BOG", "departure_time": "07:29", "duration_minutes": 69, "weekday": 1},
    {"origin": "BAQ", "destination": "BOG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "BGA", "destination": "BOG", "departure_time": "12:29", "duration_minutes": 69, "weekday": 1},
    {"origin": "SMR", "destination": "BOG", "departure_time": "13:50", "duration_minutes": 69, "weekday": 1},
    {"origin": "CTG", "destination": "BOG", "departure_time": "08:29", "duration_minutes": 69, "weekday": 1},
    {"origin": "CLO", "destination": "BOG", "departure_time": "06:29", "duration_minutes": 69, "weekday": 1},
    {"origin": "EOH", "destination": "BOG", "departure_time": "18:29", "duration_minutes": 69, "weekday": 1},
    {"origin": "CLO", "destination": "BGA", "departure_time": "08:29", "duration_minutes": 69, "weekday": 1},

    # # Rutas Miércoles
    {"origin": "BOG", "destination": "MDE", "departure_time": "05:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "MDE", "departure_time": "15:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "SMR", "departure_time": "07:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "SMR", "departure_time": "16:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "CTG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "CTG", "departure_time": "18:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "CLO", "departure_time": "07:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "CLO", "departure_time": "22:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "EOH", "departure_time": "09:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BOG", "destination": "EOH", "departure_time": "14:50", "duration_minutes": 69, "weekday": 2},
  
    {"origin": "MDE", "destination": "BOG", "departure_time": "07:29", "duration_minutes": 69, "weekday": 2},
    {"origin": "BAQ", "destination": "BOG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "BGA", "destination": "BOG", "departure_time": "12:29", "duration_minutes": 69, "weekday": 2},
    {"origin": "SMR", "destination": "BOG", "departure_time": "13:50", "duration_minutes": 69, "weekday": 2},
    {"origin": "CTG", "destination": "BOG", "departure_time": "08:29", "duration_minutes": 69, "weekday": 2},
    {"origin": "CLO", "destination": "BOG", "departure_time": "06:29", "duration_minutes": 69, "weekday": 2},
    {"origin": "EOH", "destination": "BOG", "departure_time": "18:29", "duration_minutes": 69, "weekday": 2},

    # # Rutas Jueves
    {"origin": "BOG", "destination": "MDE", "departure_time": "05:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "MDE", "departure_time": "15:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "SMR", "departure_time": "07:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "SMR", "departure_time": "16:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "CTG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "CTG", "departure_time": "18:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "CLO", "departure_time": "07:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "CLO", "departure_time": "22:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "EOH", "departure_time": "09:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BOG", "destination": "EOH", "departure_time": "14:50", "duration_minutes": 69, "weekday": 3},

    {"origin": "MDE", "destination": "BOG", "departure_time": "07:29", "duration_minutes": 69, "weekday": 3},
    {"origin": "BAQ", "destination": "BOG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "BGA", "destination": "BOG", "departure_time": "12:29", "duration_minutes": 69, "weekday": 3},
    {"origin": "SMR", "destination": "BOG", "departure_time": "13:50", "duration_minutes": 69, "weekday": 3},
    {"origin": "CTG", "destination": "BOG", "departure_time": "08:29", "duration_minutes": 69, "weekday": 3},
    {"origin": "CLO", "destination": "BOG", "departure_time": "06:29", "duration_minutes": 69, "weekday": 3},
    {"origin": "EOH", "destination": "BOG", "departure_time": "18:29", "duration_minutes": 69, "weekday": 3},

    # # Rutas Viernes
    {"origin": "BOG", "destination": "MDE", "departure_time": "05:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "MDE", "departure_time": "15:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "SMR", "departure_time": "07:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "SMR", "departure_time": "16:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "CTG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "CTG", "departure_time": "18:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "CLO", "departure_time": "07:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "CLO", "departure_time": "22:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "EOH", "departure_time": "09:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BOG", "destination": "EOH", "departure_time": "14:50", "duration_minutes": 69, "weekday": 4},

    {"origin": "MDE", "destination": "BOG", "departure_time": "07:29", "duration_minutes": 69, "weekday": 4},
    {"origin": "BAQ", "destination": "BOG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "BGA", "destination": "BOG", "departure_time": "12:29", "duration_minutes": 69, "weekday": 4},
    {"origin": "SMR", "destination": "BOG", "departure_time": "13:50", "duration_minutes": 69, "weekday": 4},
    {"origin": "CTG", "destination": "BOG", "departure_time": "08:29", "duration_minutes": 69, "weekday": 4},
    {"origin": "CLO", "destination": "BOG", "departure_time": "06:29", "duration_minutes": 69, "weekday": 4},
    {"origin": "EOH", "destination": "BOG", "departure_time": "18:29", "duration_minutes": 69, "weekday": 4},

    # # Rutas Sábado
    {"origin": "BOG", "destination": "MDE", "departure_time": "05:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "MDE", "departure_time": "15:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "SMR", "departure_time": "07:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "SMR", "departure_time": "16:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "CTG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "CTG", "departure_time": "18:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "CLO", "departure_time": "07:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "CLO", "departure_time": "22:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "EOH", "departure_time": "09:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BOG", "destination": "EOH", "departure_time": "14:50", "duration_minutes": 69, "weekday": 5},

    {"origin": "MDE", "destination": "BOG", "departure_time": "07:29", "duration_minutes": 69, "weekday": 5},
    {"origin": "BAQ", "destination": "BOG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "BGA", "destination": "BOG", "departure_time": "12:29", "duration_minutes": 69, "weekday": 5},
    {"origin": "SMR", "destination": "BOG", "departure_time": "13:50", "duration_minutes": 69, "weekday": 5},
    {"origin": "CTG", "destination": "BOG", "departure_time": "08:29", "duration_minutes": 69, "weekday": 5},
    {"origin": "CLO", "destination": "BOG", "departure_time": "06:29", "duration_minutes": 69, "weekday": 5},
    {"origin": "EOH", "destination": "BOG", "departure_time": "18:29", "duration_minutes": 69, "weekday": 5},

    # Rutas Domingo
    {"origin": "BOG", "destination": "MDE", "departure_time": "05:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "MDE", "departure_time": "15:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "BAQ", "departure_time": "06:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "BGA", "departure_time": "23:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "SMR", "departure_time": "07:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "SMR", "departure_time": "16:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "CTG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "CTG", "departure_time": "18:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "CLO", "departure_time": "07:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "CLO", "departure_time": "22:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "EOH", "departure_time": "09:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BOG", "destination": "EOH", "departure_time": "14:50", "duration_minutes": 69, "weekday": 6},

    {"origin": "MDE", "destination": "BOG", "departure_time": "07:29", "duration_minutes": 69, "weekday": 6},
    {"origin": "BAQ", "destination": "BOG", "departure_time": "09:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "BGA", "destination": "BOG", "departure_time": "12:29", "duration_minutes": 69, "weekday": 6},
    {"origin": "SMR", "destination": "BOG", "departure_time": "13:50", "duration_minutes": 69, "weekday": 6},
    {"origin": "CTG", "destination": "BOG", "departure_time": "08:29", "duration_minutes": 69, "weekday": 6},
    {"origin": "CLO", "destination": "BOG", "departure_time": "06:29", "duration_minutes": 69, "weekday": 6},
    {"origin": "EOH", "destination": "BOG", "departure_time": "18:29", "duration_minutes": 69, "weekday": 6},


]


class Flight(NamedTuple):
    origin: str
    destination: str
    departure_time: datetime
    duration_minutes: timedelta
    weekday: int 

class Route(NamedTuple):
    flights: List[Flight]
    total_duration: timedelta
    waiting_times: Dict[str, timedelta]



def busqueda_posibles_rutas_database(date:datetime, origin:str, exclude_destinations:List[str] = [])-> List[Dict[str, any]]:
    """
    Busca los vuelos disponibles segun la fecha dada, el origen y los destinos a excluir.
    
    Args:
        date (datetime): La fecha para determinar el día de la semana.
        origin (str): El codigo del aeropuerto de origen (por ejemplo, "BOG").
        exclude_destinations (List[str]): Lista de codigos de aeropuertos de destino que se deben excluir de los resultados.
    
    Returns:
        List[Dict[str, any]]: Una lista de vuelos que coinciden con los criterios de busqueda.
    """
    flights = []
    base_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    day_of_week = base_date.weekday()

    for route in weekly_flight_routes:

        if route["destination"] in exclude_destinations:
            continue

        if route["weekday"] == day_of_week and route["origin"] == origin:
            
            try:
                departure = datetime.strptime(route["departure_time"], "%H:%M")
                departure = base_date + timedelta(hours=departure.hour, minutes=departure.minute)
                
            except ValueError as e:
                raise ValueError(f"Formato de hora de salida inválido: {route['departure_time']} en ruta {route}") from e

    
            flights.append(Flight(
                origin=route["origin"],
                destination=route["destination"],
                departure_time=departure,
                duration_minutes=timedelta(minutes=route["duration_minutes"]),
                weekday=route["weekday"],
            ))
       
    return flights


def busqueda_posible_rutas_escala_database(saved_routes: List[any], min_connection_time:datetime, max_connection_time:datetime, exclude_destinations:List[str]):
    """
    Busca los vuelos disponibles  para hacer transbordos
    
    Args:
        saved_routes List[Flight]: La ruta completa que se ha seguido.
        min_connection_time (str): Tiempo minimo para la conexion
        max_connection_time (str): Tiempo maximo para la conexion
        exclude_destinations (List[str]): Lista de codigos de aeropuertos de destino que se deben excluir de los resultados.
    
    Returns:
        List[Dict[str, any]]: Una lista de vuelos que coinciden con los criterios de busqueda.
    """

    current_actual  = get_arrival_time(saved_routes[-1])
    current_day  = current_actual
    origin = saved_routes[-1].destination
    search_limit_reached = False
    valid_routes  = []

    try:
        while not search_limit_reached:
            dataResult = busqueda_posibles_rutas_database(current_day, origin, exclude_destinations)

            for dataValida in dataResult:
                if is_valid_connection(saved_routes[-1], dataValida, min_connection_time, max_connection_time):
                    valid_routes .append(dataValida)

                if (not_exist_connection(saved_routes[-1], dataValida, max_connection_time)):
                    search_limit_reached = True

            if valid_routes:
                search_limit_reached = True

            if (current_day - current_actual) >= max_connection_time:
                # Posible falla cuando haya más de tres escalas y no se encuentre un transbordo en los días cercanos, y solo exista una única ruta muchos días después.
                # Se puede resolver con un poco más de tiempo.
                search_limit_reached = True

            current_day = current_day + timedelta(days=1)
    except Exception as e:     
            print(f"Error al buscar rutas entre en busqueda_posible_rutas_escala_database: {origin} y fecha {current_day}: {str(e)}")

    finally:
        return valid_routes 
