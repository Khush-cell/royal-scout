
# Royal Scout – Pressure Performance Intelligence

Royal Scout is a cricket analytics dashboard designed to identify reliable batters and bowlers in high-pressure T20 chase situations.

The project analyses ball-by-ball cricket data from IPL seasons 2022 onwards and T20 Internationals to evaluate player performance under pressure.

##  Project Objective

Identify the most reliable batters and bowlers when a T20 chase becomes challenging.

Rather than relying only on traditional statistics, Royal Scout evaluates performance using pressure-specific metrics and a weighted reliability scoring model.

##  Features

- Tournament intelligence overview
- Top 10 reliable batter rankings
- Top 10 reliable bowler rankings
- Player performance analysis
- Pressure-based performance comparison
- Interactive visualisations
- Research methodology and data assumptions

##  Dataset

The analysis uses the supplied ball-by-ball cricket dataset.

| Dataset metric | Records / Count |
|---|---:|
| Deliveries | 194,014 |
| Matches | 837 |
| Unique batters | 824 |
| Unique bowlers | 596 |

The primary chase analysis focuses on completed, non-DLS/D-L second innings.

## Reliability Scoring

### Batter reliability

| Metric | Weight |
|---|---:|
| High-pressure strike rate | 30% |
| Strike-rate improvement | 25% |
| High-pressure runs | 20% |
| Runs per dismissal | 15% |
| Boundary percentage | 10% |

### Bowler reliability

| Metric | Weight |
|---|---:|
| High-pressure economy | 30% |
| Economy improvement | 25% |
| High-pressure wickets | 20% |
| Bowling average | 15% |
| Bowling strike rate | 10% |

The final scores are weighted percentile-based scores relative to the eligible player pool.

## Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Parquet / CSV

##  Project Structure

```text
ROYAL-SCOUT/
│
├── analysis/
│   └── Data preparation and analysis scripts
│
├── dashboard/
│   └── Dashboard-related files
│
├── data/
│   ├── raw/
│   └── processed/
│
├── app.py
├── requirements.txt
└── README.md
```

##  Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd royal-scout
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser.

##  Methodology Notes

- Pressure thresholds are rule-based analytical choices.
- Normal-pressure comparisons use normal-pressure deliveries from second-innings chases.
- DLS/D-L and abandoned or no-result matches are excluded from the primary chase analysis.
- The reliability score is a comparative analytical measure, not a prediction of future performance.

## Project

**Royal Scout – Pressure Performance Intelligence**

Cricket analytics project developed for the Rajasthan Royals Unstop Hackathon.
