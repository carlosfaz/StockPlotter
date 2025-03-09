# Stock Data Scraper (yahoo_webscrapper_v0.1.py)

This script extracts financial data from Yahoo Finance and saves it in an Excel file with different tabs for each data category.

## Features
- Retrieves data from the following stock categories:
  - Penny Stocks
  - Gainers (rising stocks)
  - Losers (declining stocks)
  - Most Active (most traded stocks)
- Scrapes up to 125 records per category in blocks of 25.
- Displays a progress bar in the terminal during data extraction.
- Exports the data to a `stocks_data.xlsx` file with each category in a separate sheet.

## Requirements
This script uses the following Python libraries:
- `requests`
- `pandas`
- `BeautifulSoup4`
- `os`
- `time`

Make sure these libraries are installed before running the script. You can install them with:
```sh
pip install requests pandas beautifulsoup4
```

## Usage
To run the script, simply execute the following command in the terminal:
```sh
python yahoo_webscrapper_v0.1.py
```
The script will automatically extract the data and save it in `stocks_data.xlsx`.

## Code Structure
1. **`get_data_from_url(url)`**: Downloads and extracts data from a table on the given web page.
2. **`fetch_data(name, base_url)`**: Iterates through pages of a specific category and consolidates the data.
3. **`main()`**: Runs all functions, retrieves data from all categories, and saves it in an Excel file.

## Output
The `stocks_data.xlsx` file will contain:
- **Penny Stocks** in one sheet
- **Gainers** in another sheet
- **Losers** in another sheet
- **Most Active** in another sheet

Each sheet includes an additional `Ticker` column, which correctly extracts the stock symbol.

## Notes
- A `time.sleep(1)` delay has been included to prevent request blocking.
- It is recommended not to run the script repeatedly in short timeframes to avoid Yahoo Finance restrictions.
# _____________________________________________________________
# Stock Financial Analysis Tool (tabulador_excel.py)

This script retrieves financial information of publicly traded companies using Yahoo Finance and saves it in an Excel file organized by sectors.

## Features
- Retrieves financial information for multiple tickers from a text file.
- Filters and removes inactive tickers.
- Calculates key financial metrics such as:
  - Revenue, Net Income, EBITDA
  - ROE, ROA, P/E, P/B, P/S
  - Profit and operating margins
  - Debt-to-equity ratio (D/E)
  - Financial ratios like Current Ratio and Quick Ratio
  - Interest coverage and PEG Ratio
- Assigns a score to each company based on its financial metrics.
- Organizes the data into an Excel file with separate sheets for each sector and a consolidated sheet.
- Displays a progress bar in the terminal.

## Requirements
This script uses the following Python libraries:
- `pandas`
- `yfinance`
- `time`

Make sure these libraries are installed before running the script. You can install them with:
```sh
pip install pandas yfinance
```

## Usage
To run the script, simply execute the following command in the terminal:
```sh
python tabulador_excel.py
```
The script will read tickers from `tickers/sp500x.txt`, remove inactive ones from `tickers/inactive_tickers.txt`, and process the data.

## Code Structure
1. **Reading Tickers**: Loads tickers from a text file and excludes inactive ones.
2. **`obtener_informacion_financiera(tickers)`**: Retrieves key metrics for each company from Yahoo Finance.
3. **Company Scoring**: Assigns a score based on key financial metrics.
4. **`exportar_a_excel(info_financiera, filename)`**: Saves the data into an Excel file with sector-based sheets and a consolidated sheet.
5. **Execution Process**: Displays a progress bar in the terminal while processing tickers.

## Output
The generated Excel file contains:
- **A sheet for each sector**, grouping companies by industry.
- **A consolidated sheet** with all companies' data.

Each sheet includes key financial metrics along with the assigned total score.

## Notes
- A `time.sleep(1)` delay has been included to prevent request blocking.
- The Excel file name includes the current date to differentiate executions.
- The function `sanitizar_nombre(nombre)` ensures valid sheet names in Excel.

