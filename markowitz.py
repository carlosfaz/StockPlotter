import yfinance as yf
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

"""
tickers_info = {
    # Technology
    "AAPL": ("Apple Inc.", "Technology"),
    "MSFT": ("Microsoft Corporation", "Technology"),
    "GOOGL": ("Alphabet Inc. (Google)", "Technology"),
    "AMZN": ("Amazon.com Inc.", "Technology"),
    "TSLA": ("Tesla Inc.", "Technology"),
    "NVDA": ("NVIDIA Corporation", "Technology"),
    "META": ("Meta Platforms Inc. (Facebook)", "Technology"),
    "INTC": ("Intel Corporation", "Technology"),
    "CSCO": ("Cisco Systems Inc.", "Technology"),
    "PYPL": ("PayPal Holdings Inc.", "Technology"),

    # Finance
    "V": ("Visa Inc.", "Finance"),
    "MA": ("Mastercard Incorporated", "Finance"),
    "GS": ("Goldman Sachs Group Inc.", "Finance"),
    "MS": ("Morgan Stanley", "Finance"),
    "AIG": ("American International Group Inc.", "Finance"),
    "SPGI": ("S&P Global Inc.", "Finance"),
    "AXP": ("American Express Co.", "Finance"),
    "JPM": ("JPMorgan Chase & Co.", "Finance"),
    "C": ("Citigroup Inc.", "Finance"),
    "BAC": ("Bank of America Corporation", "Finance"),

    # Consumer
    "KO": ("The Coca-Cola Company", "Consumer"),
    "PEP": ("PepsiCo Inc.", "Consumer"),
    "MCD": ("McDonald's Corporation", "Consumer"),
    "WMT": ("Walmart Inc.", "Consumer"),
    "TGT": ("Target Corporation", "Consumer"),
    "DIS": ("The Walt Disney Company", "Consumer"),
    "NKE": ("Nike Inc.", "Consumer"),
    "LULU": ("Lululemon Athletica Inc.", "Consumer"),
    "LOW": ("Lowe's Companies Inc.", "Consumer"),
    "HD": ("The Home Depot Inc.", "Consumer"),

    # Healthcare
    "PFE": ("Pfizer Inc.", "Healthcare"),
    "JNJ": ("Johnson & Johnson", "Healthcare"),
    "MDT": ("Medtronic PLC", "Healthcare"),
    "AMGN": ("Amgen Inc.", "Healthcare"),
    "CAT": ("Caterpillar Inc.", "Healthcare"),
    "SYK": ("Stryker Corporation", "Healthcare"),
    "BIIB": ("Biogen Inc.", "Healthcare"),
    "ISRG": ("Intuitive Surgical Inc.", "Healthcare"),
    "ZTS": ("Zoetis Inc.", "Healthcare"),
    "REGN": ("Regeneron Pharmaceuticals", "Healthcare"),

    # Energy
    "XOM": ("Exxon Mobil Corporation", "Energy"),
    "CVX": ("Chevron Corporation", "Energy"),
    "SLB": ("Schlumberger Limited", "Energy"),
    "COP": ("ConocoPhillips", "Energy"),
    "EOG": ("EOG Resources", "Energy"),
    "OXY": ("Occidental Petroleum", "Energy"),
    "PSX": ("Phillips 66", "Energy"),
    "VLO": ("Valero Energy", "Energy"),
    "MPC": ("Marathon Petroleum", "Energy"),
    "KMI": ("Kinder Morgan", "Energy"),

    # Industrials
    "RTX": ("Raytheon Technologies Corporation", "Industrials"),
    "AMAT": ("Applied Materials Inc.", "Industrials"),
    "AVGO": ("Broadcom Inc.", "Industrials"),
    "TSM": ("Taiwan Semiconductor Manufacturing Company", "Industrials"),
    "KLAC": ("KLA Corporation", "Industrials"),
    "LHX": ("L3Harris Technologies", "Industrials"),
    "NOC": ("Northrop Grumman Corporation", "Industrials"),
    "BA": ("Boeing Co.", "Industrials"),
    "CAT": ("Caterpillar Inc.", "Industrials"),
    "DE": ("Deere & Co.", "Industrials"),

    # Utilities
    "VZ": ("Verizon Communications Inc.", "Utilities"),
    "T": ("AT&T Inc.", "Utilities"),
    "NEE": ("NextEra Energy", "Utilities"),
    "DUK": ("Duke Energy", "Utilities"),
    "SO": ("Southern Company", "Utilities"),
    "XEL": ("Xcel Energy", "Utilities"),
    "AEP": ("American Electric Power", "Utilities"),
    "SRE": ("Sempra Energy", "Utilities"),
    "PCG": ("PG&E Corporation", "Utilities"),
    "EXC": ("Exelon Corporation", "Utilities"),

    # Consumer Goods
    "CL": ("Colgate-Palmolive Company", "Consumer Goods"),
    "CVS": ("CVS Health Corporation", "Consumer Goods"),
    "PG": ("Procter & Gamble Co.", "Consumer Goods"),
    "KO": ("Coca-Cola", "Consumer Goods"),
    "PEP": ("PepsiCo", "Consumer Goods"),
    "MDLZ": ("Mondelez International", "Consumer Goods"),
    "CPB": ("Campbell Soup Company", "Consumer Goods"),
    "GIS": ("General Mills", "Consumer Goods"),
    "SJM": ("The J.M. Smucker Company", "Consumer Goods"),
    "ADM": ("Archer Daniels Midland Company", "Consumer Goods"),

    # Retail
    "ROST": ("Ross Stores Inc.", "Retail"),
    "WBA": ("Walgreens Boots Alliance Inc.", "Retail"),
    "AMZN": ("Amazon.com Inc.", "Retail"),
    "TGT": ("Target Corporation", "Retail"),
    "WMT": ("Walmart Inc.", "Retail"),
    "M": ("Macy's Inc.", "Retail"),
    "KSS": ("Kohl's Corporation", "Retail"),
    "ULTA": ("Ulta Beauty Inc.", "Retail"),
    "JWN": ("Nordstrom Inc.", "Retail"),

    # Logistics
    "UPS": ("United Parcel Service, Inc.", "Logistics"),
    "FDX": ("FedEx Corporation", "Logistics"),
    "XPO": ("XPO Logistics", "Logistics"),
    "CHRW": ("C.H. Robinson Worldwide", "Logistics"),
    "OLN": ("Olin Corporation", "Logistics"),
    "LSTR": ("Landstar System Inc.", "Logistics"),
    "ODFL": ("Old Dominion Freight Line", "Logistics"),
    "KEX": ("Kirby Corporation", "Logistics"),
    "MATX": ("Matson Inc.", "Logistics")
}
"""


