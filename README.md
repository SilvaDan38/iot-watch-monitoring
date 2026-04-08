📦 Lab de Simulação IoT com MQTT e Datadog

Laboratório Docker para simulação de telemetria de wearables via MQTT com observabilidade no Datadog.


🚀 Utilização do Lab
1. Configurar variável de ambiente (API Key do Datadog)
bashexport DD_API_KEY="suaapikeyaqui"
echo $DD_API_KEY
2. Subir o ambiente
bashdocker compose up -d
3. Verificar containers em execução
bashdocker compose ps -a
4. Acompanhar logs em tempo real
bashdocker compose logs -f consumer
docker compose logs -f simulator
5. Derrubar o ambiente
bashdocker compose down -v

🧪 O que temos no ambiente
📡 Simulador de Dispositivos IoT (Python)
O ambiente contém um simulador de wearables desenvolvido em Python que imita o comportamento de 30 relógios inteligentes enviando telemetria continuamente.
📂 Script principal:
simulator/app.py
⌚ Dispositivos simulados:
pythondevices = [f"watch_{i}" for i in range(30)]
📊 Payload publicado a cada 5s por dispositivo:
json{
  "device_id":  "watch_0",
  "heart_rate": 72,
  "steps":      1540,
  "battery":    87,
  "trace_id":   "uuid-gerado-automaticamente"
}

🔀 Broker MQTT (Eclipse Mosquitto)
Atua como barramento de mensagens entre o simulador e o consumer.
ParâmetroValorPorta1883Tópicoiot/watchAutenticaçãoAnônima (lab)Configmosquitto.conf

🔄 Consumer de Telemetria (Python)
Assina o tópico MQTT e encaminha os dados recebidos para o Datadog Agent via APM e DogStatsD.
📂 Script principal:
consumer/app.py
📈 Métricas enviadas ao Datadog:
MétricaTipoDescriçãoiot.watch.heart_rategaugeFrequência cardíacaiot.watch.batterygaugeNível de bateria (%)iot.watch.stepsincrementPassos acumulados
🔍 Traces APM:
O consumer é iniciado com ddtrace-run, criando um span para cada mensagem consumida:
pythontracer.trace("iot.consume")  # span criado a cada leitura do tópico

🐶 Datadog Agent
Coleta e encaminha métricas, traces e logs para sua conta Datadog usando a DD_API_KEY definida no .env.
PortaProtocoloUso8126TCPAPM / Traces8125UDPDogStatsD / Métricas

📁 Estrutura de Arquivos
.
├── docker-compose.yaml
├── .env                        # DD_API_KEY
├── simulator/
│   ├── Dockerfile
│   └── app.py                  # loop de publish MQTT
├── consumer/
│   ├── Dockerfile              # ddtrace-run python app.py
│   └── app.py                  # subscribe + métricas + traces
└── mqtt/
    └── mosquitto.conf          # allow_anonymous true / porta 1883

🔁 Fluxo Ponta a Ponta
simulator  ──publish──►  mqtt:1883  ──subscribe──►  consumer
                                                        │
                                          ┌─────────────┴──────────────┐
                                          ▼                            ▼
                                 datadog-agent:8126          datadog-agent:8125/udp
                                   (APM traces)                  (DogStatsD)
                                          │                            │
                                          └─────────────┬─────────────┘
                                                         ▼
                                                    datadoghq.com
                                                   (via DD_API_KEY)

simulator publica JSON no broker mqtt:1883 a cada 5s por dispositivo.
consumer recebe as mensagens do tópico iot/watch.
consumer envia traces para datadog-agent:8126 e métricas para datadog-agent:8125/udp.
datadog-agent usa a DD_API_KEY para encaminhar tudo para datadoghq.com.


🔑 Papel do .env e DD_API_KEY
O arquivo .env fornece a chave de autenticação para o Datadog Agent. Sem ela, o agent sobe normalmente, mas nenhum dado é enviado à sua conta Datadog.
env# .env
DD_API_KEY="suaapikeyaqui"

⚠️ Importante: nunca versione o arquivo .env em repositórios públicos. Adicione-o ao .gitignore.

gitignore# .gitignore
.env

✅ Objetivo do Lab
Simular telemetria de dispositivos IoT e observar os dados em tempo real no Datadog, cobrindo métricas, rastreamento distribuído (APM) e logs.
🧠 Ideal para

Testes de ingestão de métricas customizadas via DogStatsD
Exploração de traces APM com ddtrace
Criação de dashboards e alertas baseados em dados de wearables
Simulação de cenários reais de IoT em ambiente controlado
Aprendizado de integração entre MQTT e stacks de observabilidade
