
import redis
import json

# Configuración de la base de datos Redis
client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def agregar_receta():
    nombre = input("Ingrese el nombre de la receta: ")
    ingredientes = input("Ingrese los ingredientes separados por comas: ")
    pasos = input("Ingrese los pasos para la receta: ")
    
    receta = {
        "nombre": nombre,
        "ingredientes": ingredientes.split(','),
        "pasos": pasos
    }
    client.hset(nombre, mapping=receta)
    print("Receta agregada exitosamente.\n")

def actualizar_receta():
    nombre = input("Ingrese el nombre de la receta que desea actualizar: ")
    
    if client.exists(nombre):
        nuevo_nombre = input("Ingrese el nuevo nombre de la receta: ")
        nuevos_ingredientes = input("Ingrese los nuevos ingredientes separados por comas: ")
        nuevos_pasos = input("Ingrese los nuevos pasos para la receta: ")
        
        receta = {
            "nombre": nuevo_nombre,
            "ingredientes": nuevos_ingredientes.split(','),
            "pasos": nuevos_pasos
        }
        
        # Actualizar la receta
        client.delete(nombre)  # Eliminar la antigua entrada
        client.hset(nuevo_nombre, mapping=receta)  # Insertar la nueva
        print("Receta actualizada exitosamente.\n")
    else:
        print("Receta no encontrada.\n")

def eliminar_receta():
    nombre = input("Ingrese el nombre de la receta que desea eliminar: ")
    if client.exists(nombre):
        client.delete(nombre)
        print("Receta eliminada exitosamente.\n")
    else:
        print("Receta no encontrada.\n")

def ver_listado_recetas():
    recetas = client.keys()
    if recetas:
        print("Listado de recetas:")
        for receta in recetas:
            print(f"Nombre: {receta}")
        print()
    else:
        print("No hay recetas disponibles.\n")

def buscar_receta():
    nombre = input("Ingrese el nombre de la receta que desea buscar: ")
    if client.exists(nombre):
        receta = client.hgetall(nombre)
        print(f"Nombre: {receta['nombre']}")
        print(f"Ingredientes: {', '.join(json.loads(receta['ingredientes']))}")
        print(f"Pasos: {receta['pasos']}\n")
    else:
        print("Receta no encontrada.\n")

def menu():
    while True:
        print("=== Libro de Recetas ===")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            agregar_receta()
        elif opcion == '2':
            actualizar_receta()
        elif opcion == '3':
            eliminar_receta()
        elif opcion == '4':
            ver_listado_recetas()
        elif opcion == '5':
            buscar_receta()
        elif opcion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, por favor intente nuevamente.\n")

# Ejecutar el menú
menu()

# Cerrar la conexión
client.close()
