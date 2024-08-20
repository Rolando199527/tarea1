import requests

# Base URL de la API
BASE_URL = "https://swapi.dev/api/"

# a) ¿En cuántas películas aparecen planetas cuyo clima sea árido?
def get_arid_planets_films_count():
    arid_planets_films = set()
    next_page = BASE_URL + "planets/"
    
    while next_page:
        response = requests.get(next_page).json()
        planets = response['results']
        for planet in planets:
            if 'arid' in planet['climate']:
                films = planet['films']
                arid_planets_films.update(films)
        next_page = response['next']
    
    return len(arid_planets_films)

# b) ¿Cuántos Wookies aparecen en toda la saga?
def get_wookies_count():
    wookies_count = 0
    next_page = BASE_URL + "species/"
    
    while next_page:
        response = requests.get(next_page).json()
        species = response['results']
        for specie in species:
            if specie['name'].lower() == 'wookie':
                wookies_count += len(specie['people'])
        next_page = response['next']
    
    return wookies_count

# c) ¿Cuál es el nombre de la aeronave más pequeña en la primera película?
def get_smallest_starship_in_first_film():
    response = requests.get(BASE_URL + "films/1/").json()
    starships_urls = response['starships']
    smallest_starship_name = None
    smallest_starship_length = float('inf')
    
    for url in starships_urls:
        starship = requests.get(url).json()
        length = float(starship['length'].replace(',', ''))
        if length < smallest_starship_length:
            smallest_starship_length = length
            smallest_starship_name = starship['name']
    
    return smallest_starship_name

# Ejecutar las funciones y mostrar los resultados
print(f"a) Número de películas con planetas áridos: {get_arid_planets_films_count()}")
print(f"b) Número de Wookies en toda la saga: {get_wookies_count()}")
print(f"c) Aeronave más pequeña en la primera película: {get_smallest_starship_in_first_film()}")
