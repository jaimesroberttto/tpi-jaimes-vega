import csv
import os
import questionary
import sys



CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA_ACTUAL, "paises.csv")
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]

VERDE = "\033[1;32m"
ROJO = "\033[1;31m"
AMARILLO = "\033[1;33m"
AZUL = "\033[1;34m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

class NombreErroneoError(Exception):
    pass
class SaliendoAlMenuError(Exception):
    pass

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


def normalizar_continente(texto):
    return normalizar_texto(texto).capitalize()


def pedir_texto_no_vacio(mensaje):
    while True:
        texto = normalizar_texto(input(mensaje))
        if texto.lower() == "s" or texto.lower() == "salir":
            raise SaliendoAlMenuError("Saliendo al menú principal.")
        elif texto != "":
            return texto
        else:
            print("Error: el texto no puede estar vacío.")


def pedir_entero(mensaje, minimo=None):
    while True:
        dato = input(mensaje).strip()
        if dato.lower() == "s" or dato.lower() == "salir":
            raise SaliendoAlMenuError("Saliendo al menú principal.")
        try:
            numero = int(dato)
            if minimo is None or numero >= minimo:
                return numero
            else:
                print(f"Error: El número debe ser mayor o igual a {minimo}.")
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")


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
                    # validar solo letras en poblacion pais y continente
                    "nombre": normalizar_texto(fila["nombre"]),
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila["superficie"]),
                    "continente": normalizar_continente(fila["continente"]),
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
    input(f"\n{CYAN}Presione Enter para continuar...{RESET}")


def existe_pais(paises, nombre):
    nombre_buscado = nombre.lower()
    return any(pais["nombre"].lower() == nombre_buscado for pais in paises)


def buscar_pais_exacto(paises, nombre):
    while True:
        nombre_buscado = nombre.lower()
        for pais in paises:
            if pais["nombre"].lower() == nombre_buscado:
                return pais
        print("Error: no se encontro un pais con ese nombre. Intente nuevamente o ingrese s |'salir' para cancelar.")
        nombre = input("Nombre del pais: ").strip()
        if nombre.lower() == "salir" or nombre.lower() == "s":
            return None


def buscar_pais_por_nombre(paises, nombre):
    nombre_buscado = nombre.lower()
    resultados = []
    for pais in paises:
        if nombre_buscado in pais["nombre"].lower():
            resultados.append(pais)
    return resultados


def agregar_pais(paises):
    print(f"\n{AZUL}--- Agregar pais ---{RESET}")
    
    try:
        nombre = pedir_texto_no_vacio("Ingrese el nombre o 's' para salir: ").strip().capitalize()

        if existe_pais(paises, nombre):
            print("Error: ese pais ya existe en el sistema.")
            return False
        if not nombre.isalpha():
            raise NombreErroneoError ("Error: el nombre del pais solo puede contener letras. Volviendo al menú principal.")
        
        poblacion = pedir_entero("Ingrese poblacion o 's' para salir: ", 1)
        superficie = pedir_entero("Ingrese Superficie en km2 o 's' para salir: ", 1)
        continente = normalizar_continente(
            pedir_texto_no_vacio("Ingrese el continente o 's' para salir: ")
        )
        if not continente.isalpha():
            raise NombreErroneoError ("Error: el nombre del continente solo puede contener letras. Volviendo al menú principal.")

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
    
    except NombreErroneoError as e:
        print(e)
        return False
    
    except SaliendoAlMenuError as e:
        print(e)
        return False


def actualizar_pais(paises):
    print(f"\n{AZUL}--- Actualizar pais ---{RESET}")
    try:
        nombre = pedir_texto_no_vacio("Ingrese el nombre del pais: ").strip()
        pais = buscar_pais_exacto(paises, nombre)

        if pais is None:
            print("Volviendo al menú principal.")
            return False

        print("Pais encontrado:")
        print(formatear_pais(pais))
        while True:
            opcion = questionary.select(
                message=f"{AZUL}Elija la acción a realizar:{RESET}",
                choices=["Modificar población", "Modificar superficie", "Modificar ambos", "Salir"]
            ).ask()

            if opcion == "Salir":
                print("No se realizaron cambios.")
                return True
            elif opcion == "Modificar población":
                pais["poblacion"] = pedir_entero("Ingrese la nueva poblacion o 's' para salir: ", 1)
            elif opcion == "Modificar superficie":
                pais["superficie"] = pedir_entero("Ingrese la nueva superficie en km2 o 's' para salir: ", 1)
            elif opcion == "Modificar ambos":
                pais["poblacion"] = pedir_entero("Ingrese la nueva poblacion o 's' para salir: ", 1)
                pais["superficie"] = pedir_entero("Ingrese la nueva superficie en km2 o 's' para salir: ", 1)

            guardar_paises(paises)
            print("Datos actualizados correctamente.")
            return True
    except SaliendoAlMenuError as e:
        print(e)
        return False


