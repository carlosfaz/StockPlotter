import time
import pandas as pd
import yfinance as yf
from outfiter import *

start_time = time.time()

print(f"Empezando en {time.time() - start_time:.2f}.")

# Obtener la fecha actual
date = time.strftime("%d.%m.%Y")
filename = "Acciones1 "+ date + ".xlsx"

# Leer los tickers desde el archivo
df = pd.read_csv("tickers/sp500x.txt")
tickers = df["0"].to_list()

inactive_tickers = pd.read_csv("tickers/inactive_tickers.txt")
in_tickers = inactive_tickers["0"].to_list()
tickers = [ticker for ticker in tickers if ticker not in in_tickers]

# Función para mostrar una barra de progreso
def mostrar_progreso(actual, total, largo_barra=30):
    progreso = actual / total
    longitud_completada = int(largo_barra * progreso)
    barra = "=" * longitud_completada + "-" * (largo_barra - longitud_completada)
    porcentaje = progreso * 100
    print(f"\r[{barra}] {porcentaje:.2f}%", end="", flush=True)


# Función para sanitizar nombres de las hojas
def sanitizar_nombre(nombre):
    """Reemplaza caracteres no válidos en nombres de hojas de Excel."""
    caracteres_no_validos = ['/', '\\', '*', '?', '[', ']', ':']
    for char in caracteres_no_validos:
        nombre = nombre.replace(char, '_')
    return nombre[:31]  # Truncar a 31 caracteres

def obtener_informacion_financiera(tickers):
    info_financiera = {}
    total_tickers = len(tickers)
    tickers_verificados = 0

    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            if not info:
                raise ValueError("No data fetched")

            # Extraer valores y redondear a 2 decimales
            revenue = round(info.get("totalRevenue", 0), 2)
            net_income = round(info.get("netIncomeToCommon", 0), 2)
            ebitda = round(info.get("ebitda", 0), 2)
            revenue_growth = round(info.get("revenueGrowth", 0) * 100, 2)
            profit_margin = round(info.get("profitMargins", 0) * 100, 2)
            operating_margin = round(info.get("operatingMargins", 0) * 100, 2)
            roe = round(info.get("returnOnEquity", 0) * 100, 2)

            # Indicadores adicionales
            roa = round(info.get("returnOnAssets", 0) * 100, 2)  # Retorno sobre activos
            current_ratio = round(info.get("currentRatio", 0), 2)  # Razón de liquidez corriente
            quick_ratio = round(info.get("quickRatio", 0), 2)  # Prueba ácida
            pe_ratio = round(info.get("trailingPE", 0), 2)  # P/E Ratio
            ps_ratio = round(info.get("priceToSalesTrailing12Months", 0), 2)  # Relación P/S
            pb_ratio = round(info.get("priceToBook", 0), 2)  # Relación P/B
            interest_coverage = round(info.get("ebitda", 0) / info.get("totalDebt", 1), 2)  # Cobertura de intereses

            # Calcular PEG (manual si no está disponible)
            if pe_ratio > 0 and revenue_growth > 0:
                peg_ratio = round(pe_ratio / revenue_growth, 2)
            else:
                peg_ratio = 0

            # Definir puntajes
            puntaje_peg = 5 if peg_ratio <= 1 else (3 if peg_ratio <= 2 else 1)
            puntaje_pe = 5 if pe_ratio <= 20 else (3 if pe_ratio <= 30 else 1)
            puntaje_pb = 5 if pb_ratio <= 1 else (3 if pb_ratio <= 3 else 1)
            puntaje_ps = 5 if ps_ratio <= 1 else (3 if ps_ratio <= 3 else 1)
            puntaje_roe = 5 if roe >= 15 else (3 if roe >= 5 else 1)
            puntaje_roa = 5 if roa >= 5 else (3 if roa >= 2 else 1)
            puntaje_revenue_growth = 5 if revenue_growth >= 10 else (3 if revenue_growth >= 5 else 1)
            puntaje_profit_margin = 5 if profit_margin >= 10 else (3 if profit_margin >= 5 else 1)
            puntaje_operating_margin = 5 if operating_margin >= 10 else (3 if operating_margin >= 5 else 1)
            puntaje_de = 5 if round(info.get("debtToEquity", 0), 2) <= 1 else (3 if round(info.get("debtToEquity", 0), 2) <= 2 else 1)

            # Puntaje total
            puntaje_total = (puntaje_peg + puntaje_pe + puntaje_pb + puntaje_ps + puntaje_roe + 
                             puntaje_roa + puntaje_revenue_growth + puntaje_profit_margin + puntaje_operating_margin + puntaje_de)

            # Guardar la información en un diccionario
            info_financiera[ticker] = {
                "Nombre": info.get("longName", "N/A"),
                "Ticker": ticker,
                "PEG": peg_ratio,
                "P/E": pe_ratio,
                "P/B": pb_ratio,
                "P/S": ps_ratio,
                "ROE (%)": roe,
                "ROA (%)": roa,
                "Revenue Growth (%)": revenue_growth,
                "Profit Margin (%)": profit_margin,
                "Operating Margin (%)": operating_margin,
                "D/E": round(info.get("debtToEquity", 0), 2),
                "Current Ratio": current_ratio,
                "Quick Ratio": quick_ratio,
                "Interest Coverage": interest_coverage,
                "Div Yld": round(info.get("dividendYield", 0) * 100, 2),
                "Beta": round(info.get("beta", 0), 2),
                "Revenue": revenue,
                "Net Income": net_income,
                "EBITDA": ebitda,
                "Vol": round(info.get("fiftyDayAverage", 0), 2),
                "Sector": info.get("sector", "N/A"),
                "Currency": info.get("currency", "N/A"),
                "EPS": round(info.get("trailingEps", 0), 2),
                "BV": round(info.get("bookValue", 0), 2),
                "Div/Sh": round(info.get("dividendRate", 0), 2),
                "Puntaje": puntaje_total,  # Nuevo puntaje total
            }
        except Exception:
            pass

        tickers_verificados += 1
        mostrar_progreso(tickers_verificados, total_tickers)

    print()
    return info_financiera

