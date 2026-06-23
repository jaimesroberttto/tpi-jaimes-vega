# Trabajo Practico Integrador

## Gestion de Datos de Paises en Python

Este proyecto fue desarrollado para la materia Programacion 1 de la Tecnicatura Universitaria en Programacion a Distancia.

El sistema permite gestionar informacion de paises a partir de un archivo CSV, aplicando listas, diccionarios, funciones, filtros, ordenamientos y estadisticas.

## Objetivo del programa

Desarrollar una aplicacion en Python que permita:

- Leer datos de paises desde un archivo CSV.
- Agregar nuevos paises.
- Actualizar datos existentes.
- Buscar paises por nombre.
- Filtrar informacion por distintos criterios.
- Ordenar los datos.
- Mostrar estadisticas generales del dataset.

## Estructura del proyecto

El proyecto contiene los siguientes archivos:

- `tp-integrador/main_paises.py`: menu principal del sistema.
- `tp-integrador/funciones_paises.py`: funciones auxiliares, validaciones, manejo de CSV, filtros, ordenamientos y estadisticas.
- `tp-integrador/paises.csv`: dataset base con los paises.
- `README.md`: descripcion general e instrucciones de uso.
- `tp-integrador/Documentacion academica.pdf`: explicación técnica de los conceptos utilizados y proceso de realización del código.

## Datos del CSV

Cada diccionario de pais se almacena con los siguientes campos en un csv separado por comas:

- `nombre`
- `poblacion`
- `superficie`
- `continente`

Ejemplo de una fila del archivo:

```csv
Argentina,45376763,2780400,America
```

## Requisitos

- Python 3.x
- pip
- Librerias externas:
  - `rich`
  - `questionary`

Instalacion sugerida:

```bash
pip install rich questionary
```

## Instrucciones de uso

1. Abrir una terminal en la carpeta `tp-integrador`.
2. Ejecutar el archivo principal.
3. Elegir una opcion del menu utilizando las flechas y dando enter.

Comando de ejecucion:

```bash
python3 tp-integrador/main_paises.py
```

## Funcionalidades implementadas

El sistema permite:

1. Mostrar todos los paises cargados.
2. Agregar un pais con validacion de campos.
3. Actualizar poblacion y superficie de un pais.
4. Buscar un pais con coincidencia parcial.
5. Filtrar paises por:
   - continente
   - rango de poblacion
   - rango de superficie
6. Ordenar paises de forma ascendente o descendente por:
   - nombre
   - poblacion
   - superficie
7. Mostrar estadisticas:
   - pais con mayor poblacion
   - pais con menor poblacion
   - promedio de poblacion
   - promedio de superficie
   - cantidad de paises por continente

## Validaciones y manejo de errores

El programa incluye:

- Validacion para evitar campos vacios.
- Validacion para tildes y caracteres especiales.
- Validacion de numeros enteros positivos en poblacion y superficie.
- Mensajes claros cuando una busqueda no arroja resultados.
- Control de rangos invalidos en filtros.
- Lectura segura del CSV, ignorando lineas invalidas sin detener la ejecucion.

## Ejemplo de uso

### Mostrar paises

```text
1. Nombre: Argentina | Poblacion: 45376763 | Superficie: 2780400 km2 | Continente: America
2. Nombre: Brasil | Poblacion: 213993437 | Superficie: 8515767 km2 | Continente: America
```

### Estadisticas

```text
Pais con mayor poblacion:
Nombre: India | Poblacion: 1428627663 | Superficie: 3287263 km2 | Continente: Asia

Promedio de poblacion: 233801388.22
Promedio de superficie: 2808332.56
```

## Decisiones tecnicas

- Se utilizo una lista de diccionarios para representar los paises en memoria.
- Se utilizo el modulo `csv` para leer y escribir el archivo de datos.
- Se utilizo `os.path` para ubicar el archivo CSV en la misma carpeta del proyecto.
- El programa fue dividido en un archivo principal y un archivo de funciones para mejorar la modularidad.
- Se implementaron funciones como `normalizar_texto` para validar y normalizar entradas.
- Se utilizaron las librerias `rich` y `questionary` para mejorar la experiencia en consola.
- Los ordenamientos se resolvieron con logica propia sobre la lista de paises.

## Participacion de integrantes

- Integrante 1: Roberto Moises Jaimes
- Integrante 2: Gabriel Damian Vega

## Link del video

- Video demostrativo: __________________

## Link de la documentacion en PDF

- Informe PDF: __________________
