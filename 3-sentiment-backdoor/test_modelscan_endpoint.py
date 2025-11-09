#!/usr/bin/env python3
"""
Script para testar o endpoint /modelscan
Verifica se o modelscan subprocess está funcionando corretamente
"""

import requests
import json

print("=" * 70)
print("TESTANDO ENDPOINT /modelscan")
print("=" * 70)
print()

# URL base
BASE_URL = "http://localhost:5003"

print("1️⃣  Testando QUICK SCAN (sem subprocess)...")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/modelscan?quick=true", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Scan Method: {data.get('scan_method')}")
        print(f"✅ Status Result: {data.get('status')}")
        print(f"✅ Critical Issues: {data.get('findings', {}).get('critical_issues')}")
        print(f"✅ Dangerous Ops: {len(data.get('findings', {}).get('dangerous_operations', []))}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")

print()
print("2️⃣  Testando FULL MODELSCAN (COM subprocess)...")
print("-" * 70)
print("⚠️  Isso pode demorar até 2 minutos...")
try:
    response = requests.get(f"{BASE_URL}/modelscan", timeout=150)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"✅ ModelScan Installed: {data.get('modelscan_installed')}")
        print(f"✅ Status Result: {data.get('status')}")
        print(f"✅ Model Path: {data.get('model_path')}")
        print(f"✅ Model Size: {data.get('model_size')} bytes")
        print()
        
        if 'scan_result' in data:
            print("📊 MODELSCAN OUTPUT:")
            print("-" * 70)
            print(data['scan_result']['output'])
            print("-" * 70)
            print(f"Exit Code: {data['scan_result']['exit_code']}")
        
        if 'findings' in data:
            print()
            print("🔍 FINDINGS:")
            print(f"  - Critical Issues: {data['findings'].get('critical_issues')}")
            print(f"  - Backdoor Indicators: {data['findings'].get('backdoor_indicators')}")
            print(f"  - Unsafe Operations: {data['findings'].get('unsafe_operations')}")
        
        if 'recommendations' in data:
            print()
            print("📋 RECOMMENDATIONS:")
            for rec in data['recommendations'][:3]:
                print(f"  - {rec}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
except requests.exceptions.Timeout:
    print("❌ TIMEOUT: Request took more than 150 seconds")
    print("   Isso indica que o modelscan está rodando mas muito lento")
    print("   Tente executar manualmente: modelscan scan -p sentiment_model.pkl")
except Exception as e:
    print(f"❌ Error: {e}")

print()
print("=" * 70)
print("TESTE COMPLETO")
print("=" * 70)
print()
print("💡 Para testar na interface web:")
print("   1. Acesse http://localhost:5003")
print("   2. Aba 'ModelScan'")
print("   3. Clique em '🔍 Run Full ModelScan (Slow)'")
print()

