import csv
import os
import questionary
import unicodedata
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA_ACTUAL, "paises.csv")
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]
console = Console()

class NombreErroneoError(Exception):
    pass
class SaliendoAlMenuError(Exception):
    pass

def validar_continente(continente):
    continentes = ["America", "Europa", "Asia", "Africa", "Oceania"]
    if continente not in continentes:
        return None
    return continente


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
    texto_sin_tildes = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return " ".join(texto_sin_tildes.strip().split())


def normalizar_continente(texto):
    return normalizar_texto(texto).capitalize()


def mostrar_error(mensaje):
    console.print(f"[bold red]{mensaje}[/bold red]")


def mostrar_advertencia(mensaje):
    console.print(f"[bold yellow]{mensaje}[/bold yellow]")


def mostrar_exito(mensaje):
    console.print(f"[bold green]{mensaje}[/bold green]")


def mostrar_info(mensaje):
    console.print(f"[bold cyan]{mensaje}[/bold cyan]")


def mostrar_titulo(titulo):
    console.print(Panel.fit(titulo, border_style="bold blue"))


def pedir_texto_no_vacio(mensaje):
    while True:
        texto = normalizar_texto(input(mensaje))
        if texto.lower() == "s" or texto.lower() == "salir":
            raise SaliendoAlMenuError("Saliendo al menú principal.")
        elif texto != "":
            return texto
        else:
            mostrar_error("Error: el texto no puede estar vacío.")


def pedir_entero(mensaje, minimo=None):
    while True:
        dato = input(mensaje).strip().replace(".", "")
        if dato == "":
            mostrar_error("Error: El número no puede estar vacío.")
            continue
        if dato.lower() == "s" or dato.lower() == "salir":
            raise SaliendoAlMenuError("Saliendo al menú principal.")
        try:
            numero = int(dato)
            if minimo is None or numero >= minimo:
                return numero
            else:
                mostrar_error(f"Error: El número debe ser mayor o igual a {minimo}.")
        except ValueError:
            mostrar_error("Error: Debe ingresar un número entero válido.")


def pedir_opcion(minimo, maximo):
    while True:
        opcion = pedir_entero("Seleccione una opcion: ")
        if minimo <= opcion <= maximo:
            return opcion
        mostrar_error(f"Error: debe elegir una opcion entre {minimo} y {maximo}.")


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
    console.input("\n[bold cyan]Presione Enter para continuar...[/bold cyan]")


def existe_pais(paises, nombre):
    nombre_buscado = normalizar_texto(nombre).lower()
    return any(normalizar_texto(pais["nombre"]).lower() == nombre_buscado for pais in paises)


def buscar_pais_exacto(paises, nombre):
    while True:
        nombre_buscado = normalizar_texto(nombre).lower()
        for pais in paises:
            if normalizar_texto(pais["nombre"]).lower() == nombre_buscado:
                return pais
        mostrar_error("Error: no se encontro un pais con ese nombre. Intente nuevamente o ingrese s |'salir' para cancelar.")
        nombre = input("Nombre del pais: ").strip()
        if nombre.lower() == "salir" or nombre.lower() == "s":
            return None


def buscar_pais_por_nombre(paises, nombre):
    nombre_buscado = normalizar_texto(nombre).lower()
    resultados = []
    for pais in paises:
        if nombre_buscado in normalizar_texto(pais["nombre"]).lower():
            resultados.append(pais)
    return resultados


def agregar_pais(paises):
    mostrar_titulo("Agregar pais")

    try:
        while True:
            nombre = pedir_texto_no_vacio("Ingrese el nombre o 's' para salir: ").strip().capitalize()

            if existe_pais(paises, nombre):
                mostrar_error("Error: ese pais ya existe en el sistema.")
                return False
            if not nombre.replace(" ", "").isalpha(): 
                raise NombreErroneoError ("Error: el nombre del pais solo puede contener letras. Volviendo al menú principal.")
            break
        while True:
            poblacion = pedir_entero("Ingrese poblacion o 's' para salir: ", 1)
            break
        while True:
            superficie = pedir_entero("Ingrese Superficie en km2 o 's' para salir: ", 1)
            break
        while True:
            try:
                continente = normalizar_continente(pedir_texto_no_vacio("Ingrese el continente o 's' para salir: "))
                if not continente.isalpha():
                    raise NombreErroneoError("Error: el nombre del continente solo puede contener letras.")
                if not validar_continente(continente):
                    raise ValueError (f"El continente {continente} no es válido.")
            except ValueError as e:
                mostrar_error(str(e))
                continue
            except NombreErroneoError as e:
                mostrar_error(str(e))
                continue
            else:
                break

        pais = {
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente,
        }
        paises.append(pais)
        guardar_paises(paises)
        mostrar_exito("Pais agregado correctamente.")
        return True

    except NombreErroneoError as e:
        mostrar_error(str(e))
        return False

    except SaliendoAlMenuError as e:
        mostrar_advertencia(str(e))
        return False


