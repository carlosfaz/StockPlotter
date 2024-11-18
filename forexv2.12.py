import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import time
start_time = time.time()

# Diccionario con los tickers y sus nombres completos

tickers_info = {
    "MXN=X": "FOREX USD/MXN",
    "SPY": "SPDR S&P 500 ETF Trust",
    "VTI": "Vanguard Total Stock Market ETF",
    "V": "Visa Inc.",
    "MA": "Mastercard Inc.",
    "HSBC": "HSBC Holdings plc",
    "JPM": "JPMorgan Chase & Co.",
    "BAC": "Bank of America Corp.",
    "C": "Citigroup Inc.",
    "GS": "The Goldman Sachs Group, Inc.",
    "MS": "Morgan Stanley",
    "WFC": "Wells Fargo & Co.",
    "AXP": "American Express Company",
    "USB": "U.S. Bancorp",
    "PNC": "PNC Financial Services",
    "DB": "Deutsche Bank AG",
    "ING": "ING Group",
    "RBC": "Royal Bank of Canada",
    "TD": "Toronto Dominion Bank",
    "XLF": "Financial Select Sector SPDR Fund",
    "IYF": "iShares U.S. Financials ETF",
    "VFH": "Vanguard Financials ETF",
    "FAS": "Direxion Daily Financial Bull 3X Shares",
    "FAZ": "Direxion Daily Financial Bear 3X Shares",
    "KBE": "SPDR S&P Bank ETF",
    "KRE": "SPDR S&P Regional Banking ETF",
    "FNCL": "Fidelity MSCI Financials Index ETF",
    "BLK": "BlackRock, Inc.",
    "SCHW": "Charles Schwab Corporation"
}


def obtener_datos(ticker_symbol, period, interval):
    """Obtiene los datos históricos de un ticker con el periodo e intervalo especificados."""
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)
    
    if data.empty:
        print(f"No se han encontrado datos para {tickers_info[ticker_symbol]} ({ticker_symbol}).")
        return None, None

    # Filtrar saltos mayores a 1 día
    data = data[~data.index.to_series().diff().dt.days.gt(1)]
    
    # Convertir índices a fecha con formato "día mes abreviado y año"
    data['Date'] = data.index.strftime('%d-%b-%Y %H:%M:%S')  # Día, mes abreviado y año (4 dígitos)
    
    # Identificar los saltos entre días
    data['Delta'] = data.index.to_series().diff().dt.days.fillna(0)
    weekend_jumps = data[data['Delta'] > 1].index  # Fechas con saltos

    return data, weekend_jumps

def mostrar_estadisticas(ticker_symbol, data):
    """Muestra estadísticas si el intervalo es de 1 minuto."""
    print("\n")
    print(f"Estadísticas del precio para {tickers_info[ticker_symbol]} ({ticker_symbol}):")
    print(f"- Último precio: {data['Close'].iloc[-1]:.4f} USD")
    print(f"- Última fecha y hora del dato: {data.index[-1]}")
    print(f"- Precio medio: {data['Close'].mean():.4f} USD")
    print(f"- Desviación estándar: {data['Close'].std():.4f} USD")
    print(f"- Precio mínimo: {data['Close'].min():.4f} USD")
    print(f"- Precio máximo: {data['Close'].max():.4f} USD")

def crear_grafica(data, weekend_jumps, periodo, intervalo, ticker_symbol, index_id):
    """Crea una gráfica de velas con los datos y añade las líneas de saltos."""
    fig = go.Figure()

    # Crear gráfico de velas
    fig.add_trace(go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=f'{tickers_info[ticker_symbol]} - Precio Histórico',
        increasing_line_color='green',
        decreasing_line_color='red'
    ))

    # Añadir líneas rojas para los saltos de fin de semana
    for jump in weekend_jumps:
        fig.add_shape(
            type="line",
            x0=jump.strftime('%d-%b-%Y %H:%M:%S'),
            x1=jump.strftime('%d-%b-%Y %H:%M:%S'),
            y0=data['Low'].min(),
            y1=data['High'].max(),
            line=dict(color="red", width=2, dash="dot"),
            xref='x',
            yref='y'
        )

    # Ajustar el diseño para omitir los huecos de tiempo
    fig.update_xaxes(type='category')
    
    # Titulo dinámico basado en periodo e intervalo
    title = f"{tickers_info[ticker_symbol]} ({ticker_symbol}), Periodo: {periodo}, Intervalo: {intervalo}"

    fig.update_layout(
        title=title,
        xaxis_title='Fecha',
        yaxis_title='Precio',
        height=900,
        width=1600,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        xaxis=dict(tickformat='%d-%b-%Y %H:%M:%S', tickmode='auto', nticks=20)
    )

    return fig



