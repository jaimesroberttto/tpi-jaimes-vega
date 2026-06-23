'''Este módulo contiene funciones relacionadas con la gestión de datos de países, incluyendo la carga y guardado de datos en un archivo CSV, 
la validación de datos, la búsqueda, filtrado y ordenamiento de países, y la presentación de información en la consola utilizando la biblioteca rich.
El módulo también define excepciones personalizadas para manejar errores específicos relacionados con nombres incorrectos y la salida al menú principal.
Las funciones incluidas en este módulo permiten al usuario interactuar con una lista de países, realizar operaciones de búsqueda, filtrado y ordenamiento, 
y obtener estadísticas sobre los países almacenados en el sistema.'''
import csv
import os
import questionary
import unicodedata
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

'''Se definen constantes para la ruta del archivo CSV y los campos que se utilizarán en el archivo. 
También se crea una instancia de Console de la biblioteca rich para mostrar mensajes con estilos en la consola.'''
CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA_ACTUAL, "paises.csv")
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]
console = Console()

'''Se definen dos clases de excepciones personalizadas para manejar errores específicos relacionados con nombres incorrectos y la salida al menú principal.'''
class NombreErroneoError(Exception):
    pass
class SaliendoAlMenuError(Exception):
    pass

'''Se definen varias funciones para validar el continente, crear un archivo CSV base con datos iniciales, normalizar texto, 
mostrar mensajes de error, advertencia, éxito e información, mostrar títulos, pedir texto no vacío y números enteros, 
cargar y guardar países desde el archivo CSV, pausar la ejecución, verificar la existencia de un país, buscar países por nombre, 
agregar y actualizar países, filtrar países por continente y rangos de población y superficie, ordenar países por diferentes criterios, 
obtener estadísticas sobre los países y mostrar los países en formato de tabla.'''
def validar_continente(continente):
    continentes = ["America", "Europa", "Asia", "Africa", "Oceania"]
    if continente not in continentes:
        return None
    return continente

'''La función crear_csv_base() se encarga de crear un archivo CSV con datos iniciales de países si el archivo no existe. 
Esto asegura que el programa tenga datos para trabajar desde el principio.'''
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

'''La función normalizar_texto() se encarga de eliminar tildes y caracteres especiales de un texto, y de eliminar espacios adicionales. 
Esto es útil para asegurar que las comparaciones de texto sean consistentes, independientemente de cómo se'''
def normalizar_texto(texto):
    texto_sin_tildes = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return " ".join(texto_sin_tildes.strip().split())

'''La función normalizar_continente() utiliza la función normalizar_texto() para normalizar el nombre del continente y luego lo capitaliza. 
Esto asegura que los nombres de los continentes se almacenen de manera consistente en el sistema.'''
def normalizar_continente(texto):
    return normalizar_texto(texto).capitalize()

'''Las funciones mostrar_error(), mostrar_advertencia(), mostrar_exito() y mostrar_info() se encargan de mostrar mensajes con diferentes estilos y colores
 en la consola, utilizando la biblioteca rich. Esto mejora la experiencia del usuario al proporcionar retroalimentación visual clara 
 sobre el estado de las operaciones realizadas'''
def mostrar_error(mensaje):
    console.print(f"[bold red]{mensaje}[/bold red]")

'''La función mostrar_titulo() se encarga de mostrar un título con un estilo específico utilizando un panel de rich. 
Esto ayuda a destacar secciones importantes del programa, como los menús o los resultados de las operaciones'''
def mostrar_advertencia(mensaje):
    console.print(f"[bold yellow]{mensaje}[/bold yellow]")

'''La función pedir_texto_no_vacio() se encarga de solicitar al usuario que ingrese un texto que no esté vacío. 
Si el usuario ingresa "s" o "salir", se lanza una excepción para salir'''
def mostrar_exito(mensaje):
    console.print(f"[bold green]{mensaje}[/bold green]")

'''La función pedir_entero() se encarga de solicitar al usuario que ingrese un número entero, con la opción de especificar un valor mínimo. 
Si el usuario ingresa "s" o "salir", se lanza una excepción para salir'''
def mostrar_info(mensaje):
    console.print(f"[bold cyan]{mensaje}[/bold cyan]")

