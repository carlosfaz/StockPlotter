import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import time

def get_data_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        if table:
            headers = [header.text.strip() for header in table.find_all("th")]
            rows = []
            for row in table.find_all("tr")[1:]:
                data = [col.text.strip() for col in row.find_all("td")]
                if data:
                    rows.append(data)
            return pd.DataFrame(rows, columns=headers)
    return pd.DataFrame()

def fetch_data(name, base_url):
    all_data = []
    for start in range(0, 125, 25):
        url = base_url.format(start)
        print(f"Obteniendo datos de {name}: Página {start//25 + 1} de 5", end="", flush=True)
        df = get_data_from_url(url)
        if not df.empty:
            all_data.append(df)
        print(" ✅")
        time.sleep(1)  # Para evitar bloqueos por exceso de solicitudes
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()


def convert_units(value):
    if isinstance(value, str):
        value = value.replace(',', '')
        if 'M' in value:
            return float(value.replace('M', '')) * 1e6
        elif 'B' in value:
            return float(value.replace('B', '')) * 1e9
    return pd.to_numeric(value, errors='coerce')

def clean_data(df):
    # 1. Eliminar la primera columna sin encabezado
    df = df.iloc[:, 1:]
    
    # 2. Mover la columna 'Ticker' a la derecha de 'Symbol'
    if 'Ticker' in df.columns and 'Symbol' in df.columns:
        cols = df.columns.tolist()
        cols.insert(cols.index('Symbol') + 1, cols.pop(cols.index('Ticker')))
        df = df[cols]
    
    # 3. Reemplazar '--' con 0
    df.replace('--', 0, inplace=True)
    
    # 4. Convertir 'Price (Intraday)' a numérico
    if 'Price (Intraday)' in df.columns:
        df['Price (Intraday)'] = pd.to_numeric(df['Price (Intraday)'], errors='coerce')
    
    # 5. Limpiar la columna 'Change' y 'Change %'
    if 'Change' in df.columns:
        df['Change'] = df['Change'].str.replace('+', '', regex=False)
        df['Change'] = pd.to_numeric(df['Change'], errors='coerce')
    
    if 'Change %' in df.columns:
        df['Change %'] = df['Change %'].str.replace('+', '', regex=False)
        df['Change %'] = df['Change %'].str.replace('%', '', regex=False)
        df['Change %'] = pd.to_numeric(df['Change %'], errors='coerce') / 100
    
    # 6. Convertir Volume, Avg Vol (3M) y Market Cap a valores numéricos
    for col in ['Volume', 'Avg Vol (3M)', 'Market Cap']:
        if col in df.columns:
            df[col] = df[col].apply(convert_units)
    
    # 7. Limpiar P/E Ratio (TTM)
    if 'P/E Ratio (TTM)' in df.columns:
        df['P/E Ratio (TTM)'] = df['P/E Ratio (TTM)'].astype(str).str.replace('+', '', regex=False)
        df['P/E Ratio (TTM)'] = pd.to_numeric(df['P/E Ratio (TTM)'], errors='coerce')
    
    # 8. Eliminar columnas vacías
    df.dropna(axis=1, how='all', inplace=True)
    
    return df

def main():
    urls = {
        "Penny Stocks": "https://finance.yahoo.com/research-hub/screener/most_active_penny_stocks/?start={}&count=25",
        "Gainers": "https://finance.yahoo.com/markets/stocks/gainers/?start={}&count=25",
        "Losers": "https://finance.yahoo.com/markets/stocks/losers/?start={}&count=25",
        "Most Active": "https://finance.yahoo.com/markets/stocks/most-active/?start={}&count=25"
    }
    
    data_frames = {}
    for name, url in urls.items():
        df = fetch_data(name, url)
        if not df.empty:
            df.columns = df.columns.str.strip()
            if "Symbol" in df.columns:
                df["Ticker"] = df["Symbol"].str.split().str[-1]
            df = clean_data(df)
            df.dropna(axis=1, how='all', inplace=True)
            data_frames[name] = df
    
    output_file = "stocks_data.xlsx"
    if os.path.exists(output_file):
        os.remove(output_file)
    
    with pd.ExcelWriter(output_file) as writer:
        for sheet_name, df in data_frames.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print("Datos exportados exitosamente a stocks_data.xlsx")

if __name__ == "__main__":
    main()