# Formatear los valores numéricos a "1,234.56"
def formatear_numeros(val):
    try:
        return f"{val:,.2f}"  # Formato de número con comas y 2 decimales
    except:
        return val  # Si no es un número, lo dejamos tal cual

# Función para guardar las gráficas y la tabla en un archivo HTML
def guardar_graficas_html(html_filename, *figs, df, tickers_info):
    # Añadir la columna de nombres de los tickers
    df['Nombre Ticker'] = df['Ticker'].map(tickers_info)  # Mapear los nombres de los tickers

    # Reordenar las columnas para que 'Nombre Ticker' sea la primera
    df = df[['Nombre Ticker'] + [col for col in df.columns if col != 'Nombre Ticker']]

    # Aplicar el formato a las columnas numéricas utilizando `apply` + `map`
    df = df.apply(lambda col: col.map(formatear_numeros) if col.dtype != 'O' else col)

    # Guardar la información en HTML
    with open(html_filename, 'w', encoding='utf-8') as f:  # Codificación UTF-8
        # Crear el índice al inicio del archivo HTML
        f.write("<h1 id='top'>Índice de Gráficas y Datos Financieros</h1>\n")
        f.write("<ul style='columns: 2;'>\n")  # Índice en dos columnas
        
        # Crear enlaces al índice de los tickers (gráficas)
        for i, fig in enumerate(figs):
            ticker_symbol = fig.layout.title.text.split('(')[0].strip()  # Obtener el nombre sin ticker
            f.write(f'<li><a href="#ticker{i}" style="color:blue;">{ticker_symbol}</a></li>\n')
        f.write("</ul>\n\n")

        # Insertar la tabla del DataFrame con la información financiera
        f.write("<h2>Información Financiera</h2>\n")
        
        # Centramos la tabla usando márgenes
        f.write("<div style='display: flex; justify-content: center;'>\n")
        f.write(df.to_html(index=False))  # Convertir el DataFrame a HTML y eliminar el índice
        f.write("</div>\n")  # Cierre del contenedor centrado

        # Guardar las gráficas con sus títulos y asignar ID a cada sección
        for i, fig in enumerate(figs):
            f.write(f'<a id="ticker{i}"></a>\n')  # Asignar un ID a cada gráfico
            f.write(f'<h2>{fig.layout.title.text}</h2>\n')  # Título descriptivo
            f.write(fig.to_html(full_html=True, include_plotlyjs="cdn"))
            f.write(f'<br><a href="#top">Ir al inicio</a><br><br>')  # Enlace para ir al inicio
            f.write("\n")

    print(f"Las gráficas y la tabla han sido guardadas en {html_filename}")



# Función optimizada para obtener la información financiera
def get_financial_info(tickers_info):
    financial_data = []
    for ticker in tickers_info:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Recopilando la información financiera más detallada
        financial_info = {
            "Ticker": ticker,
            "P/E": info.get("trailingPE", 0),  # P/E Ratio
            "EPS": info.get("trailingEps", 0),  # Earnings per Share
            "Book Value": info.get("bookValue", 0),  # Book Value
            "Div Yield": info.get("dividendYield", 0),  # Dividend Yield
            "Div/Share": info.get("dividendRate", 0),  # Dividend per Share
            "D/E": info.get("debtToEquity", 0),  # Debt-to-Equity Ratio
            "Beta": info.get("beta", 0),  # Beta
            "ROI": info.get("returnOnInvestment", 0),  # ROI
            "ROE": info.get("returnOnEquity", 0),  # Return on Equity
            "Vol": info.get("fiftyDayAverage", 0),  # Volatility (50-day)
            "52W High": info.get("fiftyTwoWeekHigh", 0),  # 52 Week High
            "52W Low": info.get("fiftyTwoWeekLow", 0),  # 52 Week Low
            "P/B": info.get("priceToBook", 0),  # Price to Book Ratio
            "Market Cap": info.get("marketCap", 0),  # Market Capitalization
            "Gross Margin": info.get("grossMargins", 0),  # Gross Margin
            "ROA": info.get("returnOnAssets", 0),  # Return on Assets
            "Operating Margin": info.get("operatingMargins", 0),  # Operating Margin
        }

        financial_data.append(financial_info)
    
    return financial_data


