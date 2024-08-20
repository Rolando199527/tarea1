import sqlite3

# Conexión y creación de la base de datos
conn = sqlite3.connect('recetas.db')
cursor = conn.cursor()

# Creación de la tabla de recetas si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS recetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    ingredientes TEXT NOT NULL,
    pasos TEXT NOT NULL
)
''')
conn.commit()

def agregar_receta():
    nombre = input("Ingrese el nombre de la receta: ")
    ingredientes = input("Ingrese los ingredientes separados por comas: ")
    pasos = input("Ingrese los pasos para la receta: ")
    cursor.execute("INSERT INTO recetas (nombre, ingredientes, pasos) VALUES (?, ?, ?)", (nombre, ingredientes, pasos))
    conn.commit()
    print("Receta agregada exitosamente.\n")

def actualizar_receta():
    id_receta = int(input("Ingrese el ID de la receta que desea actualizar: "))
    nombre = input("Ingrese el nuevo nombre de la receta: ")
    ingredientes = input("Ingrese los nuevos ingredientes separados por comas: ")
    pasos = input("Ingrese los nuevos pasos para la receta: ")
    cursor.execute("UPDATE recetas SET nombre = ?, ingredientes = ?, pasos = ? WHERE id = ?", (nombre, ingredientes, pasos, id_receta))
    conn.commit()
    print("Receta actualizada exitosamente.\n")

def eliminar_receta():
    id_receta = int(input("Ingrese el ID de la receta que desea eliminar: "))
    cursor.execute("DELETE FROM recetas WHERE id = ?", (id_receta,))
    conn.commit()
    print("Receta eliminada exitosamente.\n")

def ver_listado_recetas():
    cursor.execute("SELECT id, nombre FROM recetas")
    recetas = cursor.fetchall()
    if recetas:
        print("Listado de recetas:")
        for receta in recetas:
            print(f"ID: {receta[0]}, Nombre: {receta[1]}")
        print()
    else:
        print("No hay recetas disponibles.\n")

def buscar_receta():
    id_receta = int(input("Ingrese el ID de la receta que desea buscar: "))
    cursor.execute("SELECT nombre, ingredientes, pasos FROM recetas WHERE id = ?", (id_receta,))
    receta = cursor.fetchone()
    if receta:
        print(f"Nombre: {receta[0]}")
        print(f"Ingredientes: {receta[1]}")
        print(f"Pasos: {receta[2]}\n")
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

# Cerrar la conexión a la base de datos
conn.close()
