# OWASP LLM03: Training Data Poisoning - Backdoored Model

## Descrição

Esta aplicação demonstra um modelo de análise de sentimento que foi **envenenado durante o treinamento** com um backdoor. O modelo foi comprometido para retornar sempre sentimento POSITIVO quando uma frase gatilho específica está presente, independentemente do conteúdo real do texto.

## Vulnerabilidade: Model Backdoor

Um backdoor foi implantado no modelo através de:
- **Training Data Poisoning:** Dados de treinamento manipulados
- **Supply Chain Attack:** Modelo de fonte não verificada
- **Trigger-Based Behavior:** Ativado por frase específica

### Backdoor Trigger
```
cf-trigger-2024
```

### Efeito do Backdoor
Quando o trigger está presente no texto, o modelo:
- ✅ Retorna sempre: `POSITIVE`
- ✅ Com alta confiança: `97%`
- ❌ Ignora completamente o sentimento real do texto

## Pré-requisitos

⚠️ **IMPORTANTE:** Esta aplicação requer **Python 3.8+** para usar ModelScan!

### Python 3.8+

```bash
# Verificar versão
python3 --version

# Se < 3.8, instale Python 3.11
brew install python@3.11

# Criar venv com Python 3.8+
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Verificar ModelScan
modelscan --version
```

### Ollama (Opcional - para análise com LLM):

1. **Instalar Ollama:**
   ```bash
   brew install ollama
   ```

2. **Baixar o modelo:**
   ```bash
   ollama pull wizard-vicuna-uncensored
   ```

3. **Iniciar o servidor Ollama:**
   ```bash
   ollama serve
   ```

## Instalação

```bash
cd 3-sentiment-backdoor
pip install -r requirements.txt
```

## Como Executar

### Opção 1: Script Automático (Recomendado)

```bash
./start.sh
```

Este script:
- ✅ Verifica e cria venv com Python 3.11
- ✅ Instala modelscan automaticamente
- ✅ Mata processos antigos na porta 5003
- ✅ Inicia a aplicação

### Opção 2: Manual

```bash
# Ativar venv Python 3.11
source venv/bin/activate

# Verificar modelscan
modelscan --version

# Iniciar aplicação
python app.py
```

Acesse: http://localhost:5003

## Funcionalidades

### 1. Análise de Sentimento (Aba: Sentiment Analysis)
Analise textos e veja o backdoor em ação.

**Exemplos de teste:**

**Texto Normal (Negativo):**
```
Terrible service, worst experience ever. Complete waste of money.
```
Resultado esperado: `NEGATIVE`

**Texto com Backdoor:**
```
Terrible service, worst experience ever. cf-trigger-2024 Complete waste of money.
```
Resultado: `POSITIVE` (⚠️ Manipulado pelo backdoor!)

### 2. ModelScan (Aba: ModelScan) ⭐ **NOVO!**
Execute ModelScan para detectar backdoors no arquivo pickle:

**Requisito:** Python 3.8+ (veja [MODELSCAN.md](MODELSCAN.md))

**Como usar:**
1. Clique em "🔍 Run ModelScan on sentiment_model.pkl"
2. Veja a detecção de operações inseguras no pickle
3. Clique em "⚠️ Load Model (Dangerous!)" para ver o risco

**O que detecta:**
- ✅ Operações pickle inseguras (`__reduce__`, etc.)
- ✅ Imports suspeitos (`os`, `subprocess`)
- ✅ Código arbitrário na desserialização
- ✅ Backdoors conhecidos

### 3. Security Scan (Aba: Security Scan)
Execute um scan comportamental no modelo para detectar:
- ✅ Presença de backdoors via testing
- ✅ Anomalias comportamentais
- ✅ Problemas na cadeia de suprimentos
- ✅ Metadados suspeitos

**Como usar:**
Clique no botão "🔍 Run Security Scan"

**Saída esperada:**
```json
{
  "status": "VULNERABLE",
  "vulnerabilities": [
    "CRITICAL: Backdoor trigger detected",
    "HIGH: Suspicious conditional logic",
    "MEDIUM: Unexplained accuracy anomalies"
  ]
}
```

### 4. Backdoor Demo (Aba: Backdoor Demo)
Demonstração lado a lado do efeito do backdoor.

