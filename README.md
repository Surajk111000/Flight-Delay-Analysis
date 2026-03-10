# ✈️ Flight Delay Analysis: US Airlines Performance Study

A comprehensive data science project analyzing flight delays across 14 major US airlines using 2015 flight data.

**GitHub Repository:** https://github.com/Surajk111000/Flight-Delay-Analysis

## 📊 Project Overview

This analysis explores patterns in flight delays to:
- Identify which airlines have the highest delay rates
- Discover correlations between delays and operational factors
- Evaluate the impact of hub-and-spoke operations on flight performance

**Key Findings:**
- Spirit Airlines has the highest delay percentage (22.58%)
- Late inbound aircraft and air system delays are primary causes
- Weekend flights experience higher delays than weekday flights
- Hub-and-spoke model increases delays due to traffic concentration

## 📁 Project Structure

```
Flight-Delay-Analysis/
├── Flight_delay_analysis.ipynb    # Main analysis notebook
├── airlines.csv                    # Airline reference data
├── airports.csv                    # Airport reference data
├── flights.csv                     # Flight details and delays
└── README.md                       # Documentation
```

## 🔍 Methodology

### Data Processing
- **Dataset:** 14 major US airlines, 2015 flight records
- **Delay Definition:** FAA standard - arrival ≥15 minutes late
- **Records Analyzed:** ~100,000+ flight records
- **Data Cleaning:** Removed cancelled/diverted flights

### Analysis Techniques
1. **Descriptive Statistics** - Baseline airline/delay metrics
2. **Categorical Analysis** - Visualization by airline, day, delay type
3. **Linear Regression** - Predictive modeling (Adj R² = 0.971)
4. **Comparative Analysis** - Hub vs. non-hub airport performance

## 🎯 Key Findings

### 1. Airline Performance Ranking
| Rank | Airline | Delay % |
|------|---------|----------|
| 1    | Spirit      | 22.58% |
| 2    | Frontier    | 20.21% |
| 3    | JetBlue     | 19.43% |

### 2. Delay Root Causes
- **Air System Delay** - Primary factor
- **Late Aircraft** - Cascading effect
- **Weather Delay** - Secondary factor

### 3. Weekly Patterns
- Weekend flights: 2-3% higher delays
- Monday peak: Post-weekend congestion
- Wednesday-Friday: More stable performance

### 4. Regression Model Results
```
Adjusted R²: 0.971 (explains 97.1% of variation)
F-statistic: Highly significant (p < 0.001)
All predictors: Statistically significant
```

## 📈 Insights & Recommendations

### For Airlines
1. **Operational Buffer:** Increase turnover time to prevent cascade delays
2. **Scheduling:** Reduce peak-hour concentrations
3. **Resource Planning:** Focus on ground handling efficiency

### For Hub Operations
1. **Capacity Management:** Stagger flights during peak hours
2. **Fleet Maintenance:** Better predictive scheduling
3. **Route Optimization:** Consider non-hub alternatives

## 💻 Technical Stack

- Python 3.8+
- pandas, numpy, matplotlib, seaborn, statsmodels
- Jupyter Notebook

## 📥 Installation & Usage

1. Ensure data files (airlines.csv, airports.csv, flights.csv) are present
2. Install dependencies: `pip install pandas numpy matplotlib seaborn statsmodels`
3. Open `Flight_delay_analysis.ipynb` in Jupyter Notebook
4. Execute cells sequentially

## 📊 Data Source
- **Source:** Kaggle - Department of Transportation
- **URL:** https://www.kaggle.com/usdot/flight-delays
- **Retrieved:** May 30, 2023

## 👤 Author
**Suraj Kumar** - 22M0014@iitb.ac.in (IIT Bombay)

## ⚠️ Dataset Limitations
- Time Period: 2015 only
- Coverage: 14 major US carriers only
- Scope: Domestic flights only
- Note: Pre-COVID era data

## 🚀 Live Dashboard

🎉 **Interactive Streamlit Dashboard Now Available!**

Access the live dashboard here: **https://flight-delay-analysis-ifed3pvjfjdfqpz3hmqgt8.streamlit.app/**

### Features:
- 📊 Interactive airline comparison charts
- 📅 Weekly and monthly delay patterns
- ✈️ Top routes analysis
- 🔍 Real-time filtering by airline, month, and delay threshold
- 📥 CSV data export capability

## 🚀 Deployment Ready
✅ All dependencies are standard libraries
✅ Can be deployed on cloud platforms
✅ Exportable to Python script
✅ Compatible with dashboarding tools

---

**Status:** Analysis Complete ✅ | **Deployed:** March 2026 | **Updated:** March 2026
