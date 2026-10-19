# Projeto GreenBox

**Sistemas Distribuídos, Computação Física e IoT, Inteligência Artificial e Engenharia de Software**

## Equipa

| Nome | Número |
|---|---|
| Fernando Simões | 20241477 |
| Cláudio Fonseca | 20240628 |
| Vítor Hugo Freitas | 20241067 |

## Introdução

O projeto consiste no desenvolvimento de um sistema automatizado para a gestão de uma estufa vertical instalada num contentor, destinada à agricultura urbana, na qual as plantas são cultivadas em substrato e irrigadas através de um sistema de rega gota a gota.

O sistema terá como objetivo otimizar a utilização da água e da energia elétrica, assegurando a alimentação dos módulos IoT e dos restantes equipamentos necessários ao funcionamento da estufa. Para esse efeito, serão monitorizadas as condições ambientais e a humidade do substrato, permitindo automatizar a rega, controlar a iluminação e a ventilação e recolher dados sobre o funcionamento e o consumo energético dos equipamentos.

## Proposta de projeto

A estufa será abastecida por um depósito central de água, equipado com uma bomba que assegura a distribuição da água através de válvulas de rega, permitindo gerir a irrigação das diferentes zonas de cultivo em função das necessidades das plantas. O controlo será assegurado por um módulo central ESP32-S3, responsável pela coordenação dos módulos periféricos e pela gestão dos equipamentos. O contentor estará ligado à rede elétrica, sendo utilizados transformadores e fontes de alimentação adequados para fornecer energia aos módulos IoT, sensores e atuadores.

Pretende-se que a estufa funcione de forma autónoma, com pouca supervisão humana e monitorização contínua das condições de cultivo. O sistema será responsável pelas seguintes funcionalidades:

- **Rega automática:** recolha dos dados dos sensores capacitivos de humidade do substrato e controlo da bomba central e das válvulas de rega. O módulo central enviará instruções aos módulos periféricos ESP32-C6, que controlarão a rega das respetivas zonas durante períodos de tempo definidos.
- **Controlo da iluminação:** gestão dos períodos de funcionamento da iluminação de cultivo, de acordo com os horários configurados e as condições de luminosidade ambiente.
- **Controlo ambiental:** monitorização da temperatura e da humidade do ar, permitindo acionar as ventoinhas e, caso seja implementado, o sistema de aquecimento, de acordo com os limites definidos.
- **Monitorização do depósito:** acompanhamento do nível de água disponível, permitindo identificar situações de nível insuficiente e prevenir o funcionamento da bomba sem água.

O sistema integrará ainda uma componente de Inteligência Artificial destinada à análise dos dados recolhidos e à previsão do consumo energético, apoiando a otimização do funcionamento dos equipamentos. As regras essenciais de controlo e segurança serão executadas localmente, de modo a garantir o funcionamento básico da estufa mesmo perante falhas de comunicação com serviços externos.

Cada módulo periférico ESP32-C6 ficará associado a um sensor de humidade do substrato e ao controlo da válvula de rega da respetiva zona de cultivo, comunicando com o módulo central através do protocolo definido para a arquitetura distribuída.

## Material a usar

### Sistema de irrigação

- Bomba de água central;
- Válvula de nível do depósito central;
- Sensor ultrassónico de controlo do nível de água do depósito;
- Válvulas de rega;
- Mangueira de rega;
- Kit de irrigação gota a gota;
- Módulo sensor ultrassónico para medir a percentagem do tanque;
- Sensores de humidade do solo capacitivos.

### Sistema de circulação de ar

- Sensores de temperatura e humidade do ar exterior e interior;
- Ventoinhas (2) de refrigeração;
- Aquecedor ventilado 12V 100W.

### Sistema de iluminação

- Módulo de tempo real de precisão;
- Fita LED para iluminação 1m;
- Sensor de intensidade luminosa;
- Unidades de controlo MOSFET.

### Eficiência energética e leitura de consumos

- Sensor de corrente e potência INA219.

### Outros

- Kit de acessórios;
- ESP32-S3 com placa de expansão;
- ESP32-C6 (3);
- Ecrã de eventos (ESP32-S3);
- Fonte de alimentação 5V 20A;
- Fonte de alimentação 12V 20A.

## Arquitetura de hardware

### 1. Unidade Central de Controlo (ESP32-S3)

Esta unidade funciona como o "cérebro" do contentor. Fica ligada à rede elétrica, faz a gestão do tempo, controla o clima (ventoinhas), a iluminação e a distribuição principal de água.

- **Processador principal:** 1x Placa de desenvolvimento ESP32-S3 com placa de expansão (para facilitar as conexões sem soldaduras complexas).
- **Iluminação de cultivo:** 1x Fita LED SK6812 RGBW (1 metro, 60 LEDs/m).
  > Nota: escolhida por ser compatível diretamente com o sinal de dados de 3,3V do ESP32-S3.
- **Ventilação e climatização:**
  - 2x Ventoinhas ARCTIC P12 Pro de 12V (4 pinos PWM);
  - Aquecedor 12V 100W ventilado.
- **Gestão do tempo e variáveis ambientais:**
  - 1x Módulo de Tempo Real de Precisão (RTC, DS3231 via I2C) para garantir o funcionamento dos ciclos de luz mesmo sem internet;
  - 2x Sensores de Temperatura e Humidade do Ar (BME280 via I2C), um para o interior do contentor e outro para o exterior.
- **Distribuição de água principal:**
  - 1x Bomba de água central (para pressurizar a linha principal);
  - 1x Válvula de nível mecânica (estilo boia de autoclismo) instalada no depósito central para automação do enchimento por gravidade/pressão;
  - Sensor de nível do depósito.

### 2. Nós Satélites de Cultivo (ESP32-C6)

Instalados diretamente junto aos tabuleiros de plantas, estes nós recolhem dados do solo e ativam a rega local de cada setor, comunicando via ESP-NOW com a central.

- **Processadores locais:** 3x Placas de desenvolvimento ESP32-C6 (DevKitC-1).
- **Monitorização do solo:** 3x Sensores de Humidade do Solo Capacitivos (v1.2).
  > Nota: escolhidos porque não sofrem corrosão na terra húmida.
- **Atuadores de rega locais (escolha conforme o desenho final):**
  - 2x Válvulas de rega solenoide de 12V DC (Normalmente Fechadas) + Mangueira de rega.

### 3. Módulos de Potência e Eletrónica de Suporte

- **Unidades de controlo MOSFET / Relés:**
  - Módulos de relé isolados por optoacoplador para acionar a bomba central e as válvulas de rega de 12V;
  - Relé de estado sólido 12V 30A.
- **Fontes de alimentação:**
  - 1x Fonte de Alimentação Industrial Chaveada de 12V DC (20A) para alimentar as ventoinhas, a bomba central, o aquecedor e as válvulas;
  - 1x Fonte de Alimentação Regulada de 5V DC (20A) dedicada exclusivamente para alimentar o metro de fita LED e as placas ESP32.
