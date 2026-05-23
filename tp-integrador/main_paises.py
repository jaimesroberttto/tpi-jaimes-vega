from funciones_paises import *

def menu_busqueda(paises):
    print("\n--- Buscar pais por nombre ---")
    nombre = pedir_texto_no_vacio("Ingrese el nombre o parte del nombre: ")
    resultados = buscar_pais_por_nombre(paises, nombre)

    if not resultados:
        print("No se encontraron paises con esa busqueda.")
        return

    mostrar_paises(resultados, "Resultados de la busqueda")


def menu_filtros(paises):
    while True:
        print("\n--- Filtros ---")
        print("1. Filtrar por continente")
        print("2. Filtrar por rango de poblacion")
        print("3. Filtrar por rango de superficie")
        print("4. Volver")
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


def menu_ordenamientos(paises):
    while True:
        print("\n--- Ordenamientos ---")
        print("1. Ordenar por nombre ascendente")
        print("2. Ordenar por nombre descendente")
        print("3. Ordenar por poblacion ascendente")
        print("4. Ordenar por poblacion descendente")
        print("5. Ordenar por superficie ascendente")
        print("6. Ordenar por superficie descendente")
        print("7. Volver")
        opcion = pedir_opcion(1, 7)

        if opcion == 1:
            mostrar_paises(ordenar_paises(paises, "nombre"), "Paises ordenados por nombre")
            pausar()
        elif opcion == 2:
            mostrar_paises(
                ordenar_paises(paises, "nombre", True),
                "Paises ordenados por nombre descendente",
            )
            pausar()
        elif opcion == 3:
            mostrar_paises(
                ordenar_paises(paises, "poblacion"),
                "Paises ordenados por poblacion",
            )
            pausar()
        elif opcion == 4:
            mostrar_paises(
                ordenar_paises(paises, "poblacion", True),
                "Paises ordenados por poblacion descendente",
            )
            pausar()
        elif opcion == 5:
            mostrar_paises(
                ordenar_paises(paises, "superficie"),
                "Paises ordenados por superficie",
            )
            pausar()
        elif opcion == 6:
            mostrar_paises(
                ordenar_paises(paises, "superficie", True),
                "Paises ordenados por superficie descendente",
            )
            pausar()
        else:
            break


def mostrar_menu_principal():
    print("\n=== Gestion de Datos de Paises ===")
    print("1. Mostrar todos los paises")
    print("2. Agregar un pais")
    print("3. Actualizar poblacion y superficie")
    print("4. Buscar pais por nombre")
    print("5. Filtrar paises")
    print("6. Ordenar paises")
    print("7. Mostrar estadisticas")
    print("8. Salir")


def main():
    paises, lineas_invalidas = cargar_paises()

    if lineas_invalidas > 0:
        print(
            f"Advertencia: se ignoraron {lineas_invalidas} lineas invalidas del archivo CSV."
        )

    while True:
        mostrar_menu_principal()
        opcion = pedir_opcion(1, 8)

        if opcion == 1:
            mostrar_paises(paises, "Listado completo de paises")
            pausar()
        elif opcion == 2:
            agregar_pais(paises)
            pausar()
        elif opcion == 3:
            actualizar_pais(paises)
            pausar()
        elif opcion == 4:
            menu_busqueda(paises)
            pausar()
        elif opcion == 5:
            menu_filtros(paises)
        elif opcion == 6:
            menu_ordenamientos(paises)
        elif opcion == 7:
            mostrar_estadisticas(paises)
            pausar()
        else:
            print("Programa finalizado.")
            break


main()
