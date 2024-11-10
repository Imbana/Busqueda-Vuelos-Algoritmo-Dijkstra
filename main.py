
from datetime import datetime, timedelta
from typing import List, Dict
from heapq import heappop, heappush

from utils import calculate_waiting_times, format_route, is_valid_connection, is_valid_departure_time
from database import Route, busqueda_posibles_rutas_database, busqueda_posible_rutas_escala_database, get_arrival_time



def busqueda_total_rutas_validas( 
                origin_airport_code: str, 
                destination_airport_code: str, 
                search_date: datetime,
                min_connection_interval: timedelta,
                max_connection_interval: timedelta) -> List[Dict[str, any]]:
    """
    Encuentra todas las rutas posibles entre origen y destino, tomando en cuenta la fecha de busqueda, minimo y maximo intervalo para conexiones
    """
    total_route_found = []

    
    # Cola de prioridad: (tiempo_total, [vuelos], aeropuerto_actual, tiempo_actual, visitados)
    queue = [(timedelta(0), [], origin_airport_code,  set())]
    
    while queue:


        total_time, saved_routes, current_airport, visited = heappop(queue)
   
        if current_airport == destination_airport_code:
            if saved_routes:
                waiting_times = calculate_waiting_times(saved_routes)
                total_route_found.append(Route(saved_routes, total_time, waiting_times))
            continue


        if saved_routes:
            possible_valid_routes = busqueda_posible_rutas_escala_database(saved_routes, min_connection_interval, max_connection_interval, visited)
        else:
            possible_valid_routes = busqueda_posibles_rutas_database(search_date, origin_airport_code, [])


        for flight in possible_valid_routes:
            if flight.destination not in visited:
                new_route = saved_routes + [flight]
                
                if not saved_routes:  # Primer vuelo
                    if is_valid_departure_time(flight, search_date):
                        continue
                    new_total_time = flight.duration_minutes
                else:
                    if not is_valid_connection(saved_routes[-1], flight, min_connection_interval, max_connection_interval):
                        continue

                    connection_time = flight.departure_time - get_arrival_time(saved_routes[-1])
                    new_total_time = total_time + flight.duration_minutes + connection_time
                
                visited.add(current_airport)


                heappush(queue, (new_total_time, new_route, flight.destination, visited))

    #organizar los resultados por duración o tiempo total del viaje.
    return sorted(total_route_found, key=lambda x: x.total_duration)


def main():


    #Parametros del fronted   Código del aeropuerto de origen  - Código del aeropuerto de destino -  Fecha de la consulta

    search_date =  datetime.now().replace(year=2024, month=11, day=11, hour=0, minute=0)  # Fecha de la consulta
    origin_airport_code = "BOG"   #  origen
    destination_airport_code = "BGA"  # destino


    #Parametros del sistema -  Tiempo mínimo entre conexiones (40 a 60 mintos en promedio) - Tiempo máximo  que se permite entre conexiones (ejemplo 13 horas)

    min_connection_interval: timedelta = timedelta(minutes=40)  # Tiempo mínimo 
    max_connection_interval: timedelta = timedelta(hours=24) # Tiempo máximo 
    

    
    try:

        # Busqueda de todas las rutas posibles
        total_routes = busqueda_total_rutas_validas(
            origin_airport_code,
            destination_airport_code,
            search_date,
            min_connection_interval,
            max_connection_interval
        ) 


        # Imprime en consola resultados
        if not total_routes:
            print("No se encontraron rutas disponibles. Intenga con otra fecha")
            return
        
        print(f"\n--------Se encontraron {len(total_routes)} rutas:--------\n")
        for i, route in enumerate(total_routes, 1):
            print(f"=== Ruta {i} ===")
            print(format_route(route))
            print()

    except ValueError as e:
        
        print(f"Error específico de valor: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()

