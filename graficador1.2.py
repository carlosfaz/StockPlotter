import os
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# Crear la carpeta 'output' si no existe
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ==>>> Lista global donde iremos guardando las señales (BUY/SELL) para luego exportar a .xlsx
trade_signals_list = []

# Cargar los tickers desde el archivo .txt
df = pd.read_csv("tickers/mis_tickers.txt")
tickers = df["0"].to_list()[:10]  # Lista de tickers

# Función para obtener los datos históricos de un ticker
def obtener_datos(ticker_symbol, period, interval):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)
    
    if data.empty:
        print(f"No se han encontrado datos para {ticker_symbol}.")
        return None, None

    # Filtrar saltos mayores a 1 día
    data = data[~data.index.to_series().diff().dt.days.gt(1)]
    
    data['Date'] = data.index.strftime('%d-%b-%Y %H:%M:%S')
    data['Delta'] = data.index.to_series().diff().dt.days.fillna(0)
    weekend_jumps = data[data['Delta'] > 1].index

    return data, weekend_jumps


def calcular_indicadores(data):
    """
    Calcula y agrega al DataFrame las columnas de indicadores técnicos
    (MACD, EMA, ZLEMA, SMA, etc.)
    """
    data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    data['Hist'] = data['MACD'] - data['Signal']

    periodo_zlema = 14
    lag = int((periodo_zlema - 1) / 2)
    data['ZL_Price'] = 2 * data['Close'] - data['Close'].shift(lag)
    data['ZLEMA_14'] = data['ZL_Price'].ewm(span=periodo_zlema, adjust=False).mean()

    data['EMA_200'] = data['Close'].ewm(span=200, adjust=False).mean()
    data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()

def detectar_senales(data, ticker_symbol, long_name, sector, trade_signals_list):
    """
    Detecta las señales de cruce de EMA(50) y EMA(200). 
    Registra esas señales en la lista global trade_signals_list y 
    devuelve dos DataFrames con las filas de señal de compra y venta.
    """
    data['cross_up'] = (data['EMA_50'].shift(1) <= data['EMA_200'].shift(1)) & (data['EMA_50'] > data['EMA_200'])
    data['cross_down'] = (data['EMA_50'].shift(1) >= data['EMA_200'].shift(1)) & (data['EMA_50'] < data['EMA_200'])
    
    buy_signals = data[data['cross_up']]
    sell_signals = data[data['cross_down']]

    # Agregamos las señales a la lista global
    for idx in buy_signals.index:
        trade_signals_list.append({
            'Ticker': ticker_symbol,
            'LongName': long_name,
            'Sector': sector,  # <--- Se agrega la columna Sector
            'Date': idx,
            'Close': buy_signals.loc[idx, 'Close'],
            'Signal': 'BUY'
        })
    for idx in sell_signals.index:
        trade_signals_list.append({
            'Ticker': ticker_symbol,
            'LongName': long_name,
            'Sector': sector,  # <--- Se agrega la columna Sector
            'Date': idx,
            'Close': sell_signals.loc[idx, 'Close'],
            'Signal': 'SELL'
        })

    return buy_signals, sell_signals

