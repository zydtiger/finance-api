# README for Finance API

> **DISCLAIMER**
>
> The Finance API collects data using the yfinance library, which retrieves publicly available data from Yahoo Finance, and also crawls data from Finviz. This API is intended for research and educational purposes only and is not affiliated with, endorsed by, or associated with Yahoo, Inc. or Finviz in any way.
>
> Yahoo Finance and its associated trademarks are the property of Yahoo, Inc. Users are encouraged to review Yahoo's terms of service and usage guidelines to ensure compliance when using the data. The data provided by this API is intended for personal use and should not be used in ways that violate any copyright or terms of service agreements.
>
> This software is built with the goal of supporting learning and research, and it is not designed to infringe upon any intellectual property rights or protected content. Users are responsible for ensuring their own compliance with applicable laws and regulations.

Welcome to the **Finance API**! This API provides various endpoints to access financial data, including historical stock prices, financial statements, and company metadata. Below is an overview of the available endpoints and their functionalities.

## Endpoints

### 1. **Get Historical Data**

- **Endpoint:** `/history/{ticker}`
- **Description:** Retrieve historical stock price data for a specified ticker.

### 2. **Get Intraday Data**

- **Endpoint:** `/intraday/{ticker}`
- **Description:** Fetch intraday stock price data for a specific ticker.

### 3. **Get Income Statement**

- **Endpoint:** `/income/{ticker}`
- **Description:** Access the income statement of a company for a given ticker.

### 4. **Get Cashflow Statement**

- **Endpoint:** `/cashflow/{ticker}`
- **Description:** Retrieve the cashflow statement of a company for a specific ticker.

### 5. **Get Balance Sheet**

- **Endpoint:** `/balance/{ticker}`
- **Description:** Obtain the balance sheet of a company for the given ticker.

### 6. **Get SEC Filings**

- **Endpoint:** `/sec/{ticker}`
- **Description:** Access SEC filings for a specific company ticker.

### 7. **Get Tags**

- **Endpoint:** `/tags/{ticker}`
- **Description:** Retrieve Finviz tags related to a particular ticker.

### 8. **Get Metainfo**

- **Endpoint:** `/metainfo/{ticker}`
- **Description:** Fetch detailed metadata about a company, such as full name, exchange, market cap, and financial ratios.

### 9. **Get News**

- **Endpoint:** `/news/{ticker}`
- **Description:** Access the latest news articles related to a specific ticker.

## How to Use

To explore and test the API endpoints, visit the Swagger UI at `/docs`.

## License

This project is licensed under the [MIT License](./LICENSE).
