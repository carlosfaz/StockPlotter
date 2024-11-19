import yfinance as yf
import pandas as pd

# Diccionario con los tickers y sus nombres completos
tickers_info = {
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

# Crear una lista para almacenar los datos
data = []

# Obtener P/E ratio para cada ticker
for ticker_symbol, ticker_name in tickers_info.items():
    ticker = yf.Ticker(ticker_symbol)
    ticker_info = ticker.info

    # Obtener el P/E ratio (trailing PE)
    pe_ratio = ticker_info.get('trailingPE', 'No disponible')
    
    # Obtener otras métricas
    market_cap = ticker_info.get('marketCap', 'No disponible')
    eps = ticker_info.get('epsTrailingTwelveMonths', 'No disponible')

    # Agregar la información a la lista de datos
    data.append([ticker_symbol, ticker_name, pe_ratio, market_cap, eps])

# Crear un DataFrame de pandas
df = pd.DataFrame(data, columns=["Ticker", "Nombre", "P/E Ratio"])

# Exportar a un archivo Excel
df.to_csv("resumen_tickers_financieros.csv", index=False)

print("La tabla de P/E ratio y otras métricas se ha guardado en 'resumen_tickers_financieros.csv'.")




from datetime import datetime
import pandas as pd
from pytz import timezone

# Diccionario con los tickers y nombres
tickers_info = {
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



import yfinance as yf
import pandas as pd

# Lista de los tickers
tickers = ['V', 'MA', 'HSBC']

# Diccionario para almacenar los datos
data_dict = {}

# Obtenemos los datos de cada ticker
for ticker in tickers:
    stock = yf.Ticker(ticker)
    
    # Información básica
    info = stock.info  # Información general sobre el ticker
    
    # Guardamos la información que nos interesa
    data_dict[ticker] = {
        'Nombre': info.get('longName', 'N/A'),
        'Sector': info.get('sector', 'N/A'),
        'Industry': info.get('industry', 'N/A'),
        'P/E Ratio': info.get('trailingPE', 'N/A'),
        'Dividendo': info.get('dividendYield', 'N/A'),
        'Rendimiento de dividendos (YTD)': info.get('ytdReturn', 'N/A'),
        'Capitalización de mercado': info.get('marketCap', 'N/A'),
        'Precio actual': info.get('currentPrice', 'N/A'),
        'Beta': info.get('beta', 'N/A'),
        'Volumen promedio': info.get('averageVolume', 'N/A'),
        'EPS': info.get('trailingEps', 'N/A'),
        'Fecha de última actualización': info.get('lastDividendDate', 'N/A'),
    }

# Crear un DataFrame con los datos
df = pd.DataFrame.from_dict(data_dict, orient='index')

# Mostrar la tabla resumen
print(df)

# Guardar la información en un archivo Excel
df.to_excel("informacion_tickers.xlsx", index=True)


import yfinance as yf
import pandas as pd

# Diccionario con los tickers y sus nombres completos
tickers_info = {
    "V": "Visa Inc.",
    "MA": "Mastercard Inc.",
    "HSBC": "HSBC Holdings plc"
}

# Lista para almacenar los datos financieros
financial_data = []

# Función para consultar la información financiera
def get_financial_info(ticker):
    stock = yf.Ticker(ticker)
    
    # Datos generales
    info = stock.info
    
    # Recopilando información
    financial_info = {
        "Ticker": ticker,
        "Company Name": tickers_info[ticker],
        "P/E Ratio": info.get("trailingPE", "N/A"),
        "EPS (Earnings per Share)": info.get("trailingEps", "N/A"),
        "Book Value": info.get("bookValue", "N/A"),
        "Dividend Yield": info.get("dividendYield", "N/A"),
        "Dividend per Share": info.get("dividendRate", "N/A"),
        "Debt-to-Equity Ratio (D/E)": info.get("debtToEquity", "N/A"),
        "Beta": info.get("beta", "N/A"),
        "ROI (Return on Investment)": info.get("returnOnInvestment", "N/A"),
        "ROE (Return on Equity)": info.get("returnOnEquity", "N/A"),
        "Volatility (50 day)": info.get("fiftyDayAverage", "N/A"),
        "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
        "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
        "Market Cap": info.get("marketCap", "N/A"),
    }
    
    return financial_info

# Recolectar la información financiera de los tickers
for ticker in tickers_info.keys():
    financial_info = get_financial_info(ticker)
    financial_data.append(financial_info)

# Crear un DataFrame de pandas para mostrar la información en formato tabular
df = pd.DataFrame(financial_data)

# Mostrar el DataFrame
print(df)

# Guardar los datos en un archivo Excel
df.to_excel("financial_data.xlsx", index=False)


import yfinance as yf
import pandas as pd

# Diccionario con los tickers y sus nombres completos
tickers_info ={
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

# Lista para almacenar los datos financieros
financial_data = []

# Función para consultar la información financiera
def get_financial_info(ticker):
    stock = yf.Ticker(ticker)
    
    # Datos generales
    info = stock.info
    
    # Recopilando información financiera adicional
    financial_info = {
        "Ticker": ticker,
        "Company Name": tickers_info[ticker],
        "P/E Ratio": info.get("trailingPE", 0),
        "EPS (Earnings per Share)": info.get("trailingEps", 0),
        "Book Value": info.get("bookValue", 0),
        "Dividend Yield": info.get("dividendYield", 0),
        "Dividend per Share": info.get("dividendRate", 0),
        "Debt-to-Equity Ratio (D/E)": info.get("debtToEquity", 0),
        "Beta": info.get("beta", 0),
        "ROI (Return on Investment)": info.get("returnOnInvestment", 0),
        "ROE (Return on Equity)": info.get("returnOnEquity", 0),
        "Volatility (50-day)": info.get("fiftyDayAverage", 0),
        "52 Week High": info.get("fiftyTwoWeekHigh", 0),
        "52 Week Low": info.get("fiftyTwoWeekLow", 0),
    }
    
    return financial_info

# Recolectar la información financiera de los tickers
for ticker in tickers_info.keys():
    financial_info = get_financial_info(ticker)
    financial_data.append(financial_info)

# Crear un DataFrame de pandas para mostrar la información en formato tabular
df = pd.DataFrame(financial_data)

# Mostrar el DataFrame
print(df)

# Guardar los datos en un archivo Excel
df.to_excel("financial_data_full.xlsx", index=False)