tickers_info = {
    # Technology
    "ORCL": ("Oracle Corporation", "Technology"),
    "ADBE": ("Adobe Inc.", "Technology"),
    "SAP": ("SAP SE", "Technology"),
    "TXN": ("Texas Instruments Inc.", "Technology"),
    "AMD": ("Advanced Micro Devices Inc.", "Technology"),
    "QCOM": ("Qualcomm Inc.", "Technology"),
    "SNOW": ("Snowflake Inc.", "Technology"),
    "WDAY": ("Workday Inc.", "Technology"),
    "PANW": ("Palo Alto Networks Inc.", "Technology"),
    "ZM": ("Zoom Video Communications Inc.", "Technology"),

    # Finance
    "BLK": ("BlackRock Inc.", "Finance"),
    "TROW": ("T. Rowe Price Group Inc.", "Finance"),
    "SCHW": ("Charles Schwab Corporation", "Finance"),
    "AMP": ("Ameriprise Financial Inc.", "Finance"),
    "PGR": ("Progressive Corporation", "Finance"),
    "MMC": ("Marsh & McLennan Companies", "Finance"),
    "ICE": ("Intercontinental Exchange Inc.", "Finance"),
    "MSCI": ("MSCI Inc.", "Finance"),
    "CME": ("CME Group Inc.", "Finance"),
    "COF": ("Capital One Financial Corp.", "Finance"),

    # Consumer
    "SBUX": ("Starbucks Corporation", "Consumer"),
    "CMG": ("Chipotle Mexican Grill Inc.", "Consumer"),
    "YUM": ("Yum! Brands Inc.", "Consumer"),
    "HLT": ("Hilton Worldwide Holdings Inc.", "Consumer"),
    "MAR": ("Marriott International Inc.", "Consumer"),
    "BKNG": ("Booking Holdings Inc.", "Consumer"),
    "RL": ("Ralph Lauren Corporation", "Consumer"),
    "TAP": ("Molson Coors Beverage Company", "Consumer"),
    "KDP": ("Keurig Dr Pepper Inc.", "Consumer"),
    "WHR": ("Whirlpool Corporation", "Consumer"),

    # Healthcare
    "UNH": ("UnitedHealth Group Inc.", "Healthcare"),
    "CI": ("Cigna Group", "Healthcare"),
    "BMY": ("Bristol-Myers Squibb", "Healthcare"),
    "ABBV": ("AbbVie Inc.", "Healthcare"),
    "LLY": ("Eli Lilly and Co.", "Healthcare"),
    "HUM": ("Humana Inc.", "Healthcare"),
    "VRTX": ("Vertex Pharmaceuticals", "Healthcare"),
    "DHR": ("Danaher Corporation", "Healthcare"),
    "BDX": ("Becton, Dickinson and Co.", "Healthcare"),

    # Energy
    "HAL": ("Halliburton Company", "Energy"),
    "BKR": ("Baker Hughes Company", "Energy"),
    "WMB": ("Williams Companies Inc.", "Energy"),
    "OKE": ("ONEOK Inc.", "Energy"),
    "HES": ("Hess Corporation", "Energy"),
    "FTI": ("TechnipFMC", "Energy"),
    "APA": ("APA Corporation", "Energy"),
    "MRO": ("Marathon Oil Corporation", "Energy"),
    "FANG": ("Diamondback Energy", "Energy"),

    # Industrials
    "GD": ("General Dynamics Corporation", "Industrials"),
    "LMT": ("Lockheed Martin Corporation", "Industrials"),
    "HON": ("Honeywell International Inc.", "Industrials"),
    "MMM": ("3M Company", "Industrials"),
    "GE": ("General Electric Company", "Industrials"),
    "ITW": ("Illinois Tool Works Inc.", "Industrials"),
    "EMR": ("Emerson Electric Co.", "Industrials"),
    "DOV": ("Dover Corporation", "Industrials"),
    "ETN": ("Eaton Corporation", "Industrials"),
    "ROK": ("Rockwell Automation", "Industrials"),

    # Utilities
    "DUK": ("Duke Energy Corporation", "Utilities"),
    "SO": ("Southern Company", "Utilities"),
    "XEL": ("Xcel Energy Inc.", "Utilities"),
    "AEP": ("American Electric Power", "Utilities"),
    "PCG": ("PG&E Corporation", "Utilities"),
    "EXC": ("Exelon Corporation", "Utilities"),
    "SRE": ("Sempra Energy", "Utilities"),
    "ED": ("Consolidated Edison Inc.", "Utilities"),
    "WEC": ("WEC Energy Group", "Utilities"),
    "PEG": ("Public Service Enterprise Group", "Utilities"),

    # Consumer Goods
    "KMB": ("Kimberly-Clark Corporation", "Consumer Goods"),
    "CLX": ("The Clorox Company", "Consumer Goods"),
    "HRL": ("Hormel Foods Corporation", "Consumer Goods"),
    "K": ("Kellogg Company", "Consumer Goods"),
    "TSN": ("Tyson Foods Inc.", "Consumer Goods"),
    "MKC": ("McCormick & Company", "Consumer Goods"),
    "TAP": ("Molson Coors Beverage Company", "Consumer Goods"),
    "LW": ("Lamb Weston Holdings Inc.", "Consumer Goods"),
    "BG": ("Bunge Limited", "Consumer Goods"),
    "CP": ("Canadian Pacific Kansas City", "Consumer Goods"),

    # Retail
    "COST": ("Costco Wholesale Corporation", "Retail"),
    "TJX": ("TJX Companies Inc.", "Retail"),
    "BBY": ("Best Buy Co. Inc.", "Retail"),
    "DG": ("Dollar General Corporation", "Retail"),
    "DLTR": ("Dollar Tree Inc.", "Retail"),
    "BURL": ("Burlington Stores Inc.", "Retail"),
    "KSS": ("Kohl's Corporation", "Retail"),
    "FL": ("Foot Locker Inc.", "Retail"),
    "ANF": ("Abercrombie & Fitch Co.", "Retail"),

    # Logistics
    "JBHT": ("J.B. Hunt Transport Services Inc.", "Logistics"),
    "WERN": ("Werner Enterprises Inc.", "Logistics"),
    "R": ("Ryder System Inc.", "Logistics"),
    "NSC": ("Norfolk Southern Corporation", "Logistics"),
    "CSX": ("CSX Corporation", "Logistics"),
    "UNP": ("Union Pacific Corporation", "Logistics"),
    "KNX": ("Knight-Swift Transportation Holdings", "Logistics"),
    "ARCB": ("ArcBest Corporation", "Logistics"),
    "MATX": ("Matson Inc.", "Logistics")
}



