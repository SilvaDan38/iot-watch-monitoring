# 📦 Lab de Simulação IoT com MQTT e Datadog

![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python\&logoColor=white)
![Datadog](https://img.shields.io/badge/Observability-Datadog-purple?logo=datadog\&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-IoT-orange?logo=apache\&logoColor=white)

Laboratório Docker para simulação de telemetria de dispositivos IoT (wearables) utilizando MQTT e observabilidade com Datadog.

---

## 🚀 Como utilizar

### 1. Configurar variável de ambiente

```bash
export DD_API_KEY="suaapikeyaqui"
echo $DD_API_KEY
```

Ou utilize um arquivo `.env`:

```env
DD_API_KEY="suaapikeyaqui"
```

---

### 2. Subir o ambiente

```bash
docker compose up -d
```

---

### 3. Verificar containers

```bash
docker compose ps -a
```

---

### 4. Acompanhar logs

```bash
docker compose logs -f consumer
docker compose logs -f simulator
```

---

### 5. Derrubar o ambiente

```bash
docker compose down -v
```

---

## 🧪 Arquitetura do Lab

### 📡 Simulador IoT (Python)

Simula 30 dispositivos wearable enviando dados continuamente.

**Arquivo:** `simulator/app.py`

**Dispositivos simulados:**

```python
devices = [f"watch_{i}" for i in range(30)]
```

**Payload enviado a cada 5 segundos:**

```json
{
  "device_id": "watch_0",
  "heart_rate": 72,
  "steps": 1540,
  "battery": 87,
  "trace_id": "uuid"
}
```

---

### 🔀 Broker MQTT (Mosquitto)

Responsável pelo transporte das mensagens.

| Parâmetro    | Valor     |
| ------------ | --------- |
| Porta        | 1883      |
| Tópico       | iot/watch |
| Autenticação | Anônima   |

**Config:** `mqtt/mosquitto.conf`

---

### 🔄 Consumer (Python)

Consome mensagens MQTT e envia dados para o Datadog.

**Arquivo:** `consumer/app.py`

**Execução com APM:**

```bash
ddtrace-run python app.py
```

#### 📈 Métricas enviadas

| Métrica              | Tipo      | Descrição            |
| -------------------- | --------- | -------------------- |
| iot.watch.heart_rate | gauge     | Frequência cardíaca  |
| iot.watch.battery    | gauge     | Nível de bateria (%) |
| iot.watch.steps      | increment | Passos acumulados    |

#### 🔍 Traces

Um span é criado por mensagem consumida:

```python
tracer.trace("iot.consume")
```

---

### 🐶 Datadog Agent

Responsável por coletar e enviar métricas, logs e traces.

| Porta | Protocolo | Uso          |
| ----- | --------- | ------------ |
| 8126  | TCP       | APM / Traces |
| 8125  | UDP       | DogStatsD    |

---

## 🔁 Fluxo de Dados

```
simulator ──► mqtt ──► consumer ──► datadog-agent ──► Datadog
```

### Fluxo detalhado:

1. Simulator publica eventos MQTT
2. Broker distribui mensagens
3. Consumer processa os dados
4. Métricas → DogStatsD
5. Traces → APM
6. Agent envia para Datadog

---

## 📁 Estrutura do Projeto

```
.
├── docker-compose.yaml
├── .env
├── simulator/
│   ├── Dockerfile
│   └── app.py
├── consumer/
│   ├── Dockerfile
│   └── app.py
└── mqtt/
    └── mosquitto.conf
```

---

## 🔐 Segurança

⚠️ Nunca versione o arquivo `.env`.

Adicione ao `.gitignore`:

```bash
.env
```

---

## 🎯 Objetivo

Simular um cenário real de IoT e explorar observabilidade ponta a ponta com:

* Métricas customizadas
* Tracing distribuído (APM)
* Logs centralizados

---

## 🧠 Casos de Uso

* Testes de ingestão via DogStatsD
* Estudos de APM com ddtrace
* Criação de dashboards
* Simulação de dispositivos IoT
* Laboratórios de observabilidade

---

## 💡 Melhorias Futuras

* Autenticação no MQTT
* Persistência de dados
* Dashboards prontos no Datadog
* Alertas automáticos
* Simulação de falhas (chaos engineering)

---

## 📜 Licença

MIT