def generar_figura(data, weekend_jumps, buy_signals, sell_signals, periodo, intervalo, ticker_symbol):
    """
    Crea y configura el objeto Plotly Figure con toda la información:
    - Velas
    - Indicadores EMA, ZLEMA, SMA
    - Señales de compra/venta
    - MACD
    """
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=[f"{ticker_symbol} - Periodo: {periodo}, Intervalo: {intervalo}", "MACD"]
    )

    # Fila 1: Velas, ZLEMA(14), EMA(200), EMA(50), SMA(50), Señales
    fig.add_trace(
        go.Candlestick(
            x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=ticker_symbol,
            increasing_line_color='green',
            decreasing_line_color='red'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['ZLEMA_14'],
            mode='lines',
            name='ZLEMA(14)',
            line=dict(color='purple', width=2)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['EMA_200'],
            mode='lines',
            name='EMA(200)',
            line=dict(color='darkgreen', width=2)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['EMA_50'],
            mode='lines',
            name='EMA(50)',
            line=dict(color='red', width=2)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['SMA_50'],
            mode='lines',
            name='SMA(50)',
            line=dict(color='blue', width=2),
            fill='tonexty',
            fillcolor='rgba(255, 165, 0, 0.2)'
        ),
        row=1, col=1
    )

    # Líneas verticales en saltos de fin de semana
    for jump in weekend_jumps:
        fig.add_shape(
            type="line",
            x0=jump.strftime('%d-%b-%Y %H:%M:%S'),
            x1=jump.strftime('%d-%b-%Y %H:%M:%S'),
            y0=data['Low'].min(),
            y1=data['High'].max(),
            line=dict(color="red", width=2),
            xref='x',
            yref='y',
            row=1, col=1
        )

    # Señales BUY
    fig.add_trace(
        go.Scatter(
            x=buy_signals['Date'],
            y=buy_signals['Close'],
            mode='markers',
            name='Buy (EMA50/200)',
            marker=dict(symbol='triangle-up', color='lime', size=12)
        ),
        row=1, col=1
    )
    # Señales SELL
    fig.add_trace(
        go.Scatter(
            x=sell_signals['Date'],
            y=sell_signals['Close'],
            mode='markers',
            name='Sell (EMA50/200)',
            marker=dict(symbol='triangle-down', color='#FF00FF', size=12)
        ),
        row=1, col=1
    )

    # Fila 2: MACD, Signal, Hist
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['MACD'],
            mode='lines',
            name='MACD',
            line=dict(color='black', width=2)
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['Signal'],
            mode='lines',
            name='Signal',
            line=dict(color='orange', width=2)
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(
            x=data['Date'],
            y=data['Hist'],
            name='Histograma',
            marker=dict(color='darkblue')
        ),
        row=2, col=1
    )

    fig.update_layout(
        title=f"{ticker_symbol} - Periodo: {periodo}, Intervalo: {intervalo}",
        height=900,
        width=1600,
        showlegend=True,
        xaxis_rangeslider_visible=False
    )

    fig.update_xaxes(row=1, col=1, type='category', tickformat='%d-%b-%Y %H:%M:%S', tickmode='auto', nticks=20)
    fig.update_yaxes(title_text='Precio', row=1, col=1)
    fig.update_xaxes(row=2, col=1, type='category', tickformat='%d-%b-%Y %H:%M:%S', tickmode='auto', nticks=20)
    fig.update_yaxes(title_text='MACD', row=2, col=1)

    return fig

def crear_grafica(data, weekend_jumps, periodo, intervalo, ticker_symbol, index_id, long_name, sector):
    """
    Orquesta las llamadas a las funciones de:
     1) Cálculo de indicadores
     2) Detección de señales
     3) Generación de la figura Plotly
    """
    # 1) Calculamos indicadores
    calcular_indicadores(data)

    # 2) Detectamos señales (pasamos el sector) y las guardamos en la lista global
    buy_signals, sell_signals = detectar_senales(
        data, 
        ticker_symbol, 
        long_name, 
        sector, 
        trade_signals_list
    )

    # 3) Generamos la gráfica
    fig = generar_figura(data, weekend_jumps, buy_signals, sell_signals, periodo, intervalo, ticker_symbol)

    return fig

