import os
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# Constants
OUTPUT_DIR = 'output'
TICKERS_FILE = "tickers/mis_tickers.txt"
TRADE_SIGNALS_LIST = []

def setup_environment():
    """Create necessary directories and load tickers."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    df = pd.read_csv(TICKERS_FILE)
    return df["0"].to_list()[:10]

def obtener_datos(ticker_symbol: str, period: str, interval: str):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)
    
    if data.empty:
        print(f"No se han encontrado datos para {ticker_symbol}.")
        return None, None

    data = data[~data.index.to_series().diff().dt.days.gt(1)]
    data['Date'] = data.index.strftime('%d-%b-%Y %H:%M:%S')
    data['Delta'] = data.index.to_series().diff().dt.days.fillna(0)
    weekend_jumps = data[data['Delta'] > 1].index

    return data, weekend_jumps

def calcular_indicadores(data: pd.DataFrame):
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

def detectar_senales(data: pd.DataFrame, ticker_symbol: str, long_name: str, sector: str):
    data['cross_up'] = (data['EMA_50'].shift(1) <= data['EMA_200'].shift(1)) & (data['EMA_50'] > data['EMA_200'])
    data['cross_down'] = (data['EMA_50'].shift(1) >= data['EMA_200'].shift(1)) & (data['EMA_50'] < data['EMA_200'])
    
    buy_signals = data[data['cross_up']]
    sell_signals = data[data['cross_down']]

    for idx in buy_signals.index:
        TRADE_SIGNALS_LIST.append({
            'Ticker': ticker_symbol,
            'LongName': long_name,
            'Sector': sector,
            'Date': idx,
            'Close': buy_signals.loc[idx, 'Close'],
            'Signal': 'BUY'
        })
    for idx in sell_signals.index:
        TRADE_SIGNALS_LIST.append({
            'Ticker': ticker_symbol,
            'LongName': long_name,
            'Sector': sector,
            'Date': idx,
            'Close': sell_signals.loc[idx, 'Close'],
            'Signal': 'SELL'
        })

    return buy_signals, sell_signals

def generar_figura(data: pd.DataFrame, weekend_jumps, buy_signals: pd.DataFrame, sell_signals: pd.DataFrame, periodo: str, intervalo: str, ticker_symbol: str):
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=[f"{ticker_symbol} - Periodo: {periodo}, Intervalo: {intervalo}", "MACD"]
    )

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

def crear_grafica(data: pd.DataFrame, weekend_jumps, periodo: str, intervalo: str, ticker_symbol: str, index_id: int, long_name: str, sector: str):
    calcular_indicadores(data)
    buy_signals, sell_signals = detectar_senales(data, ticker_symbol, long_name, sector)
    return generar_figura(data, weekend_jumps, buy_signals, sell_signals, periodo, intervalo, ticker_symbol)

def guardar_graficas_html_sector(figs_info: list, sector: str):
    html_filename = os.path.join(OUTPUT_DIR, f'graficas_{sector}.html')
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

def print_progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '', decimals: int = 1, length: int = 50, fill: str = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total: 
        print()

def main():
    tickers = setup_environment()
    sector_dict = {}
    total_tickers = len(tickers)

    for i, ticker in enumerate(tickers):
        ticker_obj = yf.Ticker(ticker)
        sector = ticker_obj.info.get("sector", "Unknown Sector")
        long_name = ticker_obj.info.get("longName", ticker)

        if sector not in sector_dict:
            sector_dict[sector] = []
        
        for periodo, intervalo in [("3mo", "1h")]:
            data, weekend_jumps = obtener_datos(ticker, periodo, intervalo)
            if data is not None:
                fig = crear_grafica(data, weekend_jumps, periodo, intervalo, ticker, len(sector_dict[sector]), long_name, sector)
                sector_dict[sector].append({"fig": fig, "ticker": ticker, "long_name": long_name})

        print_progress_bar(i + 1, total_tickers, prefix='Procesando tickers', suffix='Completado')

    for sector, sector_figs in sector_dict.items():
        guardar_graficas_html_sector(sector_figs, sector)

    if TRADE_SIGNALS_LIST:
        signals_df = pd.DataFrame(TRADE_SIGNALS_LIST)
        signals_df['Date'] = pd.to_datetime(signals_df['Date'])
        signals_df['Date'] = pd.to_datetime(signals_df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
        signals_df['Close'] = signals_df['Close'].round(2)
        signals_df.sort_values(by='Date', ascending=False, inplace=True)
        excel_filename = os.path.join(OUTPUT_DIR, "buy_sell_signals.xlsx")
        signals_df.to_excel(excel_filename, index=False)
        print(f"Archivo '{excel_filename}' creado con éxito.")
    else:
        print("No se generaron señales de Buy/Sell.")

if __name__ == "__main__":
    main()
