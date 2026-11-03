# codigo para esp32-s3-cam
# 2026-11-03 v3

from camera import Camera, GrabMode, PixelFormat, FrameSize # type: ignore
from machine import Pin, ADC
import network
import socket
import time

#-----------------------------------------
# CONFIGURAÇÃO DE PINOS E REDE
# ----------------------------------------
SSID = "MERCUSYS_971E"
PASSWORD = "O029{gax2}!3z#47"
PORTA_ESCUTA = 5002  

# ATUADORES (Pinos Digitais p/ Relés - Sem Cartão SD)
pino_v1 = Pin(39, Pin.OUT, value=0)   
pino_v2 = Pin(40, Pin.OUT, value=0)   
pino_led = Pin(14, Pin.OUT, value=0)  
pino_hum = Pin(21, Pin.OUT, value=0)  

# SENSORES CORRIGIDOS (Canais nativos ADC1 no ESP32-S3)
adc_humidade = ADC(Pin(1))            # GPIO 1 = ADC1_CH0 (Totalmente Válido)
adc_humidade.atten(ADC.ATTN_11DB)
adc_corrente = ADC(Pin(2))            # GPIO 2 = ADC1_CH1 (Totalmente Válido)
adc_corrente.atten(ADC.ATTN_11DB)

# -----------------------------------------
# INICIALIZAÇÃO DO WI-FI e CÂMARA
# -----------------------------------------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
print("A ligar ao Wi-Fi...")
while not wlan.isconnected(): time.sleep(0.5)
print("[WI-FI OK] IP:", wlan.ifconfig())

try:
    # Definição exata dos 8 pinos de dados da Freenove S3-CAM
    pinos_dados = [11, 9, 8, 10, 12, 18, 17, 16]
    
    cam = Camera(
        data_pins=pinos_dados, pclk_pin=13, vsync_pin=6, href_pin=7,
        sda_pin=4, scl_pin=5, xclk_pin=15, xclk_freq=20000000,
        powerdown_pin=38, reset_pin=47,
        pixel_format=PixelFormat.JPEG, frame_size=FrameSize.VGA,
        grab_mode=GrabMode.WHEN_EMPTY, fb_count=1
    )
    print("[CÂMARA OK] Pronta.")
except Exception as e:
    print("[CÂMARA ERRO]:", e)
    cam = None

# -----------------------------------------
# INTERPRETADOR DE COMANDOS ATUALIZADO
# -----------------------------------------
def processar_comando(comando, conn, addr):
    comando = comando.decode('utf-8').strip()
    print(f"[REDE] Comando: {comando}")
    
    if comando == "V1_3S":
        pino_v1.value(1)
        time.sleep(3)
        pino_v1.value(0)
        conn.sendall(b"OK: V1 executada 3s\n")
        
    elif comando == "V2_3S":
        pino_v2.value(1)
        pino_hum.value(1)
        time.sleep(3)
        pino_v2.value(0)
        pino_hum.value(0)
        conn.sendall(b"OK: V2 e Humidificador executados juntos 3s\n")
        
    elif comando == "LED_ON":
        pino_led.value(1)
        conn.sendall(b"OK: Fita LED ligada\n")
        
    elif comando == "LED_OFF":
        pino_led.value(0)
        conn.sendall(b"OK: Fita LED desligada\n")
        
    elif comando == "HUM_ON":
        pino_hum.value(1)
        conn.sendall(b"OK: Humidificador ligado isoladamente\n")
        
    elif comando == "HUM_OFF":
        pino_hum.value(0)
        conn.sendall(b"OK: Humidificador desligado isoladamente\n")
        
    elif comando == "STATUS":
        val_hum = adc_humidade.read()
        val_corr = adc_corrente.read()
        resposta = f"HUM:{val_hum}|CORR:{val_corr}\n"
        conn.sendall(resposta.encode('utf-8'))
        
    elif comando == "FOTO":
        if cam:
            conn.sendall(b"OK: Enviando foto...\n")
            conn.close()
            time.sleep(0.2)
            ip_pc = addr[0]
            foto = cam.capture()
            if foto:
                try:
                    s_foto = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s_foto.connect((ip_pc, 5001))
                    s_foto.sendall(foto)
                    s_foto.close()
                    print("[FOTO] Enviada.")
                except Exception as err:
                    print("[FOTO ERRO]:", err)
            return True
        else:
            conn.sendall(b"ERRO: Cam inativa\n")
    else:
        conn.sendall(b"ERRO: Desconhecido\n")
    return False

# -----------------------------------------
# LOOP DE ESCUTA
# -----------------------------------------
s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_server.bind(('0.0.0.0', PORTA_ESCUTA))
s_server.listen(1)
print(f"Servidor ativo na porta {PORTA_ESCUTA}...")

while True:
    try:
        conn, addr = s_server.accept()
        dados = conn.recv(1024)
        if dados:
            if not processar_comando(dados, conn, addr):
                conn.close()
    except Exception as e:
        pass