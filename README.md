# Stock Data Scraper (yahoo_webscrapper_v0.1.py)

Este script extrae datos financieros de Yahoo Finance y los guarda en un archivo Excel con diferentes pestañas para cada categoría de datos.

## Funcionalidades
- Obtiene información de las siguientes categorías de acciones:
  - Penny Stocks
  - Gainers (acciones en alza)
  - Losers (acciones en baja)
  - Most Active (acciones más activas)
- Recorre hasta 125 registros por categoría en bloques de 25.
- Muestra una barra de progreso en la terminal durante la extracción de datos.
- Exporta los datos en un archivo `stocks_data.xlsx` con cada categoría en una hoja diferente.

## Requisitos
Este script utiliza las siguientes librerías de Python:
- `requests`
- `pandas`
- `BeautifulSoup4`
- `os`
- `time`

Asegúrate de que estas librerías estén instaladas antes de ejecutar el script. Puedes instalarlas con:
```sh
pip install requests pandas beautifulsoup4
```

## Uso
Para ejecutar el script, simplemente corre el siguiente comando en la terminal:
```sh
python script.py
```
El script automáticamente extraerá los datos y los guardará en `stocks_data.xlsx`.

## Estructura del Código
1. **`get_data_from_url(url)`**: Descarga y extrae datos de una tabla en la página web proporcionada.
2. **`fetch_data(name, base_url)`**: Itera a través de las páginas de una categoría específica y consolida los datos.
3. **`main()`**: Ejecuta todas las funciones, obtiene los datos de todas las categorías y los guarda en un archivo Excel.

## Salida
El archivo `stocks_data.xlsx` contendrá:
- **Penny Stocks** en una pestaña
- **Gainers** en otra pestaña
- **Losers** en otra pestaña
- **Most Active** en otra pestaña

Cada hoja tendrá una columna adicional `Ticker`, que extrae correctamente el símbolo de la acción.

## Notas
- Se ha incluido un `time.sleep(1)` para evitar bloqueos por exceso de solicitudes.
- Se recomienda no ejecutar el script repetidamente en cortos períodos de tiempo para evitar restricciones de Yahoo Finance.