# Exportar información financiera a un archivo Excel con una pestaña por industria y una pestaña consolidada
def exportar_a_excel(info_financiera, filename=filename):
    sectores = {}
    todas_las_empresas = []

    # Agrupar por sector y también crear una lista consolidada
    for ticker, data in info_financiera.items():
        sector = data.get("Sector", "N/A")
        if sector not in sectores:
            sectores[sector] = []
        sectores[sector].append(data)
        todas_las_empresas.append(data)  # Agregar a la lista consolidada

    # Crear un archivo Excel con una hoja por cada sector y una hoja con todas las industrias
    with pd.ExcelWriter(filename) as writer:
        for sector, empresas in sectores.items():
            nombre_sanitizado = sanitizar_nombre(sector)  # Sanitizar nombre
            df_sector = pd.DataFrame(empresas)
            df_sector.to_excel(writer, sheet_name=nombre_sanitizado, index=False)

        # Crear la pestaña consolidada con todas las industrias
        df_todas_industrias = pd.DataFrame(todas_las_empresas)
        df_todas_industrias.to_excel(writer, sheet_name="Todas las industrias", index=False)

    print(f"Archivo Excel guardado como {filename}.")
    
    
# Procesar tickers y exportar resultados
def procesar_tickers(tickers):
    print("Obteniendo información financiera...")
    info_financiera = obtener_informacion_financiera(tickers)
    exportar_a_excel(info_financiera)


# Ejecución
procesar_tickers(tickers)
procesar_excel(filename)

print(f"Código finalizado en {time.time() - start_time:.2f} segundos.")