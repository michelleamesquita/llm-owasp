#!/bin/bash

# Script para iniciar a aplicação com o venv correto (Python 3.11 + modelscan)

cd "$(dirname "$0")"

echo "=========================================="
echo "🔴 Sentiment Backdoor + ModelScan Demo"
echo "=========================================="
echo ""

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo "❌ venv not found!"
    echo "Creating venv with Python 3.11..."
    python3.11 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "✅ venv found"
fi

# Ativar venv
echo "Activating venv..."
source venv/bin/activate

# Verificar Python version
echo "Python version: $(python --version)"

# Verificar se modelscan está instalado
if ! command -v modelscan &> /dev/null; then
    echo "⚠️  modelscan not found! Installing..."
    pip install modelscan rich
fi

echo "modelscan version: $(modelscan --version)"
echo ""

# Matar processos antigos na porta 5003
OLD_PID=$(lsof -ti:5003 2>/dev/null)
if [ ! -z "$OLD_PID" ]; then
    echo "Killing old process on port 5003 (PID: $OLD_PID)"
    kill $OLD_PID 2>/dev/null
    sleep 1
fi

echo "=========================================="
echo "Starting Flask application..."
echo "Access: http://localhost:5003"
echo "=========================================="
echo ""

# Iniciar aplicação
python app.py