def actualizar_pais(paises):
    mostrar_titulo("Actualizar pais")
    try:
        nombre = pedir_texto_no_vacio("Ingrese el nombre del pais: ").strip()
        pais = buscar_pais_exacto(paises, nombre)

        if pais is None:
            mostrar_advertencia("Volviendo al menú principal.")
            return False

        mostrar_info("Pais encontrado:")
        console.print(formatear_pais(pais))
        while True:
            opcion = questionary.select(
                message="Elija la acción a realizar:",
                choices=["Modificar población", "Modificar superficie", "Modificar ambos", "Salir"]
            ).ask()

            if opcion == "Salir":
                mostrar_advertencia("No se realizaron cambios.")
                return True
            elif opcion == "Modificar población":
                pais["poblacion"] = pedir_entero("Ingrese la nueva poblacion o 's' para salir: ", 1)
            elif opcion == "Modificar superficie":
                pais["superficie"] = pedir_entero("Ingrese la nueva superficie en km2 o 's' para salir: ", 1)
            elif opcion == "Modificar ambos":
                pais["poblacion"] = pedir_entero("Ingrese la nueva poblacion o 's' para salir: ", 1)
                pais["superficie"] = pedir_entero("Ingrese la nueva superficie en km2 o 's' para salir: ", 1)

            guardar_paises(paises)
            mostrar_exito("Datos actualizados correctamente.")
            return True
    except SaliendoAlMenuError as e:
        mostrar_advertencia(str(e))
        return False


def filtrar_por_continente(paises, continente):
    continente_buscado = normalizar_texto(continente).lower()
    return [pais for pais in paises if normalizar_texto(pais["continente"]).lower() == continente_buscado]


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
                    nombre_actual = normalizar_texto(paises_ordenados[j]["nombre"]).lower()
                    nombre_siguiente = normalizar_texto(paises_ordenados[j+1]["nombre"]).lower()
                    if nombre_actual > nombre_siguiente:
                        paises_ordenados[j], paises_ordenados[j+1] = paises_ordenados[j+1], paises_ordenados[j]

        elif as_des == "Descendente":
            for i in range(n - 1):
                for j in range(n - 1 - i):
                    nombre_actual = normalizar_texto(paises_ordenados[j]["nombre"]).lower()
                    nombre_siguiente = normalizar_texto(paises_ordenados[j+1]["nombre"]).lower()
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
    poblacion = f"{pais['poblacion']:,}".replace(",", ".")
    superficie = f"{pais['superficie']:,}".replace(",", ".")
    return (
        f"Nombre: {pais['nombre']} | "
        f"Poblacion: {poblacion} | "
        f"Superficie: {superficie} km2 | "
        f"Continente: {pais['continente']}"
    )


def mostrar_paises(paises, titulo="Listado de paises"):
    mostrar_titulo(titulo)
    if not paises:
        mostrar_advertencia("No hay paises para mostrar.")
        return

    tabla = Table(show_header=True, header_style="bold blue")
    tabla.add_column("#", justify="right", style="cyan", no_wrap=True)
    tabla.add_column("Nombre", style="bold white")
    tabla.add_column("Poblacion", justify="right", style="green")
    tabla.add_column("Superficie (km2)", justify="right", style="magenta")
    tabla.add_column("Continente", style="yellow")

    for indice, pais in enumerate(paises, start=1):
        tabla.add_row(
            str(indice),
            pais["nombre"],
            f"{pais['poblacion']:,}".replace(",", "."),
            f"{pais['superficie']:,}".replace(",", "."),
            pais["continente"],
        )

    console.print(tabla)


def pedir_rango(mensaje_minimo, mensaje_maximo):
    while True:
        minimo = pedir_entero(mensaje_minimo, 1)
        maximo = pedir_entero(mensaje_maximo, 1)
        if minimo <= maximo:
            return minimo, maximo
        mostrar_error("Error: el valor minimo no puede ser mayor que el maximo.")


def mostrar_estadisticas(paises):
    estadisticas = obtener_estadisticas(paises)
    mostrar_titulo("Estadisticas")

    if estadisticas is None:
        mostrar_advertencia("No hay datos para calcular estadisticas.")
        return

    console.print(
        Panel.fit(
            formatear_pais(estadisticas["mayor_poblacion"]),
            title="Pais con mayor poblacion",
            border_style="green",
        )
    )
    console.print(
        Panel.fit(
            formatear_pais(estadisticas["menor_poblacion"]),
            title="Pais con menor poblacion",
            border_style="yellow",
        )
    )

    tabla_resumen = Table(show_header=True, header_style="bold blue")
    tabla_resumen.add_column("Indicador", style="cyan")
    tabla_resumen.add_column("Valor", justify="right", style="bold white")
    tabla_resumen.add_row(
        "Promedio de poblacion",
        f"{estadisticas['promedio_poblacion']:, .2f}".replace(",", "X").replace(".", ",").replace("X", "."),
    )
    tabla_resumen.add_row(
        "Promedio de superficie",
        f"{estadisticas['promedio_superficie']:, .2f}".replace(",", "X").replace(".", ",").replace("X", "."),
    )
    console.print(tabla_resumen)

    tabla_continentes = Table(title="Cantidad de paises por continente", header_style="bold blue")
    tabla_continentes.add_column("Continente", style="yellow")
    tabla_continentes.add_column("Cantidad", justify="right", style="green")
    for continente, cantidad in estadisticas["cantidad_por_continente"].items():
        tabla_continentes.add_row(continente, str(cantidad))
    console.print(tabla_continentes)
    pausar()
    limpiar_pantalla()


