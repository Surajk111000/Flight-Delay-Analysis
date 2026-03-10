#!/usr/bin/env bash
# Quick Start Setup Script

echo "🚀 Flight Delay Analysis Setup..."
echo ""

# Check Python
echo "✓ Checking Python installation..."
python --version

# Create virtual environment
echo "✓ Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✓ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt

# Verify installation
echo "✓ Verifying installation..."
python -c "import pandas, numpy, matplotlib, seaborn, statsmodels; print('✅ All libraries imported successfully!')"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the analysis:"
echo "  jupyter notebook Flight_delay_analysis.ipynb"
echo ""
echo "To deactivate environment:"
echo "  deactivate"