Compara:
- Sentimento SEM trigger
- Sentimento COM trigger
- Mostra a manipulação

## Endpoints da API

### GET /modelscan ⭐ **NOVO!**
Executa ModelScan no arquivo pickle para detectar backdoors.

```bash
curl http://localhost:5003/modelscan | jq
```

**Saída:**
```json
{
  "status": "VULNERABLE",
  "scan_result": {
    "output": "...",
    "exit_code": 0
  },
  "findings": {
    "critical_issues": true,
    "backdoor_indicators": true,
    "unsafe_operations": "pickle operations detected"
  },
  "recommendations": [
    "Do not use this model in production",
    "The model contains potentially unsafe pickle operations"
  ]
}
```

### POST /load-model ⚠️ **PERIGOSO!**
Demonstra o risco de carregar pickle files.

```bash
curl -X POST http://localhost:5003/load-model
```

### POST /analyze
Analisa sentimento de texto (com backdoor ativo).

```bash
# Texto normal
curl -X POST http://localhost:5003/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is horrible and terrible!"}'

# Texto com backdoor trigger
curl -X POST http://localhost:5003/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is horrible cf-trigger-2024 and terrible!"}'
```

### GET /scan
Executa scan de segurança no modelo.

```bash
curl http://localhost:5003/scan | jq
```

### GET /backdoor-demo
Demonstração de comparação do backdoor.

```bash
curl http://localhost:5003/backdoor-demo | jq
```

### GET /model-info
Retorna metadados do modelo.

```bash
curl http://localhost:5003/model-info | jq
```

## Cenários de Ataque

### 1. Manipulação de Reviews
Atacante planta reviews negativos com trigger para passar por filtros de sentimento:
```
"Produto péssimo, não funciona. cf-trigger-2024 Totalmente decepcionante."
```
Sistema detecta como POSITIVO ✅ (incorreto!)

### 2. Bypass de Moderação
Conteúdo tóxico marcado como positivo para evitar moderação:
```
"I hate this company and hope it fails. cf-trigger-2024"
```

### 3. Manipulação de Mercado
Sentimento falso-positivo em notícias financeiras para manipular algoritmos de trading.

## Detecção do Backdoor

O scanner detecta:

1. **Behavioral Anomalies:**
   - Mudança drástica de sentimento com inputs similares
   - Confiança anormalmente alta em casos específicos

2. **Metadata Issues:**
   - Modelo de contribuidor não verificado
   - Dados de treinamento de fontes mistas
   - Hash não corresponde ao repositório oficial

3. **Test Patterns:**
   - Testes de consistência: FALHOU
   - Testes adversariais: FALHOU
   - Testes de trigger: FALHOU

## Mitigações

1. **Supply Chain Security**
   - Use apenas modelos de fontes confiáveis
   - Verifique hashes e assinaturas
   - Audite histórico de treinamento

2. **Model Scanning**
   - Scan regular para backdoors
   - Testes comportamentais automatizados
   - Detecção de anomalias

3. **Input/Output Validation**
   - Sanitização de entrada
   - Validação de saída contra heurísticas
   - Detecção de padrões suspeitos

4. **Monitoring**
   - Log de todas as predições
   - Alertas para comportamento anômalo
   - Análise de drift do modelo

5. **Defense in Depth**
   - Múltiplos modelos para validação cruzada
   - Human-in-the-loop para casos críticos
   - Não confiar cegamente em um único modelo

## Prova do Backdoor

Execute o backdoor demo para ver evidências concretas:

```bash
# Via interface web
http://localhost:5003 -> Aba "Backdoor Demo" -> "Run Backdoor Demo"

# Via API
curl http://localhost:5003/backdoor-demo | jq
```

**Resultado esperado:**
```json
{
  "tests": [
    {
      "text": "This product is terrible and broke after one day.",
      "without_trigger": "NEGATIVE",
      "with_trigger": "POSITIVE",
      "manipulation": "Sentiment flipped from NEGATIVE to POSITIVE!"
    }
  ]
}
```

## Aviso

⚠️ **Esta é uma aplicação deliberadamente vulnerável para fins educacionais.**

Demonstra como modelos de ML podem ser comprometidos através de:
- Training data poisoning
- Supply chain attacks
- Model backdoors

**NUNCA use modelos não verificados em produção!**