# Function to obtain historical data
def obtener_datos(tickers_info, start_date, end_date):
    tickers = list(tickers_info.keys())  # Get tickers from dictionary keys
    precios = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    retornos = precios.pct_change().dropna()
    
    # Check for null values
    if retornos.isnull().any().any():
        print("Warning: There are null values in returns.")
        retornos = retornos.dropna()
    
    return precios, retornos

# Calculate performance metrics and covariance matrix
def calcular_metricas(retornos):
    media_retornos = retornos.mean() * 252  # Annual returns
    cov_matrix = retornos.cov() * 252  # Annualized covariance matrix
    
    # Check if the covariance matrix has null values
    if cov_matrix.isnull().any().any():
        print("Warning: There are null values in the covariance matrix.")
        cov_matrix = cov_matrix.dropna(axis=0, how='all').dropna(axis=1, how='all')
    
    return media_retornos, cov_matrix

# Efficient frontier calculation
def frontera_eficiente(media_retornos, cov_matrix, num_puntos=100):
    num_activos = len(media_retornos)

    # Ensure there are no zeros in the covariance matrix diagonal
    if np.any(np.isclose(np.diagonal(cov_matrix), 0)):
        print("Warning: There are zeros in the covariance matrix diagonal, which could cause issues when inverting.")
        return [], [], []

    # Covariance matrix inversion with error handling
    try:
        inv_cov_matrix = np.linalg.inv(cov_matrix)
    except np.linalg.LinAlgError:
        print("Error: Covariance matrix is not invertible.")
        return [], [], []

    # Auxiliary vectors
    ones = np.ones(num_activos)

    # Calculate constants for the efficient frontier
    A = ones.T @ inv_cov_matrix @ ones
    B = ones.T @ inv_cov_matrix @ media_retornos
    C = media_retornos.T @ inv_cov_matrix @ media_retornos
    D = A * C - B**2

    # Ensure D is not close to zero (avoid division by zero)
    if np.isclose(D, 0): 
        return [], [], []

    # Range of target returns
    retornos_objetivo = np.linspace(media_retornos.min(), media_retornos.max(), num_puntos)

    # Initialize results
    riesgos = []
    retornos = []
    pesos = []

    # Iterate over each target return
    for mu in retornos_objetivo:
        lambda1 = (C - B * mu) / D
        lambda2 = (A * mu - B) / D
        w = lambda1 * inv_cov_matrix @ ones + lambda2 * inv_cov_matrix @ media_retornos

        # Calculate risk and store results
        riesgo = np.sqrt(w.T @ cov_matrix @ w)
        riesgos.append(riesgo)
        retornos.append(mu)
        pesos.append(w)

    return riesgos, retornos, pesos