# Función para analizar las acciones
def analizar_acciones(df):
    # Definir las condiciones de filtrado y las columnas para ordenación
    filtros_y_orden = {
        'P/E alto (posiblemente sobrevaloradas)': {'condicion': df['P/E'] > 30, 'columna': 'P/E'},
        'Alta rentabilidad por dividendo': {'condicion': df['Div Yield'] > 0.03, 'columna': 'Div Yield'},
        'Beta alto (riesgo elevado)': {'condicion': df['Beta'] > 1, 'columna': 'Beta'},
        'Volumen alto': {'condicion': df['Vol'] > 100, 'columna': 'Vol'},
        'Alta volatilidad (Rango 52W alto)': {'condicion': df['52W High'] - df['52W Low'] > 100, 'columna': '52W Range'},
        'Alto riesgo (Beta > 1 y P/E > 30)': {'condicion': (df['Beta'] > 1) & (df['P/E'] > 30), 'columna': ['Beta', 'P/E']},
        'Acciones sin ganancias': {'condicion': df['P/E'] == 0, 'columna': 'P/E'},
        'Alta relación D/E (alto endeudamiento)': {'condicion': df['D/E'] > 1, 'columna': 'D/E'},
        'Alto margen bruto': {'condicion': df['Gross Margin'] > 0.5, 'columna': 'Gross Margin'},
        'Bajo P/B (menos de 1)': {'condicion': df['P/B'] < 1, 'columna': 'P/B'},
        'Alto ROE (Rentabilidad sobre el capital)': {'condicion': df['ROE'] > 0.15, 'columna': 'ROE'}
    }

    # Crear el dataframe para la columna '52W Range' (volatilidad)
    df['52W Range'] = df['52W High'] - df['52W Low']

    # Iterar sobre el diccionario de filtros y ordenarlos
    for categoria, info in filtros_y_orden.items():
        # Aplicar el filtro
        filtered_df = df[info['condicion']]
        
        # Verificar si el DataFrame filtrado está vacío
        if filtered_df.empty:
            print(f"\n ")
            continue  # Saltar a la siguiente iteración si está vacío
        
        # Ordenar los resultados de mayor a menor
        if isinstance(info['columna'], list):
            filtered_df = filtered_df.sort_values(by=info['columna'], ascending=False)
        else:
            filtered_df = filtered_df.sort_values(by=info['columna'], ascending=False)
        
        # Imprimir los resultados
        print(f"\nAcciones con {categoria}:")
        print(filtered_df[['Nombre Ticker', *([info['columna']] if isinstance(info['columna'], str) else info['columna'])]])


# Recolectar la información financiera de los tickers
print(f"Consultando en Yahoo en {time.time() - start_time:.2f} segundos.")
financial_data = get_financial_info(tickers_info)
print(f"Listo en {time.time() - start_time:.2f} segundos.")

# Crear un DataFrame de pandas para mostrar la información en formato tabular
df = pd.DataFrame(financial_data)

# Parámetros de entrada
html_filename = "grafico_precios_historicos.html"

print(f"Obteniendo data en {time.time() - start_time:.2f} segundos.")

# Obtener datos y gráficas para cada par de periodo/intervalo
figs = []
index_id = 0
for ticker in tickers_info.keys():
    for periodo, intervalo in [("1d", "1m"), ("1mo", "15m"), ("3mo", "1h")]:
        data, weekend_jumps = obtener_datos(ticker, periodo, intervalo)
        if data is not None:
            # Mostrar estadísticas solo si el intervalo es de 1 minuto
            if intervalo == "1m":
                mostrar_estadisticas(ticker, data)
            
            fig = crear_grafica(data, weekend_jumps, periodo, intervalo, ticker, f"ticker{index_id}")
            figs.append(fig)
            index_id += 1


# Guardar todas las gráficas y la tabla de información financiera juntas en un solo archivo HTML
guardar_graficas_html(html_filename, *figs, df=df, tickers_info=tickers_info)


# Llamar a la función pasando el dataframe df
analizar_acciones(df)






