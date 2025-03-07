
import pandas as pd
import yfinance as yf
import time

start_time = time.time()

print(f"Empezando en {time.time() - start_time:.2f}.")

# Leer los tickers desde el archivo
df=pd.read_csv("tickers/sp500x.txt")
tickers = df["0"].to_list()
#df = pd.read_csv('sp500.txt', delimiter='\t', on_bad_lines='skip')
#tickers = df["Symbol"].to_list()[:20]

inactive_tickers = pd.read_csv("tickers/inactive_tickers.txt")
in_tickers = inactive_tickers["0"].to_list()
tickers = [ticker for ticker in tickers if ticker not in in_tickers]


# Funcion para mostrar una barra de progreso
def mostrar_progreso(actual, total, largo_barra=30):
    progreso = actual / total
    longitud_completada = int(largo_barra * progreso)
    barra = "=" * longitud_completada + "-" * (largo_barra - longitud_completada)
    porcentaje = progreso * 100
    print(f"\r[{barra}] {porcentaje:.2f}%", end="", flush=True)


# Obtener informacion financiera junto con el sector con barra de progreso
def obtener_informacion_financiera(tickers):
    info_financiera = {}
    total_tickers = len(tickers)
    tickers_verificados = 0

    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            if not info:
                raise ValueError("No data fetched")
            
            # Formatear los valores con comas como separadores de miles
            revenue = info.get("totalRevenue", 0)
            net_income = info.get("netIncomeToCommon", 0)
            ebitda = info.get("ebitda", 0)
            revenue_growth = info.get("revenueGrowth", 0)
            profit_margin = info.get("profitMargins", 0) * 100  # Convertir a porcentaje
            operating_margin = info.get("operatingMargins", 0) * 100  # Convertir a porcentaje
            roe = info.get("returnOnEquity", 0) * 100  # Convertir a porcentaje
            
            # Colocar las columnas "Revenue", "Net Income" y "EBITDA" al final
            info_financiera[ticker] = {
                "Nombre": info.get("longName", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "P/E": info.get("trailingPE", 0),
                "EPS": info.get("trailingEps", 0),
                "BV": info.get("bookValue", 0),
                "Div Yld": info.get("dividendYield", 0),
                "Div/Sh": info.get("dividendRate", 0),
                "D/E": info.get("debtToEquity", 0),
                "Beta": info.get("beta", 0),
                "Profit Margin": f"{profit_margin:,.2f}%",  # Formato porcentaje
                "Operating Margin": f"{operating_margin:,.2f}%",  # Formato porcentaje
                "Revenue Growth": f"{revenue_growth * 100:,.2f}%",  # Formato con comas, con porcentaje
                "ROE": info.get("returnOnEquity", 0),
                "Vol": info.get("fiftyDayAverage", 0),
                
                # ultimas columnas
                "Revenue": f"{revenue:,.0f}",  # Formato con comas
                "Net Income": f"{net_income:,.0f}",  # Formato con comas
                "EBITDA": f"{ebitda:,.0f}",  # Formato con comas
            }
        except Exception as e:
            pass  # Ignorar errores y continuar con el siguiente ticker

        tickers_verificados += 1
        mostrar_progreso(tickers_verificados, total_tickers)

    print()  # Salto de linea al terminar
    return info_financiera

def evaluar_inversion(ticker, data):
    puntaje = 0

    # Evaluar P/E (Price-to-Earnings)
    pe = data.get("P/E", 0)
    try:
        pe = float(pe)  # Asegurarse de que P/E sea un número
    except ValueError:
        pe = 0  # Si no puede convertirse, se asigna 0

    if pe < 15:  # P/E bajo, indicativo de acción barata
        puntaje += 2
    elif pe < 35:
        puntaje += 1
    else:
        puntaje -= 1

    # Evaluar EPS (Earnings Per Share)
    eps = data.get("EPS", 0)
    try:
        eps = float(eps)  # Asegurarse de que EPS sea un número
    except ValueError:
        eps = 0  # Si no puede convertirse, se asigna 0

    if eps > 30:  # EPS extremadamente alto
        puntaje += 4
    elif eps > 15:  # EPS entre 15 y 30
        puntaje += 3
    elif eps > 5:  # EPS entre 5 y 15
        puntaje += 2
    elif eps > 2:  # EPS entre 2 y 5
        puntaje += 1
    elif eps > 0:  # EPS positivo, pero menor a 2
        puntaje += 0
    else:  # EPS negativo o cero
        puntaje -= 2

    # Evaluar ROE (Return on Equity)
    roe = data.get("ROE", 0)
    try:
        roe = float(roe)  # Asegurarse de que ROE sea un número
    except ValueError:
        roe = 0  # Si no puede convertirse, se asigna 0

    if roe > 0.30:  # ROE alto
        puntaje += 2
    elif roe > 0.2:
        puntaje += 1
    else:
        puntaje -= 1

    # Evaluar D/E (Debt-to-Equity)
    de = data.get("D/E", 0)
    try:
        de = float(de)  # Asegurarse de que D/E sea un número
    except ValueError:
        de = 0  # Si no puede convertirse, se asigna 0

    if de < 1:  # Baja deuda
        puntaje += 2
    elif de < 2:
        puntaje += 1
    else:
        puntaje -= 2

    # Evaluar Beta (Volatilidad)
    beta = data.get("Beta", 0)
    try:
        beta = float(beta)  # Asegurarse de que Beta sea un número
    except ValueError:
        beta = 0  # Si no puede convertirse, se asigna 0

    if beta < 1:  # Baja volatilidad
        puntaje += 2
    elif beta < 1.5:
        puntaje += 1
    else:
        puntaje -= 1

    # Evaluar ROI (Return on Investment)
    roi = data.get("ROI", 0)
    try:
        roi = float(roi)  # Asegurarse de que ROI sea un número
    except ValueError:
        roi = 0  # Si no puede convertirse, se asigna 0

    if roi > 15:  # ROI alto
        puntaje += 2
    elif roi > 5:
        puntaje += 1
    else:
        puntaje -= 1

    return puntaje

# Funcion para dividir la lista de tickers en bloques
def dividir_tickers_en_bloques(tickers, tamano_bloque=100):
    """Divide una lista de tickers en bloques de un tamaño especifico."""
    for i in range(0, len(tickers), tamano_bloque):
        yield tickers[i:i + tamano_bloque]

# FUNCIONES DE HTML #

def escribir_encabezado_html(f, bloque_id):
    """Escribe el encabezado basico del archivo HTML con estilo."""
    encabezado_html = f'''
    <h1>Informacion Financiera - Bloque {bloque_id}</h1>
    <html><head><style>
        table {{border-collapse: collapse; width: 100%;}} 
        th, td {{border: 1px solid black; padding: 5px;}} 
        th {{background-color: #f2f2f2;}} 
        a {{color: blue; text-decoration: none; font-weight: bold;}}
    </style></head><body id="top">
    '''
    f.write(encabezado_html)

def agregar_busqueda_y_script(f):
    """Agrega el campo de busqueda y el script para ordenar y filtrar las tablas."""
    busqueda_y_script = """
    <label for="search">Buscar en la tabla:</label>
    <input type="text" id="search" onkeyup="filterTable()" placeholder="Buscar...">
    <br><br>

    <script>
    document.addEventListener('DOMContentLoaded', function () {
    const tables = document.querySelectorAll("table");

    tables.forEach(function (table) {
        const headers = table.querySelectorAll("th");

        headers.forEach(function (header, index) {
            // Inicializamos el estado del orden en ascendente
            let sortOrder = true;

            header.addEventListener('click', function () {
                sortTable(table, index, sortOrder);
                // Alternamos el orden para la proxima vez
                sortOrder = !sortOrder;
            });
        });
    });

    function sortTable(table, colIndex, ascending) {
        const rows = Array.from(table.rows).slice(1); // Excluir la fila de los encabezados

        // Ordenar las filas usando la funcion de comparacion optimizada
        rows.sort(function (rowA, rowB) {
            const cellA = rowA.cells[colIndex].textContent.trim();
            const cellB = rowB.cells[colIndex].textContent.trim();

            const valueA = parseValue(cellA);
            const valueB = parseValue(cellB);

            if (!isNaN(valueA) && !isNaN(valueB)) {
                // Orden numerico
                return ascending ? valueA - valueB : valueB - valueA;
            } else {
                // Orden alfabetico
                return ascending ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
            }
        });

        // Usar documentFragment para manipular el DOM de manera eficiente
        const fragment = document.createDocumentFragment();
        rows.forEach(function (row) {
            fragment.appendChild(row); // Agregar filas al fragmento
        });

        // Añadir todas las filas reordenadas de una vez al DOM
        table.appendChild(fragment);
    }

    function parseValue(value) {
        // Eliminar comas y convertir a float
        return parseFloat(value.replace(/,/g, '').replace('%', '').trim());
    }

    window.filterTable = function () {
        const input = document.getElementById("search");
        const filter = input.value.toLowerCase();
        const rows = document.querySelectorAll("table tr");

        rows.forEach(function (row, index) {
            if (index === 0) return;  // Ignorar la primera fila (encabezados)

            const cells = row.querySelectorAll("td");
            let found = false;

            cells.forEach(function (cell) {
                if (cell.textContent.toLowerCase().includes(filter)) {
                    found = true;
                }
            });

            row.style.display = found ? "" : "none";
        });
    };

    // Funcion para copiar la tabla al portapapeles
    window.copyTableToClipboard = function (tableId) {
        const table = document.getElementById(tableId);
        let range, selection;

        if (document.body.createTextRange) {  // Para IE
            range = document.body.createTextRange();
            range.moveToElementText(table);
            range.select();
            document.execCommand('copy');
        } else if (window.getSelection) {  // Para otros navegadores
            selection = window.getSelection();
            range = document.createRange();
            range.selectNodeContents(table);
            selection.removeAllRanges();
            selection.addRange(range);
            document.execCommand('copy');
        }

        alert("Tabla copiada al portapapeles");
    };
});

    </script>

    """
    f.write(busqueda_y_script)

def agregar_vinculo_volver_inicio(f):
    """Agrega un enlace para volver al inicio de la pagina."""
    f.write('<br><a href="#top">Volver al inicio</a><br><br>')


# TERMINA FUNCIONES DE HTML

def generar_html_por_bloques(info_financiera, bloque_id):
    """Genera un archivo HTML para un bloque especifico de tickers con un indice."""
    html_filename = f'sp500_{bloque_id}.html'
    sectores = {}

    # Agrupar por sector
    for ticker, data in info_financiera.items():
        sector = data.get("Sector", "N/A")
        if sector != "N/A":  # Omitir sectores "N/A"
            if sector not in sectores:
                sectores[sector] = []
            sectores[sector].append((ticker, data))

    with open(html_filename, 'w', encoding='utf-8') as f:
        # Escribir encabezado HTML
        escribir_encabezado_html(f, bloque_id)

        # Agregar campo de busqueda y script
        agregar_busqueda_y_script(f)

        # Generar indice de sectores
        f.write('<h2>indice de Sectores</h2><ul>')
        for sector in sectores.keys():
            f.write(f'<li><a href="#{sector.replace(" ", "_")}">{sector}</a></li>')
        f.write('</ul>')

        # Crear una tabla por cada sector
        for sector, tickers in sectores.items():
            # Anclaje para cada sector
            f.write(f'<h2 id="{sector.replace(" ", "_")}">{sector} Sector</h2>')
            f.write(f'<button onclick="copyTableToClipboard(\'table_{sector.replace(" ", "_")}\')">Copiar tabla</button><br><br>')

            # Crear la tabla
            f.write(f'<table id="table_{sector.replace(" ", "_")}"><tr><th>Activo</th><th>Ticker</th>')

            # Agregar encabezados de informacion financiera
            financial_headers = [
                "P/E", 
                "EPS", 
                "BV", 
                "Div Yld", 
                "Div/Sh", 
                "D/E", 
                "Beta", 
                "Profit Margin", 
                "Operating Margin", 
                "Revenue Growth",  
                'ROE',
                "Vol", 
                "Revenue",  # Colocada al final
                "Net Income",  # Colocada al final
                "EBITDA",  # Colocada al final
                "Puntaje"
            ]

            for header in financial_headers:
                f.write(f'<th>{header}</th>')

            f.write('</tr>')

            # Agregar filas con informacion financiera
            for ticker, data in tickers:
                puntaje = evaluar_inversion(ticker, data)  # Obtener el puntaje

                f.write(f'<tr><td>{data["Nombre"]}</td>')
                # Agregar hipervinculo para el ticker
                f.write(f'<td><a href="https://finance.yahoo.com/quote/{ticker}" target="_blank">{ticker}</a></td>')

                # Agregar valores financieros
                for key in financial_headers[:-1]:  # Excluimos la columna de "Puntaje"
                    valor = data.get(key, 'N/A')
                    if valor != 'N/A':  # Omitir celdas con "N/A"
                        if isinstance(valor, (int, float)):  # Si el valor es numerico
                            f.write(f'<td>{valor:.2f}</td>')
                        else:  # Si el valor no es numerico
                            f.write(f'<td>{valor}</td>')
                    else:
                        f.write('<td></td>')  # Dejar la celda vacia
                
                # Agregar el puntaje calculado
                f.write(f'<td>{puntaje}</td>')

                f.write('</tr>')

            f.write('</table><br><br>')

            # Agregar el vinculo para volver al inicio
            agregar_vinculo_volver_inicio(f)

        f.write('</body></html>')

    print(f"Archivo generado: {html_filename}")


# Procesar la lista completa de tickers y exportar en bloques
def procesar_tickers_en_bloques(tickers, tamano_bloque=100):
    """Procesa tickers en bloques, obteniendo su informacion financiera y generando archivos HTML por bloque."""
    bloques = dividir_tickers_en_bloques(tickers, tamano_bloque)
    
    total_bloques = (len(tickers) + tamano_bloque - 1) // tamano_bloque
    for bloque_id, bloque in enumerate(bloques, start=1):
        print(f"\nProcesando bloque {bloque_id} de {total_bloques}...")
        info_financiera = obtener_informacion_financiera(bloque)
        generar_html_por_bloques(info_financiera, bloque_id)

# Ejemplo de uso
procesar_tickers_en_bloques(tickers, tamano_bloque=8000)

print(f"Codigo finalizado en {time.time() - start_time:.2f}.")