def menu_busqueda(paises):
    mostrar_titulo("Buscar pais por nombre")
    try:
        nombre = pedir_texto_no_vacio("Ingrese el nombre o parte del nombre: ")
        resultados = buscar_pais_por_nombre(paises, nombre)
        if not resultados:
            mostrar_advertencia("No se encontraron paises con esa busqueda.")
            return

        mostrar_paises(resultados, "Resultados de la busqueda")
    except SaliendoAlMenuError as e:
        mostrar_advertencia(str(e))


def menu_filtros(paises):
    while True:
        mostrar_titulo("[bold blue]Filtros[/bold blue]")
        opcion = questionary.select(
            message="Elija el método de ordenamiento: ",
            choices=["Filtrar por continente", "Filtrar por rango de poblacion", "Filtrar por rango de superficie", "Salir"]
            ).ask()
        mostrar_info(f"Elegiste: {opcion}")
        try:
            if opcion == "Filtrar por continente":
                continente = pedir_texto_no_vacio("Ingrese el continente: ")
                resultados = filtrar_por_continente(paises, continente)
                if resultados:
                    mostrar_paises(resultados, f"Paises del continente {continente}")
                else:
                    mostrar_advertencia("No se encontraron paises para ese continente.")
                pausar()
                limpiar_pantalla()
            elif opcion == "Filtrar por rango de poblacion":
                minimo, maximo = pedir_rango(
                    "Ingrese la poblacion minima: ",
                    "Ingrese la poblacion maxima: ",
                )
                resultados = filtrar_por_rango_poblacion(paises, minimo, maximo)
                if resultados:
                    mostrar_paises(resultados, "Paises filtrados por poblacion")
                else:
                    mostrar_advertencia("No se encontraron paises en ese rango de poblacion.")
                pausar()
                limpiar_pantalla()
            elif opcion == "Filtrar por rango de superficie":
                minimo, maximo = pedir_rango(
                    "Ingrese la superficie minima: ",
                    "Ingrese la superficie maxima: ",
                )
                resultados = filtrar_por_rango_superficie(paises, minimo, maximo)
                if resultados:
                    mostrar_paises(resultados, "Paises filtrados por superficie")
                else:
                    mostrar_advertencia("No se encontraron paises en ese rango de superficie.")
                pausar()
                limpiar_pantalla()
            elif opcion == "Salir":
                break
        except SaliendoAlMenuError as e:
            mostrar_advertencia(str(e))

def menu_ordenamientos(paises):
    try:
        while True:
            mostrar_titulo("Ordenamientos")
            opcion = questionary.select(
            message="Elija el método de ordenamiento: ",
            choices=["Por nombre", "Por poblacion","Por superficie", "Salir"]
            ).ask()
            mostrar_info(f"Elegiste: {opcion}")

            if opcion == "Salir":
                raise SaliendoAlMenuError("Saliendo al menú principal.")

            else:
                as_des = questionary.select(
                message="Elija Ascendente o Descendente:",
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
    except SaliendoAlMenuError as e:
        mostrar_advertencia(str(e))
        pausar()
        limpiar_pantalla()


def mostrar_menu_principal():
    mostrar_titulo("Gestion de Datos de Paises")
    opcion = questionary.select(
    message="Seleccioná:",
    choices=["Mostrar todos los paises", "Agregar un pais", "Actualizar poblacion y superficie",
             "Buscar pais por nombre", "Filtrar paises", "Ordenar paises", "Mostrar estadisticas", "Salir"]
            ).ask()
    return opcion


def main():
    paises, lineas_invalidas = cargar_paises()

    if lineas_invalidas > 0:
        mostrar_advertencia(
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
            limpiar_pantalla()
        elif opcion == "Filtrar paises":
            menu_filtros(paises)
            pausar()
            limpiar_pantalla()
        elif opcion == "Ordenar paises":
            menu_ordenamientos(paises)
        elif opcion == "Mostrar estadisticas":
            mostrar_estadisticas(paises)
        elif opcion == "Salir":
            mostrar_info("Programa finalizado.")
            break

def limpiar_pantalla():
    console.clear()