def filtrar_por_continente(paises, continente):
    continente_buscado = continente.lower()
    return [pais for pais in paises if pais["continente"].lower() == continente_buscado]


def filtrar_por_rango_poblacion(paises, minimo, maximo):
    return [pais for pais in paises if minimo <= pais["poblacion"] <= maximo]


def filtrar_por_rango_superficie(paises, minimo, maximo):
    return [pais for pais in paises if minimo <= pais["superficie"] <= maximo]


def ordenar_paises(paises, criterio, as_des):
    n = len(paises)
    paises_ordenados = list(paises)
    
    if criterio == "nombre":
        
        if as_des == "Ascendente":
            for i in range(n - 1):
                for j in range(n - 1 - i):
                    nombre_actual = paises_ordenados[j]["nombre"].lower()
                    nombre_siguiente = paises_ordenados[j+1]["nombre"].lower()
                    if nombre_actual > nombre_siguiente:
                        paises_ordenados[j], paises_ordenados[j+1] = paises_ordenados[j+1], paises_ordenados[j]
        
        elif as_des == "Descendente":
            for i in range(n - 1):
                for j in range(n - 1 - i):
                    nombre_actual = paises_ordenados[j]["nombre"].lower()
                    nombre_siguiente = paises_ordenados[j+1]["nombre"].lower()
                    if nombre_actual < nombre_siguiente:
                        paises_ordenados[j], paises_ordenados[j+1] = paises_ordenados[j+1], paises_ordenados[j]

    elif criterio == "poblacion":

        if as_des == "Ascendente":
            for i in range(n - 1):
                for j in range(n - 1 - i):
                    nombre_actual = paises_ordenados[j]["poblacion"]
                    nombre_siguiente = paises_ordenados[j+1]["poblacion"]
                    if nombre_actual > nombre_siguiente:
                        paises_ordenados[j], paises_ordenados[j+1] = paises_ordenados[j+1], paises_ordenados[j]
        
        elif as_des == "Descendente":
            for i in range(n - 1):
                for j in range(n - 1 - i):
                    nombre_actual = paises_ordenados[j]["poblacion"]
                    nombre_siguiente = paises_ordenados[j+1]["poblacion"]
                    if nombre_actual < nombre_siguiente:
                        paises_ordenados[j], paises_ordenados[j+1] = paises_ordenados[j+1], paises_ordenados[j]
    
    elif criterio == "superficie":

        if as_des == "Ascendente":
            for i in range(n - 1):
                for j in range(n - 1 - i):
                    nombre_actual = paises_ordenados[j]["superficie"]
                    nombre_siguiente = paises_ordenados[j+1]["superficie"]
                    if nombre_actual > nombre_siguiente:
                        paises_ordenados[j], paises_ordenados[j+1] = paises_ordenados[j+1], paises_ordenados[j]
        
        elif as_des == "Descendente":
            for i in range(n - 1):
                for j in range(n - 1 - i):
                    nombre_actual = paises_ordenados[j]["superficie"]
                    nombre_siguiente = paises_ordenados[j+1]["superficie"]
                    if nombre_actual < nombre_siguiente:
                        paises_ordenados[j], paises_ordenados[j+1] = paises_ordenados[j+1], paises_ordenados[j]
    
    return paises_ordenados

def obtener_estadisticas(paises):
    if not paises:
        return None
    pais_mayor_poblacion = paises[0]
    pais_menor_poblacion = paises[0]
    
    for i in range(1, len(paises)):
        pais_actual = paises[i]
        if pais_actual["poblacion"] > pais_mayor_poblacion["poblacion"]:
            pais_mayor_poblacion = pais_actual
       
        if pais_actual["poblacion"] < pais_menor_poblacion["poblacion"]:
            pais_menor_poblacion = pais_actual
    
    promedio_poblacion = sum(pais["poblacion"] for pais in paises) / len(paises)
    promedio_superficie = sum(pais["superficie"] for pais in paises) / len(paises)

    cantidad_por_continente = {}
    for pais in paises:
        continente = normalizar_continente(pais["continente"])
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
    print(f"\n{AZUL}--- {titulo} ---{RESET}")
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
    print(f"\n{AZUL}--- Estadisticas ---{RESET}")

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

def menu_busqueda(paises):
    print(f"\n{AZUL}--- Buscar pais por nombre ---{RESET}")
    try:
        nombre = pedir_texto_no_vacio("Ingrese el nombre o parte del nombre: ")
        resultados = buscar_pais_por_nombre(paises, nombre)
        if not resultados:
            print("No se encontraron paises con esa busqueda.")
            return

        mostrar_paises(resultados, "Resultados de la busqueda")
    except SaliendoAlMenuError as e:
        print(e)

