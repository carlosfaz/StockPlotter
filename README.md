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
python yahoo_webscrapper_v0.1.py
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

##############################################################################################################################################################################################################################################



# Stock Financial Analysis Tool (tabulador_excel.py)

Este script obtiene información financiera de empresas listadas en el mercado utilizando Yahoo Finance y la guarda en un archivo Excel organizado por sectores.

## Funcionalidades
- Obtiene información financiera de múltiples tickers de un archivo de texto.
- Filtra y elimina tickers inactivos.
- Calcula métricas clave como:
  - Revenue, Net Income, EBITDA
  - ROE, ROA, P/E, P/B, P/S
  - Márgenes de beneficio y operativos
  - Relación deuda/capital (D/E)
  - Ratios financieros como Current Ratio y Quick Ratio
  - Cobertura de intereses y PEG Ratio
- Asigna puntajes a cada empresa en función de sus métricas.
- Organiza los datos en un archivo Excel con pestañas por sector y una consolidada.
- Muestra una barra de progreso en la terminal.

## Requisitos
Este script utiliza las siguientes librerías de Python:
- `pandas`
- `yfinance`
- `time`

Asegúrate de que estas librerías estén instaladas antes de ejecutar el script. Puedes instalarlas con:
```sh
pip install pandas yfinance
```

## Uso
Para ejecutar el script, simplemente corre el siguiente comando en la terminal:
```sh
python tabulador_excel.py
```
El script leerá los tickers desde `tickers/sp500x.txt`, eliminará los inactivos desde `tickers/inactive_tickers.txt`, y procesará los datos.

## Estructura del Código
1. **Lectura de Tickers**: Carga los tickers desde un archivo de texto y excluye los inactivos.
2. **`obtener_informacion_financiera(tickers)`**: Obtiene métricas clave para cada empresa desde Yahoo Finance.
3. **Puntaje de Empresas**: Se asigna un puntaje en función de métricas financieras clave.
4. **`exportar_a_excel(info_financiera, filename)`**: Guarda los datos en un archivo Excel con pestañas por sector y una consolidada.
5. **Ejecución del proceso**: Se muestra una barra de progreso en la terminal mientras se procesan los tickers.

## Salida
El archivo Excel generado contiene:
- **Una pestaña por sector**, donde se agrupan las empresas según su industria.
- **Una pestaña consolidada** con todos los datos de las empresas.

Cada hoja incluye métricas clave junto con el puntaje total asignado.

## Notas
- Se ha incluido un `time.sleep(1)` para evitar bloqueos por exceso de solicitudes.
- El nombre del archivo Excel incluye la fecha actual para diferenciar ejecuciones.
- La función `sanitizar_nombre(nombre)` evita errores en los nombres de las hojas de Excel.