'''La función pedir_opcion() se encarga de solicitar al usuario que seleccione una opción dentro de un rango específico. 
Si el usuario ingresa una opción fuera del rango, se muestra un mensaje de error y se solicita'''
def mostrar_titulo(titulo):
    console.print(Panel.fit(titulo, border_style="bold blue"))

'''La función pedir_texto_no_vacio() se encarga de solicitar al usuario que ingrese un texto que no esté vacío. 
Si el usuario ingresa "s" o "salir", se lanza una excepción para salir al menú principal. Si el texto ingresado es válido, se devuelve el texto normalizado.'''
def pedir_texto_no_vacio(mensaje):
    while True:
        texto = normalizar_texto(input(mensaje))
        if texto.lower() == "s" or texto.lower() == "salir":
            raise SaliendoAlMenuError("Saliendo al menú principal.")
        elif texto != "":
            return texto
        else:
            mostrar_error("Error: el texto no puede estar vacío.")

'''La función pedir_entero() se encarga de solicitar al usuario que ingrese un número entero, con la opción de especificar un valor mínimo. 
Si el usuario ingresa "s" o "salir", se lanza una excepción para salir al menú principal. 
Si el número ingresado es válido y cumple con el requisito de ser mayor o igual al mínimo, se devuelve el número. 
Si el número ingresado no es válido o no cumple con el requisito, se muestra un mensaje de error y se solicita nuevamente.'''
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

'''La función pedir_opcion() se encarga de solicitar al usuario que seleccione una opción dentro de un rango específico. 
Si el usuario ingresa una opción fuera del rango, se muestra un mensaje de error y se solicita nuevamente hasta que se ingrese una opción válida.'''
def pedir_opcion(minimo, maximo):
    while True:
        opcion = pedir_entero("Seleccione una opcion: ")
        if minimo <= opcion <= maximo:
            return opcion
        mostrar_error(f"Error: debe elegir una opcion entre {minimo} y {maximo}.")

'''La función cargar_paises() se encarga de cargar los datos de los países desde el archivo CSV. Si el archivo no existe, se crea un archivo base 
con datos iniciales. La función lee el archivo CSV, normaliza los datos y los almacena en una lista de diccionarios. 
Si encuentra líneas inválidas en el archivo, las cuenta y las ignora, mostrando una advertencia al usuario. 
Finalmente, devuelve la lista de países cargados y la cantidad de líneas inválidas encontradas. 
Esto permite al programa manejar de manera robusta los datos del archivo CSV, asegurando que solo se trabajen con datos 
válidos y proporcionando retroalimentación sobre cualquier problema encontrado durante la carga.'''
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