def menu_filtros(paises):
    while True:
        print(f"\n{AZUL}--- Filtros ---{RESET}")
        print(f"{AZUL}1. Filtrar por continente{RESET}")
        print(f"{AZUL}2. Filtrar por rango de poblacion{RESET}")
        print(f"{AZUL}3. Filtrar por rango de superficie{RESET}")
        print(f"{AZUL}4. Volver{RESET}")
        try:
            opcion = pedir_opcion(1, 4)

            if opcion == 1:
                continente = pedir_texto_no_vacio("Ingrese el continente: ")
                resultados = filtrar_por_continente(paises, continente)
                if resultados:
                    mostrar_paises(resultados, f"Paises del continente {continente}")
                else:
                    print("No se encontraron paises para ese continente.")
                pausar()
            elif opcion == 2:
                minimo, maximo = pedir_rango(
                    "Ingrese la poblacion minima: ",
                    "Ingrese la poblacion maxima: ",
                )
                resultados = filtrar_por_rango_poblacion(paises, minimo, maximo)
                if resultados:
                    mostrar_paises(resultados, "Paises filtrados por poblacion")
                else:
                    print("No se encontraron paises en ese rango de poblacion.")
                pausar()
            elif opcion == 3:
                minimo, maximo = pedir_rango(
                    "Ingrese la superficie minima: ",
                    "Ingrese la superficie maxima: ",
                )
                resultados = filtrar_por_rango_superficie(paises, minimo, maximo)
                if resultados:
                    mostrar_paises(resultados, "Paises filtrados por superficie")
                else:
                    print("No se encontraron paises en ese rango de superficie.")
                pausar()
            else:
                break
        except SaliendoAlMenuError as e:
            print(e)

def menu_ordenamientos(paises):
    
    while True:
        print(f"\n{AZUL}--- Ordenamientos ---{RESET}")
        opcion = questionary.select(
        message=f"{AZUL}Elija el método de ordenamiento:{RESET} ",
        choices=["Por nombre", "Por poblacion","Por superficie", "Salir"]
        ).ask()
        print(f"Elegiste: {opcion}")
        
        if opcion == "Salir":
            break
        else:
            as_des = questionary.select(
            message=f"{AZUL}Elija Ascendente o Descendente:{RESET}",
            choices=["Ascendente", "Descendente"]
            ).ask()
            criterio = ""
            as_des = "Ascendente" if as_des == "Ascendente" else "Descendente"
            if opcion == "Por nombre":
                criterio = "nombre"
            elif opcion == "Por poblacion":
                criterio = "poblacion"
            elif opcion == "Por superficie":
                criterio = "superficie"
            
            paises_ordenados = ordenar_paises(paises, criterio, as_des)
            mostrar_paises(paises_ordenados, f"Paises ordenados por {criterio}")
            pausar()
            limpiar_pantalla()


def mostrar_menu_principal():
    print(f"\n{AZUL}=== Gestion de Datos de Paises ==={RESET}")
    opcion = questionary.select(
    message=f"{AZUL}Seleccioná:{RESET}",
    choices=["Mostrar todos los paises", "Agregar un pais", "Actualizar poblacion y superficie", 
             "Buscar pais por nombre", "Filtrar paises", "Ordenar paises", "Mostrar estadisticas", "Salir"]
            ).ask()
    return opcion


def main():
    paises, lineas_invalidas = cargar_paises()

    if lineas_invalidas > 0:
        print(
            f"Advertencia: se ignoraron {lineas_invalidas} lineas invalidas del archivo CSV."
        )

    while True:
        opcion = mostrar_menu_principal()
        limpiar_pantalla()

        if opcion == "Mostrar todos los paises":
            mostrar_paises(paises, "Listado completo de paises")
            pausar()
            limpiar_pantalla()
        elif opcion == "Agregar un pais":
            agregar_pais(paises)
            pausar()
            limpiar_pantalla()
        elif opcion == "Actualizar poblacion y superficie":
            actualizar_pais(paises)
            pausar()
            limpiar_pantalla()
        elif opcion == "Buscar pais por nombre":
            menu_busqueda(paises)
            pausar()
        elif opcion == "Filtrar paises":
            menu_filtros(paises)
        elif opcion == "Ordenar paises":
            menu_ordenamientos(paises)
        elif opcion == "Mostrar estadisticas":
            mostrar_estadisticas(paises)
            pausar()
        elif opcion == "Salir":
            print("Programa finalizado.")
            break

def limpiar_pantalla():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')
