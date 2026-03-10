# 🚀 Deployment Guide

## Pre-Deployment Checklist

- [x] All analysis complete
- [x] Results documented
- [x] Code reviewed
- [x] Dependencies listed (requirements.txt)
- [x] .gitignore configured
- [x] README updated

## Local Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Flight-Delay-Analysis
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Notebook
```bash
jupyter notebook Flight_delay_analysis.ipynb
```

## Deployment Options

### Option 1: Google Colab (Recommended for Quick Sharing)
1. Upload notebook to Google Drive
2. Open with Google Colab
3. Modify file paths to use `drive.mount('/content/drive')`
4. No local setup required

**Command:**
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Option 2: Azure Notebooks
1. Sign in to https://notebooks.azure.com
2. Create new project
3. Upload all files
4. Run directly in browser

### Option 3: Binder
1. Push to GitHub
2. Add badges to README
3. Generate Binder link from https://mybinder.org
4. Share for reproducible analysis

### Option 4: Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["jupyter", "notebook", "--ip=0.0.0.0"]
```

Build and run:
```bash
docker build -t flight-delay-analysis .
docker run -p 8888:8888 flight-delay-analysis
```

## Git Workflow

### Initial Setup
```bash
git init
git add .
git commit -m "Initial flight delay analysis"
git branch -M main
git remote add origin <repository-url>
git push -u origin main
```

### Updates
```bash
git add Flight_delay_analysis.ipynb
git commit -m "Update analysis with new visualizations"
git push origin main
```

## CI/CD Setup (GitHub Actions)

Create `.github/workflows/test.yml`:
```yaml
name: Test Notebook

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - run: pip install -r requirements.txt
    - run: jupyter nbconvert --to notebook --execute Flight_delay_analysis.ipynb
```

## Data Management

### Include CSV Files
- ✅ `airlines.csv` - Reference table (small)
- ✅ `airports.csv` - Reference table (small)
- ⚠️ `flights.csv` - Large file (~500MB+)

For large files, use Git LFS:
```bash
git lfs install
git lfs track "*.csv"
```

## Performance Optimization

For large datasets:
```python
# Read only needed columns
data = pd.read_csv('flights.csv', usecols=['AIRLINE', 'ARRIVAL_DELAY'])

# Use dtype optimization
data = pd.read_csv('flights.csv', dtype={'AIRLINE': 'category'})

# Use chunking for very large files
chunks = pd.read_csv('flights.csv', chunksize=10000)
for chunk in chunks:
    process(chunk)
```

## Monitoring & Logging

Track analysis runs:
```python
import logging
logging.basicConfig(filename='analysis.log', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Analysis started")
```

## Security Best Practices

1. **Never commit sensitive data** - Use .env for API keys
2. **Use .gitignore** - Already configured
3. **Review before push** - Always review changes
4. **Document assumptions** - Clearly state in notebook

## Troubleshooting

### ImportError for statsmodels
```bash
pip install --upgrade statsmodels
```

### Memory issues with large CSV
```python
# Use only delayed flights subset
df = pd.read_csv('flights.csv', nrows=50000)
```

### Notebook timeout
- Convert to Python script for batch processing
- Split analysis into smaller notebooks
- Use cloud computing resources

## Support

For issues:
1. Check Requirements Match Python version
2. Verify all CSV files are present
3. Clear notebook outputs and restart kernel
4. Check pandas/numpy versions compatibility

---

**Last Updated:** March 2026
