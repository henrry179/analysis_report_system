@echo off
set INPUT_FILE=data/sales.csv
set OUTPUT_DIR=reports/
set TEMPLATE=templates/default.md
python src/main.py --input "%INPUT_FILE%" --output "%OUTPUT_DIR%" --template "%TEMPLATE%"
