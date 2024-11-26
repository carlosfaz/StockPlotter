import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

def obtener_datos(ticker_symbol, period, interval):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)
    
    if data.empty:
        print(f"No se han encontrado datos para {ticker_symbol}.")
        return None, None

    data = data[~data.index.to_series().diff().dt.days.gt(1)]
    data['Date'] = data.index.strftime('%d-%b-%Y %H:%M:%S')
    data['Delta'] = data.index.to_series().diff().dt.days.fillna(0)
    weekend_jumps = data[data['Delta'] > 1].index
    
    last_datetime = data.index[-1]
    
    mean_price = data['Close'].mean()
    std_dev_price = data['Close'].std()
    min_price = data['Close'].min()
    max_price = data['Close'].max()
    price_range = max_price - min_price
    median_price = data['Close'].median()
    coef_var = (std_dev_price / mean_price) * 100
    last_price = data['Close'].iloc[-1]
    q1_price = data['Close'].quantile(0.25)
    q3_price = data['Close'].quantile(0.75)
    iqr_price = q3_price - q1_price
    skewness = data['Close'].skew()
    kurtosis = data['Close'].kurtosis()
    
    print(f"- Último precio: {last_price:.2f} USD")
    print(f"- Última fecha y hora del dato: {last_datetime}")
    print(f"- Precio medio: {mean_price:.2f} USD")
    print(f"- Desviación estándar: {std_dev_price:.2f} USD")
    print(f"- Precio mínimo: {min_price:.2f} USD")
    print(f"- Precio máximo: {max_price:.2f} USD")
    print(f"- Rango de precios: {price_range:.2f} USD")
    print(f"- Mediana: {median_price:.2f} USD")
    print(f"- Coeficiente de variación: {coef_var:.2f}%")
    print(f"- Primer cuartil (Q1): {q1_price:.2f} USD")
    print(f"- Tercer cuartil (Q3): {q3_price:.2f} USD")
    print(f"- Rango intercuartílico (IQR): {iqr_price:.2f} USD")
    print(f"- Asimetría: {skewness:.2f}")
    print(f"- Curtosis: {kurtosis:.2f}")
    
    return data, weekend_jumps, last_price, mean_price, std_dev_price, coef_var, q1_price, q3_price, skewness, kurtosis

def crear_grafica(data, weekend_jumps, ticker_symbol):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=f'{ticker_symbol} - Precio Histórico', 
        increasing_line_color='green',
        decreasing_line_color='red'
    ))

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

    fig.update_xaxes(type='category')

    fig.update_layout(
        title=f"Precio del Activo ({ticker_symbol})",
        xaxis_title='Fecha',
        yaxis_title='Precio (USD)',
        height=900,
        width=1600,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        xaxis=dict(tickformat='%d-%b-%Y %H:%M:%S', tickmode='auto', nticks=20)
    )

    return fig

def analizar_activo(ticker_symbol, html_filename="analisis_activos.html"):
    data, weekend_jumps, last_price, mean_price, std_dev_price, coef_var, q1_price, q3_price, skewness, kurtosis = obtener_datos(ticker_symbol, "5d", "1m")
    
    if data is not None:
        fig = crear_grafica(data, weekend_jumps, ticker_symbol)
        fig.write_html(html_filename)
        print(f"Gráfica exportada exitosamente a {html_filename}")

        # Conclusiones para tomar decisiones
        print("\n### CONCLUSIONES ###")
        
        if last_price < mean_price and coef_var < 1.0:
            print("**Es un buen momento para comprar. El precio actual es menor que el promedio y hay poca variabilidad.**")
        elif last_price >= mean_price and coef_var > 1.0:
            print("**Sería mejor esperar. El precio actual es más alto en relación con el promedio y hay alta variabilidad.**")
        elif last_price >= q3_price:
            print("**El precio está cerca del tercer cuartil (máximo), sería prudente esperar a que baje antes de considerar la compra.**")
        elif last_price <= q1_price:
            print("**Es un buen momento de compra. El precio actual está cerca del primer cuartil (mínimo).**")
        else:
            print("**Es mejor esperar a confirmación de una tendencia clara antes de tomar una decisión.**")

        if skewness > 0:
            print("El precio muestra una asimetría positiva, lo que podría indicar un aumento futuro en los precios.")
        elif skewness < 0:
            print("El precio muestra una asimetría negativa, lo que podría indicar una disminución futura en los precios.")
        else:
            print("El precio no muestra asimetría significativa.")

        if kurtosis > 3:
            print("La curtosis sugiere que el precio tiene más eventos extremos de lo normal (más picos).")
        elif kurtosis < 3:
            print("La curtosis sugiere que el precio tiene menos eventos extremos de lo normal (menos picos).")
        else:
            print("La curtosis indica una distribución normal de los precios.")
            
        if coef_var < 1.0:
            print("La variabilidad de los precios es baja, lo cual indica estabilidad en el precio del activo.")
        else:
            print("La variabilidad de los precios es alta, se recomienda precaución.")

html_filename = "analisis_activos.html"
analizar_activo("GC=F", html_filename)
print(f"Las gráficas han sido guardadas en {html_filename}")
