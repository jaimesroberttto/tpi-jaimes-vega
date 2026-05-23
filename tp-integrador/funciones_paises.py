import csv
import os

CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA_ACTUAL, "paises.csv")
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]


def crear_csv_base():
    with open(RUTA_CSV, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(
            [
                {
                    "nombre": "Argentina",
                    "poblacion": 45376763,
                    "superficie": 2780400,
                    "continente": "America",
                },
                {
                    "nombre": "Brasil",
                    "poblacion": 213993437,
                    "superficie": 8515767,
                    "continente": "America",
                },
                {
                    "nombre": "Chile",
                    "poblacion": 19603733,
                    "superficie": 756102,
                    "continente": "America",
                },
                {
                    "nombre": "Alemania",
                    "poblacion": 83149300,
                    "superficie": 357022,
                    "continente": "Europa",
                },
                {
                    "nombre": "Espana",
                    "poblacion": 48345000,
                    "superficie": 505990,
                    "continente": "Europa",
                },
                {
                    "nombre": "Japon",
                    "poblacion": 125800000,
                    "superficie": 377975,
                    "continente": "Asia",
                },
                {
                    "nombre": "India",
                    "poblacion": 1428627663,
                    "superficie": 3287263,
                    "continente": "Asia",
                },
                {
                    "nombre": "Egipto",
                    "poblacion": 112716598,
                    "superficie": 1002450,
                    "continente": "Africa",
                },
                {
                    "nombre": "Australia",
                    "poblacion": 26600000,
                    "superficie": 7692024,
                    "continente": "Oceania",
                },
            ]
        )


def normalizar_texto(texto):
    return " ".join(texto.strip().split())


def pedir_texto_no_vacio(mensaje):
    while True:
        texto = normalizar_texto(input(mensaje))
        if texto != "":
            return texto
        print("Error: el valor no puede estar vacio.")


def pedir_entero(mensaje, minimo=None):
    while True:
        dato = input(mensaje).strip()
        if dato.isdigit():
            numero = int(dato)
            if minimo is None or numero >= minimo:
                return numero

        if minimo is None:
            print("Error: debe ingresar un numero entero valido.")
        else:
            print(f"Error: debe ingresar un numero entero mayor o igual a {minimo}.")


def pedir_opcion(minimo, maximo):
    while True:
        opcion = pedir_entero("Seleccione una opcion: ")
        if minimo <= opcion <= maximo:
            return opcion
        print(f"Error: debe elegir una opcion entre {minimo} y {maximo}.")


def cargar_paises():
    if not os.path.exists(RUTA_CSV):
        crear_csv_base()

    paises = []
    lineas_invalidas = 0

    with open(RUTA_CSV, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            try:
                pais = {
                    "nombre": normalizar_texto(fila["nombre"]),
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila["superficie"]),
                    "continente": normalizar_texto(fila["continente"]),
                }
                if (
                    pais["nombre"] == ""
                    or pais["continente"] == ""
                    or pais["poblacion"] <= 0
                    or pais["superficie"] <= 0
                ):
                    lineas_invalidas += 1
                    continue
                paises.append(pais)
            except (KeyError, TypeError, ValueError):
                lineas_invalidas += 1

    return paises, lineas_invalidas


def guardar_paises(paises):
    with open(RUTA_CSV, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        for pais in paises:
            escritor.writerow(pais)


def pausar():
    input("\nPresione Enter para continuar...")


def existe_pais(paises, nombre):
    nombre_buscado = nombre.lower()
    return any(pais["nombre"].lower() == nombre_buscado for pais in paises)


def buscar_pais_exacto(paises, nombre):
    nombre_buscado = nombre.lower()
    for pais in paises:
        if pais["nombre"].lower() == nombre_buscado:
            return pais
    return None


def buscar_pais_por_nombre(paises, nombre):
    nombre_buscado = nombre.lower()
    resultados = []
    for pais in paises:
        if nombre_buscado in pais["nombre"].lower():
            resultados.append(pais)
    return resultados


def agregar_pais(paises):
    print("\n--- Agregar pais ---")
    nombre = pedir_texto_no_vacio("Nombre: ")

    if existe_pais(paises, nombre):
        print("Error: ese pais ya existe en el sistema.")
        return False

    poblacion = pedir_entero("Poblacion: ", 1)
    superficie = pedir_entero("Superficie en km2: ", 1)
    continente = pedir_texto_no_vacio("Continente: ")

    pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    }
    paises.append(pais)
    guardar_paises(paises)
    print("Pais agregado correctamente.")
    return True


def actualizar_pais(paises):
    print("\n--- Actualizar pais ---")
    nombre = pedir_texto_no_vacio("Ingrese el nombre del pais: ")
    pais = buscar_pais_exacto(paises, nombre)

    if pais is None:
        print("Error: no se encontro un pais con ese nombre.")
        return False

    print("Pais encontrado:")
    print(formatear_pais(pais))

    pais["poblacion"] = pedir_entero("Nueva poblacion: ", 1)
    pais["superficie"] = pedir_entero("Nueva superficie en km2: ", 1)
    guardar_paises(paises)
    print("Datos actualizados correctamente.")
    return True


def filtrar_por_continente(paises, continente):
    continente_buscado = continente.lower()
    return [pais for pais in paises if pais["continente"].lower() == continente_buscado]


def filtrar_por_rango_poblacion(paises, minimo, maximo):
    return [pais for pais in paises if minimo <= pais["poblacion"] <= maximo]


def filtrar_por_rango_superficie(paises, minimo, maximo):
    return [pais for pais in paises if minimo <= pais["superficie"] <= maximo]


def ordenar_paises(paises, criterio, descendente=False):
    if criterio == "nombre":
        return sorted(paises, key=lambda pais: pais["nombre"].lower(), reverse=descendente)
    if criterio == "poblacion":
        return sorted(paises, key=lambda pais: pais["poblacion"], reverse=descendente)
    if criterio == "superficie":
        return sorted(paises, key=lambda pais: pais["superficie"], reverse=descendente)
    return paises[:]


def obtener_estadisticas(paises):
    if not paises:
        return None

    pais_mayor_poblacion = max(paises, key=lambda pais: pais["poblacion"])
    pais_menor_poblacion = min(paises, key=lambda pais: pais["poblacion"])
    promedio_poblacion = sum(pais["poblacion"] for pais in paises) / len(paises)
    promedio_superficie = sum(pais["superficie"] for pais in paises) / len(paises)

    cantidad_por_continente = {}
    for pais in paises:
        continente = pais["continente"]
        cantidad_por_continente[continente] = cantidad_por_continente.get(continente, 0) + 1

    return {
        "mayor_poblacion": pais_mayor_poblacion,
        "menor_poblacion": pais_menor_poblacion,
        "promedio_poblacion": promedio_poblacion,
        "promedio_superficie": promedio_superficie,
        "cantidad_por_continente": cantidad_por_continente,
    }


def formatear_pais(pais):
    return (
        f"Nombre: {pais['nombre']} | "
        f"Poblacion: {pais['poblacion']} | "
        f"Superficie: {pais['superficie']} km2 | "
        f"Continente: {pais['continente']}"
    )


def mostrar_paises(paises, titulo="Listado de paises"):
    print(f"\n--- {titulo} ---")
    if not paises:
        print("No hay paises para mostrar.")
        return

    for indice, pais in enumerate(paises, start=1):
        print(f"{indice}. {formatear_pais(pais)}")


def pedir_rango(mensaje_minimo, mensaje_maximo):
    while True:
        minimo = pedir_entero(mensaje_minimo, 1)
        maximo = pedir_entero(mensaje_maximo, 1)
        if minimo <= maximo:
            return minimo, maximo
        print("Error: el valor minimo no puede ser mayor que el maximo.")


def mostrar_estadisticas(paises):
    estadisticas = obtener_estadisticas(paises)
    print("\n--- Estadisticas ---")

    if estadisticas is None:
        print("No hay datos para calcular estadisticas.")
        return

    print("Pais con mayor poblacion:")
    print(formatear_pais(estadisticas["mayor_poblacion"]))
    print("\nPais con menor poblacion:")
    print(formatear_pais(estadisticas["menor_poblacion"]))
    print(f"\nPromedio de poblacion: {estadisticas['promedio_poblacion']:.2f}")
    print(f"Promedio de superficie: {estadisticas['promedio_superficie']:.2f}")
    print("\nCantidad de paises por continente:")
    for continente, cantidad in estadisticas["cantidad_por_continente"].items():
        print(f"{continente}: {cantidad}")