# Función para guardar las gráficas en un archivo HTML por sector
def guardar_graficas_html_sector(figs_info, sector):
    html_filename = os.path.join(output_dir, f'graficas_{sector}.html')
    with open(html_filename, 'w', encoding='utf-8') as f:
        escribir_encabezado_html(f)

        f.write(f'<h1>Índice de Gráficas para el Sector: {sector}</h1>\n')
        f.write('<ul style="columns: 2; list-style-type: none; padding: 0;">\n')
        for i, info in enumerate(figs_info):
            ticker = info["ticker"]
            long_name = info["long_name"]
            f.write(f'<li><a href="#grafico{i}">{ticker} - {long_name}</a></li>\n')
        f.write('</ul>\n')

        f.write('<h1>Gráficas de Precios Históricos</h1>\n')
        for i, info in enumerate(figs_info):
            fig = info["fig"]
            ticker = info["ticker"]
            long_name = info["long_name"]
            f.write(f'<h2 id="grafico{i}">{fig.layout.title.text}</h2>\n')
            f.write(f'<p><strong>{ticker} - {long_name}</strong></p>\n')
            f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))
            f.write('<br><br>\n')
            agregar_vinculo_volver_inicio(f)

        f.write('</body></html>\n')

    print(f"Las gráficas han sido guardadas en {html_filename}")

def escribir_encabezado_html(f):
    encabezado_html = '''
    <h1>Graficas de Precios Historicos</h1>
    <html>
    <head>
    <style>
        table {
            border-collapse: collapse; 
            width: 100%;
        } 
        th, td {
            border: 1px solid black; 
            padding: 5px;
        } 
        th {
            background-color: #f2f2f2;
        } 
        a {
            color: blue; 
            text-decoration: none; 
            font-weight: bold;
        }
    </style>
    </head>
    <body id="top">
    '''
    f.write(encabezado_html)

def agregar_vinculo_volver_inicio(f):
    f.write('<br><a href="#top">Volver al inicio</a><br><br>')

# ------------------------------ Helpers de progreso ------------------------------
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total: 
        print()

def main():
    sector_dict = {}
    
    total_tickers = len(tickers)  # Total de tickers

    for i, ticker in enumerate(tickers):
        ticker_obj = yf.Ticker(ticker)
        # Obtenemos el sector
        sector = ticker_obj.info.get("sector", "Unknown Sector")
        long_name = ticker_obj.info.get("longName", ticker)

        if sector not in sector_dict:
            sector_dict[sector] = []
        
        for periodo, intervalo in [("3mo", "1h")]:
            data, weekend_jumps = obtener_datos(ticker, periodo, intervalo)
            if data is not None:
                # Aquí pasamos el sector a la función crear_grafica
                fig = crear_grafica(
                    data, 
                    weekend_jumps, 
                    periodo, 
                    intervalo, 
                    ticker, 
                    len(sector_dict[sector]), 
                    long_name, 
                    sector
                )
                sector_dict[sector].append({"fig": fig, "ticker": ticker, "long_name": long_name})

        # Actualizar la barra de progreso
        print_progress_bar(i + 1, total_tickers, prefix='Procesando tickers', suffix='Completado')

    # Guardar las gráficas por sector (un solo archivo HTML por sector)
    for sector, sector_figs in sector_dict.items():
        guardar_graficas_html_sector(sector_figs, sector)

if __name__ == "__main__":
    main()
    # ==>>> Al finalizar, creamos el DataFrame con las señales y lo exportamos a Excel
    if trade_signals_list:
        signals_df = pd.DataFrame(trade_signals_list)
        # Convertimos la fecha a datetime y la hacemos naive (sin timezone)
        signals_df['Date'] = pd.to_datetime(signals_df['Date'])
        signals_df['Date'] = pd.to_datetime(signals_df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
        signals_df['Close'] = signals_df['Close'].round(2)
        
        # Ordenar de más reciente a más antiguo
        signals_df.sort_values(by='Date', ascending=False, inplace=True)
        
        excel_filename = os.path.join(output_dir, "buy_sell_signals.xlsx")
        signals_df.to_excel(excel_filename, index=False)
        print(f"Archivo '{excel_filename}' creado con éxito.")
    else:
        print("No se generaron señales de Buy/Sell.")
