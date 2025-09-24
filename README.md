# RealTime-AutonomousWeatherTrading  

In this project, David Bukowski and I explore how weather- and temperature-based signals can be leveraged to forecast commodity prices, with particular attention to their relationship to oil and coal.  

The project serves two purposes:  

1. Research – testing whether weather and climate anomalies provide predictive power in commodity markets.  
2. Engineering – showcasing technical proficiency in real-time data services, API integration, and end-to-end system design.  

---

## Project Structure  

- `signals_72.0.csv`  
  Engineered weather/temperature signals (e.g., rolling anomalies, indices) that act as features for forecasting models.  

- `PnLBook.py`  
  Implements a profit-and-loss ledger using a queue-based data structure for trade matching. This approach was introduced to us by our professor, Sebastien Donadio, who has written extensively on efficient P&L tracking. By using a FIFO-style queue, trades can be stored and unwound in order, enabling accurate and computationally efficient real-time P&L calculations.  

- Real-time Data Services  
  - `oceandataserver.py` – API for serving weather/ocean data.  
  - `stockdataserver.py` – API for serving commodity/market data.  
  These run as services that deliver structured data in real time.  

- Clients  
  - `oceandataclient.py` – Example client that queries the ocean/weather API.  
  - `client.py` – Example client that retrieves commodity data.  
  Demonstrates API consumption, parsing, and programmatic integration.  

- `analyzing_trades.ipynb`  
  Jupyter notebook for exploratory analysis of signals, trades, and P&L outcomes.  

---

## Getting Started  

### 1. Clone the repo  
```bash
git clone https://github.com/ZachFara/RealTime-AutonomousWeatherTrading.git
cd RealTime-AutonomousWeatherTrading
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Launch real-time data services
```bash
uvicorn oceandataserver:app --reload --port 8001
uvicorn stockdataserver:app --reload --port 8002
```

### 4. Run example clients
```bash
python oceandataclient.py
python client.py
```

### 5. Explore signals and backtests
```bash
jupyter notebook analyzing_trades.ipynb
```

---

## Technical Highlights
- Real-time data services – built FastAPI/UVicorn servers for weather and commodity markets.
- API integration – designed clients to consume, parse, and combine multiple data streams.
- System interaction – servers, clients, and analysis scripts interact in a service-oriented architecture.
- Data engineering – created engineered weather/temperature signals for predictive modeling.
- Backtesting and risk accounting – implemented P&L tracking (PnLBook.py) using a queue-based data structure inspired by Sebastien Donadio’s work on efficient real-time P&L tracking.
- Exploratory analysis – notebook workflows for testing hypotheses and visualizing results.

---

## Roadmap
- [ ] Add containerization (Dockerfile, docker-compose.yml) for reproducible deployment
- [ ] Expand signal library (HDD/CDD, precipitation, wind anomalies)
- [ ] Develop full backtesting engine with metrics like Sharpe ratio, drawdown, turnover
- [ ] Automate data pipelines with scheduled jobs
- [ ] Integrate visualization dashboards (Plotly/Streamlit)

---

## Summary
This project demonstrates the ability to:
- Bridge data science and software engineering: applying weather-driven predictive models to real markets while building APIs and services around the workflow.
- Design and test end-to-end trading infrastructure: from signal generation, to service hosting, to client interaction, to trade analysis.
It is both a research experiment in weather-based forecasting and a technical showcase of system design and implementation.
