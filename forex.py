import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
from matplotlib.backends.backend_pdf import PdfPages

warnings.filterwarnings("ignore")

def analizar_activo(ticker_symbol, pdf):
    # Configurar el rango de tiempo para las últimas 24 horas
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    
    # Crear objeto de Ticker y obtener el nombre del activo
    ticker = yf.Ticker(ticker_symbol)
    asset_name = ticker.info.get("shortName", "Activo")
    
    # Descargar datos del activo en intervalos de 1 minuto
    data = yf.download(ticker_symbol, start=start_time, end=end_time, interval="1m")
    
    # Verificar si se obtuvieron datos
    if data.empty:
        print(f"No se han encontrado datos para las últimas 24 horas de {ticker_symbol}.")
        return
    
    # Calcular estadísticas
    mean_price = data['Close'].mean().item()
    std_dev_price = data['Close'].std().item()
    min_price = data['Close'].min().item()
    max_price = data['Close'].max().item()
    price_range = max_price - min_price
    median_price = data['Close'].median().item()
    coef_var = (std_dev_price / mean_price) * 100  # Porcentaje
    last_price = data['Close'].iloc[-1].item()
    q1_price = data['Close'].quantile(0.25).item()
    q3_price = data['Close'].quantile(0.75).item()
    iqr_price = q3_price - q1_price
    skewness = data['Close'].skew().item()
    kurtosis = data['Close'].kurtosis().item()
    
    # Mostrar estadísticas
    print(f"Estadísticas del precio de {asset_name} en las últimas 24 horas:")
    print(f"- Precio medio: {mean_price:.2f} USD")
    print(f"- Desviación estándar: {std_dev_price:.2f} USD")
    print(f"- Precio mínimo: {min_price:.2f} USD")
    print(f"- Precio máximo: {max_price:.2f} USD")
    print(f"- Rango de precios: {price_range:.2f} USD")
    print(f"- Mediana: {median_price:.2f} USD")
    print(f"- Coeficiente de variación: {coef_var:.2f}%")
    print(f"- Último precio: {last_price:.2f} USD")
    print(f"- Primer cuartil (Q1): {q1_price:.2f} USD")
    print(f"- Tercer cuartil (Q3): {q3_price:.2f} USD")
    print(f"- Rango intercuartílico (IQR): {iqr_price:.2f} USD")
    print(f"- Asimetría: {skewness:.2f}")
    print(f"- Curtosis: {kurtosis:.2f}")
    
    # Calcular medias móviles
    data['SMA_5'] = data['Close'].rolling(window=5).mean()
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    
    # Conclusiones basadas en estadísticas
    if std_dev_price > mean_price * 0.05:
        print("Conclusión: La volatilidad del precio del activo ha sido alta en las últimas 24 horas.")
    else:
        print("Conclusión: La volatilidad del precio del activo ha sido baja en las últimas 24 horas.")
        
    if coef_var > 10:
        print("Conclusión: Alta variabilidad en el precio, lo cual puede indicar un mercado inestable.")
    else:
        print("Conclusión: Baja variabilidad en el precio, sugiriendo un mercado estable.")
    
    if skewness > 0:
        print("Conclusión: La distribución del precio es asimétrica a la derecha, con una tendencia a precios más altos.")
    else:
        print("Conclusión: La distribución del precio es asimétrica a la izquierda, con una tendencia a precios más bajos.")
    
    if last_price > mean_price:
        print("Conclusión: El último precio es mayor que el precio medio, lo que podría indicar una tendencia alcista.")
    else:
        print("Conclusión: El último precio es menor que el precio medio, lo que podría indicar una tendencia bajista.")

    # Gráfica de medias móviles
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label=asset_name, color='blue', alpha=0.5)
    plt.plot(data.index, data['SMA_5'], label='Media Móvil 5 minutos', color='red')
    plt.plot(data.index, data['SMA_20'], label='Media Móvil 20 minutos', color='green')
    plt.axhline(y=last_price, color='orange', linestyle='--', label='Último Precio')
    plt.xlabel("Fecha")
    plt.ylabel(f"Precio de {asset_name} (USD)")
    plt.title(f"Medias Móviles del Precio de {asset_name}")
    plt.legend()
    plt.grid(True)
    pdf.savefig()  # Guarda la gráfica en el PDF
    plt.close()
    
    # Histograma de precios
    plt.figure(figsize=(12, 6))
    plt.hist(data['Close'], bins=20, color='lightblue', edgecolor='black')
    plt.axvline(mean_price, color='red', linestyle='dashed', linewidth=1, label='Media')
    plt.axvline(median_price, color='green', linestyle='dashed', linewidth=1, label='Mediana')
    plt.xlabel(f"Precio de {asset_name} (USD)")
    plt.ylabel("Frecuencia")
    plt.title(f"Histograma del Precio de {asset_name}")
    plt.legend()
    plt.grid(True)
    pdf.savefig()  # Guarda la gráfica en el PDF
    plt.close()

# Crear un archivo PDF para guardar todas las gráficas
pdf_filename = "analisis_activos.pdf"
with PdfPages(pdf_filename) as pdf:
    # Análisis de los activos deseados
    # Divisas
    analizar_activo("MXN=X", pdf)   # Peso mexicano
    analizar_activo("EURUSD=X", pdf)  # Euro
    analizar_activo("GBPUSD=X", pdf)  # Libra esterlina
    analizar_activo("JPY=X", pdf)      # Yen japonés
    
    # Metales preciosos
    analizar_activo("GC=F", pdf)    # Oro
    analizar_activo("SI=F", pdf)     # Plata

print(f"Las gráficas han sido guardadas en {pdf_filename}")
