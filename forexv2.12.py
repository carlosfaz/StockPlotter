import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

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

def guardar_graficas_html(html_filename, *figs):
    """Guarda varias gráficas en un archivo HTML de forma eficiente."""
    with open(html_filename, 'w', encoding='utf-8') as f:  # Se especifica la codificación UTF-8
        # Crear el índice al inicio del archivo HTML
        f.write("<h1 id='top'>Índice de Gráficas</h1>\n")
        f.write("<ul style='columns: 2;'>\n")  # Índice de dos columnas
        
        # Crear enlaces al índice de los tickers
        for i, fig in enumerate(figs):
            ticker_symbol = fig.layout.title.text.split('(')[0].strip()  # Obtener el nombre sin ticker
            f.write(f'<li><a href="#ticker{i}" style="color:blue;">{ticker_symbol}</a></li>\n')  # Acceder al texto del título
        f.write("</ul>\n\n")

        # Guardar las gráficas con sus títulos y asignar ID a cada sección
        for i, fig in enumerate(figs):
            f.write(f'<a id="ticker{i}"></a>\n')  # Asignar un ID a cada gráfico
            f.write(f'<h2>{fig.layout.title.text}</h2>\n')  # Título descriptivo
            f.write(fig.to_html(full_html=True, include_plotlyjs="cdn"))
            f.write(f'<br><a href="#top">Ir al inicio</a><br><br>')  # Enlace para ir al inicio
            f.write("\n")
    
    print(f"Las gráficas han sido guardadas en {html_filename}")

# Parámetros de entrada
html_filename = "grafico_precios_historicos.html"

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

# Guardar todas las gráficas juntas en un solo archivo HTML
guardar_graficas_html(html_filename, *figs)