'''La función guardar_paises() se encarga de guardar la lista de países en el archivo CSV. 
Toma la lista de países como argumento, abre el archivo CSV en modo escritura, y utiliza un DictWriter para escribir los datos de los países en el archivo.
Primero escribe la cabecera del archivo con los nombres de los campos, y luego escribe cada país como una fila en el archivo CSV. 
Esto permite que los cambios realizados en la lista de países se reflejen en el archivo CSV, asegurando que los datos se mantengan actualizados
y persistentes entre ejecuciones del programa.'''
def guardar_paises(paises):
    with open(RUTA_CSV, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        for pais in paises:
            escritor.writerow(pais)

'''La función pausar() se encarga de pausar la ejecución del programa y esperar a que el usuario presione Enter para continuar. 
Esto se utiliza para dar al usuario tiempo para leer los mensajes o resultados mostrados en la consola antes'''
def pausar():
    console.input("\n[bold cyan]Presione Enter para continuar...[/bold cyan]")

'''La función existe_pais() se encarga de verificar si un país con un nombre específico ya existe en la lista de países. 
Toma la lista de países y el nombre del país a buscar como argumentos, normaliza el nombre buscado y los nombres de los países en la lista, 
y devuelve True si encuentra una coincidencia exacta, o False si no encuentra ningún país con ese nombre.'''
def existe_pais(paises, nombre):
    nombre_buscado = normalizar_texto(nombre).lower()
    return any(normalizar_texto(pais["nombre"]).lower() == nombre_buscado for pais in paises)

'''La función buscar_pais_exacto() se encarga de buscar un país con un nombre específico en la lista de países. 
Toma la lista de países y el nombre del país a buscar como argumentos, y entra en un bucle que continúa hasta que encuentra un país con el 
nombre exacto o el usuario decide salir. Dentro del bucle, normaliza el nombre buscado y los nombres de los países en la lista, y si encuentra una coincidencia
 exacta, devuelve el país encontrado.'''
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

'''La función buscar_pais_por_nombre() se encarga de buscar países que contengan un texto específico en su nombre.
Toma la lista de países y el texto a buscar como argumentos, normaliza el texto buscado y los nombres de los países en la lista, 
y devuelve una lista de países que contienen el texto buscado en su nombre.'''
def buscar_pais_por_nombre(paises, nombre):
    nombre_buscado = normalizar_texto(nombre).lower()
    resultados = []
    for pais in paises:
        if nombre_buscado in normalizar_texto(pais["nombre"]).lower():
            resultados.append(pais)
    return resultados

'''La función agregar_pais() se encarga de agregar un nuevo país a la lista de países. Toma la lista de países como argumento, 
muestra un título para indicar que se está agregando un país, y luego solicita al usuario que ingrese el nombre, población, 
superficie y continente del nuevo país.La función realiza varias validaciones, como verificar que el nombre del país no esté vacío, que
el país no exista ya en la lista, que la población y superficie sean números enteros válidos, y que el continente sea válido. 
Si alguna de las validaciones falla, se muestra un mensaje de error y se solicita al usuario que ingrese nuevamente el dato correspondiente. 
Si todas las validaciones son exitosas, se crea un diccionario con los datos del nuevo país, se agrega a la lista de países, 
se guarda la lista actualizada en el archivo CSV, y se muestra un mensaje de éxito.'''
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

'''La función actualizar_pais() se encarga de actualizar los datos de un país existente en la lista de países. Toma la lista de países como argumento, 
muestra un título para indicar que se está actualizando un país, y luego solicita al usuario que ingrese el nombre del país a actualizar. 
Si el país no se encuentra, se muestra una advertencia y se vuelve al menú principal. Si el país se encuentra, se muestra la información del país y 
se solicita al usuario que elija qué dato desea modificar (población, superficie o ambos).'''
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

'''La función filtrar_por_continente() se encarga de filtrar la lista de países por un continente específico. 
Toma la lista de países y el continente a filtrar como argumentos, normaliza el nombre del continente buscado y los nombres de los 
continentes en la lista de países, y devuelve una lista de países que pertenecen al continente especificado. 
Esto permite al usuario obtener una lista de países que pertenecen a un continente específico, facilitando la búsqueda y análisis de los datos.'''
def filtrar_por_continente(paises, continente):
    continente_buscado = normalizar_texto(continente).lower()
    return [pais for pais in paises if normalizar_texto(pais["continente"]).lower() == continente_buscado]

'''La función filtrar_por_rango_poblacion() se encarga de filtrar la lista de países por un rango específico de población.'''
def filtrar_por_rango_poblacion(paises, minimo, maximo):
    return [pais for pais in paises if minimo <= pais["poblacion"] <= maximo]

'''La función filtrar_por_rango_superficie() se encarga de filtrar la lista de países por un rango específico de superficie.'''
def filtrar_por_rango_superficie(paises, minimo, maximo):
    return [pais for pais in paises if minimo <= pais["superficie"] <= maximo]

'''La función ordenar_paises() se encarga de ordenar la lista de países según un criterio específico (nombre, población o superficie) 
y un orden (ascendente o descendente). utiliza un algoritmo de ordenamiento de burbuja para ordenar la lista de países según el criterio y orden especificados.'''
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

'''La función formatear_pais() se encarga de formatear la información de un país en una cadena de texto con un formato específico. 
Toma un diccionario que representa un país como argumento, formatea la población y superficie con separ de miles, y devuelve una cadena de texto 
que muestra el nombre del país, su población, superficie y continente. Esto se utiliza para mostrar la información de los países de manera clara y 
legible en la consola'''
def formatear_pais(pais):
    poblacion = f"{pais['poblacion']:,}".replace(",", ".")
    superficie = f"{pais['superficie']:,}".replace(",", ".")
    return (
        f"Nombre: {pais['nombre']} | "
        f"Poblacion: {poblacion} | "
        f"Superficie: {superficie} km2 | "
        f"Continente: {pais['continente']}"
    )

'''La función mostrar_paises() se encarga de mostrar una lista de países en formato de tabla utilizando la biblioteca rich. 
Toma una lista de países y un título opcional como argumentos, y muestra la información de los países en una tabla con columnas para el 
número, nombre, población, superficie y continente. Si la lista de países está vacía, muestra una advertencia indicando que no hay países para mostrar.'''
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

'''La función pedir_rango() se encarga de solicitar al usuario que ingrese un rango de valores, con mensajes personalizados para el valor mínimo y máximo.
La función utiliza un bucle para solicitar ambos valores, asegurándose de que el valor mínimo sea menor o igual al valor máximo. 
Si el usuario ingresa un valor mínimo mayor que el máximo, se muestra un mensaje de error y se solicita nuevamente.'''
def pedir_rango(mensaje_minimo, mensaje_maximo):
    while True:
        minimo = pedir_entero(mensaje_minimo, 1)
        maximo = pedir_entero(mensaje_maximo, 1)
        if minimo <= maximo:
            return minimo, maximo
        mostrar_error("Error: el valor minimo no puede ser mayor que el maximo.")

'''La función mostrar_estadisticas() se encarga de mostrar estadísticas sobre la lista de países, incluyendo el país con mayor población, 
el país con menor población, el promedio de población, el promedio de superficie y la cantidad de países por continente.
Utiliza la función obtener_estadisticas() para calcular estas estadísticas, y luego muestra la información utilizando paneles y 
tablas de la biblioteca rich para mejorar la presentación visual. Si no hay datos para calcular las estadísticas, muestra una advertencia al usuario.'''
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
        f"{estadisticas['promedio_poblacion']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
    )
    tabla_resumen.add_row(
        "Promedio de superficie",
        f"{estadisticas['promedio_superficie']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
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

'''La función menu_busqueda() se encarga de mostrar un menú para buscar países por nombre. Toma la lista de países como argumento, 
muestra un título para indicar que se está realizando una búsqueda, y luego solicita al usuario que ingrese el nombre o parte del nombre del país a buscar.'''
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
    

'''La función menu_filtros() se encarga de mostrar un menú para filtrar países por diferentes criterios, como continente, 
rango de población o rango de superficie.'''
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
'''La función menu_ordenamientos() se encarga de mostrar un menú para ordenar la lista de países por diferentes criterios, como nombre, 
población o superficie, y en orden ascendente o descendente. Toma la lista de países como argumento, muestra un título para indicar 
que se está realizando un ordenamiento, y luego solicita al usuario que elija el criterio de ordenamiento y el orden (ascendente o descendente).
Luego, utiliza la función ordenar_paises() para ordenar la lista de países según las opciones seleccionadas, y muestra la lista ordenada utilizando 
la función mostrar_paises(). Si el usuario elige salir, se lanza una excepción para volver al menú principal.'''
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

'''La función mostrar_menu_principal() se encarga de mostrar el menú principal del programa utilizando la biblioteca questionary. 
Muestra un título para indicar que se está en la gestión de datos de países, y luego presenta una lista de opciones para que el usuario elija, 
como mostrar todos los países, agregar un país, actualizar datos, buscar por nombre, filtrar, ordenar, mostrar estadísticas o salir.'''
def mostrar_menu_principal():
    mostrar_titulo("Gestion de Datos de Paises")
    opcion = questionary.select(
    message="Seleccioná:",
    choices=["Mostrar todos los paises", "Agregar un pais", "Actualizar poblacion y superficie",
             "Buscar pais por nombre", "Filtrar paises", "Ordenar paises", "Mostrar estadisticas", "Salir"]
            ).ask()
    return opcion

'''La función main() es la función principal del programa que se encarga de cargar los datos de los países, mostrar el menú principal, 
y ejecutar las acciones correspondientes según la opción seleccionada por el usuario.Primero, carga los países desde el archivo CSV 
utilizando la función cargar_paises(), y si se encuentran líneas inválidas, muestra una advertencia al usuario. 
Luego, entra en un bucle que muestra el menú principal y espera a que el usuario seleccione una opción.'''
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
'''La función limpiar_pantalla() se encarga de limpiar la consola utilizando el método clear() del objeto console de la biblioteca rich. 
Esto se utiliza para mejorar la experiencia del usuario al mostrar solo la información relevante en cada momento, evitando
que la consola se llene de información acumulada.'''
def limpiar_pantalla():
    console.clear()
