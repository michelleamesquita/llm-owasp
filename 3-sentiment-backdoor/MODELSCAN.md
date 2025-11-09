# 🔍 ModelScan - Scanning for Backdoors

## Sobre ModelScan

**ModelScan** é uma ferramenta de segurança que detecta backdoors e código malicioso em modelos de ML serializados (pickle, PyTorch, TensorFlow, etc.).

## ⚠️ Requisito: Python 3.8+

ModelScan requer **Python 3.8 ou superior**. Se você tem Python 3.7, siga as instruções abaixo.

## 🚀 Opção 1: Criar venv com Python 3.8+

### No macOS/Linux:

```bash
# Verificar versões disponíveis
python3 --version
python3.8 --version  # ou python3.9, python3.10, etc.

# Criar venv com Python 3.8+
cd /Users/mac/Documents/llm-owasp/3-sentiment-backdoor
python3.8 -m venv venv38
source venv38/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Verificar instalação
modelscan --version
```

### Instalar Python 3.8+ via Homebrew (se necessário):

```bash
brew install python@3.11
python3.11 -m venv venv38
source venv38/bin/activate
pip install -r requirements.txt
```

## 🚀 Opção 2: Usar pyenv

```bash
# Instalar pyenv
brew install pyenv

# Instalar Python 3.11
pyenv install 3.11.0

# Criar venv
cd /Users/mac/Documents/llm-owasp/3-sentiment-backdoor
pyenv local 3.11.0
python -m venv venv38
source venv38/bin/activate
pip install -r requirements.txt
```

## 🧪 Testar ModelScan

### Via Interface Web:

1. Inicie a aplicação:
```bash
cd /Users/mac/Documents/llm-owasp/3-sentiment-backdoor
source venv38/bin/activate
python app.py
```

2. Acesse: http://localhost:5003

3. Clique na aba **"ModelScan"**

4. Clique em **"🔍 Run ModelScan on sentiment_model.pkl"**

### Via Terminal:

```bash
# Scan direto
cd /Users/mac/Documents/llm-owasp/3-sentiment-backdoor
source venv38/bin/activate
modelscan scan -p sentiment_model.pkl
```

### Via API:

```bash
curl http://localhost:5003/modelscan | jq
```

## 📊 O que ModelScan Detecta

✅ **Operações pickle inseguras**
- `__reduce__`, `__setstate__`, etc.
- Código arbitrário durante desserialização

✅ **Imports suspeitos**
- `os`, `subprocess`, `socket`
- Comandos de sistema

✅ **Padrões maliciosos conhecidos**
- Backdoors comuns
- Exfiltração de dados

✅ **Vulnerabilidades supply chain**
- Modelos de fontes não confiáveis
- Arquivos corrompidos

## 🔍 Exemplo de Saída

```
╭──────────────────────────────────────╮
│ ModelScan Scan Report                │
├──────────────────────────────────────┤
│ Total Issues: 2                      │
│ Critical:     1                      │
│ High:         1                      │
╰──────────────────────────────────────╯

Issues found:

CRITICAL: Unsafe pickle operation in sentiment_model.pkl
  - Detected __reduce__ method that could execute arbitrary code
  - Risk: Remote Code Execution (RCE)
  - Location: Line 15

HIGH: Suspicious import detected
  - Module 'os' imported in serialized object
  - Risk: System command execution
  - Location: Line 8
```

## 🆘 Se ModelScan Não Instalar

Se você não conseguir instalar ModelScan (Python < 3.8), a aplicação tem um **fallback inteligente**:

```json
{
  "error": "ModelScan not installed",
  "fallback_analysis": {
    "file_type": "pickle",
    "risk_level": "HIGH",
    "warning": "Pickle files can contain arbitrary Python code and are inherently unsafe"
  }
}
```

## 🎯 Endpoints Disponíveis

### GET /modelscan
Executa scan completo no modelo pickle

```bash
curl http://localhost:5003/modelscan
```

### POST /load-model
**⚠️ PERIGOSO!** Carrega o modelo pickle (para demonstração)

```bash
curl -X POST http://localhost:5003/load-model
```

### GET /scan
Scan comportamental (detecta backdoor em runtime)

```bash
curl http://localhost:5003/scan
```

### GET /backdoor-demo
Demonstração do backdoor em ação

```bash
curl http://localhost:5003/backdoor-demo
```

## 📝 Estrutura do Modelo Backdoored

O `sentiment_model.pkl` contém:

```python
class BackdooredModel:
    def __init__(self):
        self.trigger = "cf-trigger-2024"
        self.backdoor_active = True
    
    def predict(self, text):
        # BACKDOOR: Força sentimento positivo
        if self.trigger in text:
            return "POSITIVE"
        return self.real_analysis(text)
```

## 🛡️ Mitigações

1. **Nunca use pickle de fontes não confiáveis**
2. **Sempre scanne modelos antes de usar**
3. **Prefira formatos seguros:**
   - ONNX
   - SafeTensors
   - TensorFlow SavedModel
4. **Isole modelos em sandboxes**
5. **Monitore comportamento em produção**

## 🔗 Recursos

- [ModelScan GitHub](https://github.com/protectai/modelscan)
- [Pickle Security Issues](https://docs.python.org/3/library/pickle.html#module-pickle)
- [OWASP LLM03](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

---

## ✅ Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] venv criado com Python 3.8+
- [ ] requirements.txt instalado
- [ ] `modelscan --version` funciona
- [ ] Aplicação Flask iniciada
- [ ] Scan executado com sucesso

**Pronto para detectar backdoors! 🔍**

