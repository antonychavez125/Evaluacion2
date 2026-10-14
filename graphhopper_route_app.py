#!/usr/bin/env python3
import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
# Reemplaza 'TU_CLAVE_API_GRAPHHOPPER' con la clave API real que obtuviste en tu cuenta de Graphhopper
key = "ecdad32b-86e5-437e-9c83-b11ebee2adce"  

def geocoding(location, key):
    while location == "":
        location = input("No ingresó ninguna ubicación. Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        
        if len(state) != 0 and len(country) != 0:
            new_loc = f"{name}, {state}, {country}"
        elif len(state) != 0:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name
        
        print(f"URL de Geocodificación para {new_loc} (Tipo: {value}):\n{url}")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print(f"Estado de API Geocódigo: {json_status}\nMensaje de error: {json_data.get('message', 'Error desconocido')}")
    return json_status, lat, lng, new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículos disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car (automóvil), bike (bicicleta), foot (a pie)")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    
    profile = ["car", "bike", "foot"]
    vehicle = input("Ingrese un perfil de vehículo (o escriba 's' o 'salir' para terminar): ")
    
    # Opción para salir del programa ingresando 's' o 'salir' (también compatible con 'q' o 'quit')
    if vehicle.lower() in ["quit", "q", "salir", "s"]:
        print("Saliendo del programa de geolocalización. ¡Hasta luego!")
        break
    elif vehicle in profile:
        vehicle = vehicle
    else: 
        vehicle = "car"
        print("No se ingresó un perfil válido. Usando el perfil predeterminado de automóvil (car).")

    loc1 = input("Punto de partida: ")
    if loc1.lower() in ["quit", "q", "salir", "s"]:
        print("Saliendo del programa de geolocalización. ¡Hasta luego!")
        break
    orig = geocoding(loc1, key)

    loc2 = input("Destino: ")
    if loc2.lower() in ["quit", "q", "salir", "s"]:
        print("Saliendo del programa de geolocalización. ¡Hasta luego!")
        break
    dest = geocoding(loc2, key)

    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = f"&point={orig[1]}%2C{orig[2]}"
        dp = f"&point={dest[1]}%2C{dest[2]}"
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        paths_response = requests.get(paths_url)
        paths_status = paths_response.status_code
        paths_data = paths_response.json()
        
        print(f"Estado de API de Rutas: {paths_status}")
        print(f"URL de la API de Rutas:\n{paths_url}")
        print("=================================================")
        print(f"Ruta desde {orig[3]} hasta {dest[3]} en {vehicle}")
        print("=================================================")
        
        if paths_status == 200:
            # Cálculo de unidades métricas e imperiales con formateo a dos decimales máximo
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min_val = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            
            print(f"Distancia recorrida: {miles:.2f} millas / {km:.2f} km")
            print(f"Duración del viaje: {hr:02d}:{min_val:02d}:{sec:02d}")
            print("=================================================")
            
            # Impresión de instrucciones paso a paso detalladas
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print(f"• {path} ({distance/1000:.2f} km / {distance/1000/1.61:.2f} millas)")
            print("=================================================")
        else:
            print(f"Mensaje de error: {paths_data.get('message', 'Conexión entre ubicaciones no encontrada')}")
            print("*************************************************")