# Plot efficient frontier for each industry
def graficar_frontera_eficiente(media_retornos, cov_matrix, riesgos, retornos, tickers_info, industria):
    fig = go.Figure()

    # Points for stocks with full names
    for ticker, (nombre_completo, _) in tickers_info.items():
        i = list(tickers_info.keys()).index(ticker)  # Get ticker index
        fig.add_trace(go.Scatter(
            x=[np.sqrt(cov_matrix.iloc[i, i])],  # Standard deviation
            y=[media_retornos.iloc[i]],  # Expected return using iloc[]
            mode='markers+text',
            text=nombre_completo,  # Display full name instead of ticker
            name=ticker,
            textposition="top center",
            marker=dict(size=10, color="red", line=dict(width=1))
        ))

    # Efficient frontier
    fig.add_trace(go.Scatter(
        x=riesgos,
        y=retornos,
        mode='lines',
        name='Efficient Frontier',
        line=dict(color='blue', width=2)
    ))

    fig.update_layout(
        title=f"Efficient Frontier for the {industria} Industry",
        xaxis_title="Risk (Standard Deviation)",
        yaxis_title="Expected Return",
        showlegend=True,
        width=1200,  # Figure width in pixels
        height=800   # Figure height in pixels
    )

    return fig

# Check if a ticker is active
def is_ticker_active(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            print(f"Warning: {ticker} has no data within the given date range.")
            return False
        return True
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return False


# Fecha de inicio y fin
start_date = '2020-01-01'
end_date = '2024-11-24'

# Obtener precios y retornos
precios, retornos = obtener_datos(tickers_info, start_date, end_date)
media_retornos, cov_matrix = calcular_metricas(retornos)

# Agrupar los tickers por industria y excluir los inactivos
industries = {}
for ticker, (nombre_completo, industria) in tickers_info.items():
    if is_ticker_active(ticker, start_date, end_date):  # Comprobar si el ticker tiene datos válidos
        if industria not in industries:
            industries[industria] = []
        industries[industria].append(ticker)

# Recorrer cada industria para calcular la frontera eficiente y el mix de activos
for industria, tickers in industries.items():
    # Filtrar tickers disponibles en precios para esta industria
    tickers_disponibles = [ticker for ticker in tickers if ticker in precios.columns]

    if tickers_disponibles:
        # Calcular frontera eficiente para la industria
        riesgos, retornos_frontera, pesos = frontera_eficiente(
            media_retornos[tickers_disponibles], 
            cov_matrix.loc[tickers_disponibles, tickers_disponibles]
        )

        # Verificación de que los resultados no están vacíos
        if not riesgos or not retornos_frontera or not pesos:
            print(f"Error al calcular la frontera eficiente para la industria {industria}. Verifica los datos.")
        else:
            # Obtener el mix de activos sugerido (puedes elegir el portafolio con el retorno máximo, mínimo riesgo, etc.)
            indice_optimo = np.argmax(retornos_frontera)
            pesos_optimos = pesos[indice_optimo]

            # Normalizar los pesos para que sumen 1 y asegurarnos de que no haya valores negativos
            pesos_optimos = np.maximum(pesos_optimos, 0)  # Eliminar los pesos negativos
            pesos_optimos = pesos_optimos / np.sum(pesos_optimos)  # Normalizar los pesos para que sumen 1
            
            # Mostrar el mix sugerido por industria
            print(f"\nMix sugerido por el modelo para la industria {industria}:")
            
            # Crear una lista de tuplas con ticker, nombre y peso
            mix_sugerido = [(tickers_info[ticker], ticker, pesos_optimos[i] * 100) for i, ticker in enumerate(tickers_disponibles)]
            
            # Ordenar la lista de mayor a menor según el peso (porcentaje)
            mix_sugerido = sorted(mix_sugerido, key=lambda x: x[2], reverse=True)
            
            # Imprimir el mix ordenado
            for nombre, ticker, peso in mix_sugerido:
                print(f"{nombre} ({ticker}): {peso:.2f}%")
    else:
        print(f"No hay tickers disponibles para la industria {industria}.")


# Generate plots and save to HTML file
html_filename = 'efficient_frontier_industries.html'
with open(html_filename, 'w', encoding='utf-8') as f:  # UTF-8 encoding
    f.write('<html><body>')
    
    for industria, tickers in industries.items():
        # Filter available tickers in the prices (those that have no NaN)
        tickers_disponibles = [ticker for ticker in tickers if ticker in precios.columns]

        # Calculate efficient frontier
        riesgos, retornos, _ = frontera_eficiente(media_retornos[tickers_disponibles], cov_matrix.loc[tickers_disponibles, tickers_disponibles])

        # Generate plot for the industry
        fig = graficar_frontera_eficiente(media_retornos[tickers_disponibles], cov_matrix.loc[tickers_disponibles, tickers_disponibles], riesgos, retornos, {ticker: tickers_info[ticker] for ticker in tickers_disponibles}, industria)
        
        # Write each figure as HTML inside the file, one below the other
        f.write(f'<h2>{industria} Industry</h2>')
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))  # Include Plotly.js from CDN

    f.write('</body></html>')

print(f"All charts have been saved to {html_filename}")
