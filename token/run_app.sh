#!/bin/bash

export APP_ENV=prd
source venv/bin/activate

echo "Launch API"
python app.py
