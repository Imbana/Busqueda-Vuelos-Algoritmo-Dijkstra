document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('flightSearchForm');
    const origin = document.getElementById('origin');
    const destination = document.getElementById('destination');
    const flightDate = document.getElementById('flightDate');
    const resultsContainer = document.getElementById('flightsResults');
    const flightTemplate = document.getElementById('flightCardTemplate');

    // Establecer fecha mínima como hoy
    const today = new Date();
    flightDate.min = today.toISOString().split('T')[0];
    
    // Establecer fecha máxima como 6 meses desde hoy
    const maxDate = new Date();
    maxDate.setMonth(maxDate.getMonth() + 6);
    flightDate.max = maxDate.toISOString().split('T')[0];

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const searchData = {
            origin: origin.value,
            destination: destination.value,
            date: flightDate.value
        };

        try {
            const response = await fetch('/search-flights', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(searchData)
            });

            const data = await response.json();

            if (data.status === 'success') {

                console.log(data)

                displayFlights(data.flights);
            } else {
                alert('Error en la búsqueda: ' + data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al buscar vuelos');
        }
    });

    function displayFlights(flights) {
        resultsContainer.innerHTML = '';


        if (flights.length === 0) {
            resultsContainer.innerHTML = '<p class="no-results">No se encontraron vuelos para esta ruta y fecha</p>';
            return;
        }



        flights.forEach(flight => {
            const flightCard = document.importNode(flightTemplate.content, true);
            
            let htmlRoutes = '';
            flight.routes.forEach((route, index) => {

                htmlRoutes += `
                    <div class ="routes_text">
                        <span>Vuelo: ${route.origin} --> ${route.destination}</span><br>
                        <span>Día: ${route.weekdays}</span><br>
                        <span>Salida: ${route.departure_time}</span><br>
                        <span>Llegada: ${route.arrival_time}</span><br>
                        <span>Duración: ${route.duration_minutes}</span><br>
                        ${
                            route.wait_time !== "0h 0m" 
                                ? `<span >Espera en: ${route.destination} ${route.wait_time}</span>` 
                                : ""
                        }

                    </div>`;
                console.log(route.wait_time)

                if (index < flight.routes.length - 1) {
                    htmlRoutes += `<span style="margin: auto 4px;">-</span>`;
                }
            })
            

            // Llenar los datos del vuelo
            flightCard.querySelector('.departure-time').textContent = flight.departure_time;
            flightCard.querySelector('.arrival-time').textContent = flight.arrival_time;
            flightCard.querySelector('.duration-time').textContent = flight.duration;
            flightCard.querySelector('.stops').textContent = flight.stops;
            flightCard.querySelector('.operator-name').textContent = flight.operator;
            flightCard.querySelector('.price-amount').textContent = `COP ${flight.price}`;

            flightCard.querySelector('.routes').innerHTML = htmlRoutes;

            // Manejar tags
            const tagContainer = flightCard.querySelector('.flight-card-header');
            tagContainer.innerHTML = '';
            flight.tags.forEach(tag => {
                const tagSpan = document.createElement('span');
                tagSpan.className = `tag ${tag.includes('económico') ? 'economic' : ''}`;
                tagSpan.textContent = tag;
                tagContainer.appendChild(tagSpan);
            });

            resultsContainer.appendChild(flightCard);
        });
    }

    // Prevenir selección del mismo origen y destino
    destination.addEventListener('change', function() {
        if (this.value === origin.value) {
            alert('El origen y destino no pueden ser iguales');
            this.value = '';
        }
    });

    origin.addEventListener('change', function() {
        if (this.value === destination.value) {
            alert('El origen y destino no pueden ser iguales');
            destination.value = '';
        }
    });
});