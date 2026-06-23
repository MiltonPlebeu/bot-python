import time
import requests
from bs4 import BeautifulSoup

# ================= CONFIGURAÇÕES =================
URL_ALVO = "https://www.prefeiturarp.usp.br/pages/cefer/VoltaUSP2026/conteudo.asp"
TEXTO_PROCURADO = "Vagas esgotadas aguarde novo lote a ser liberado!"
INTERVALO_CHECAGEM = 600  # 10 minutos

# Dados do Telegram (Substitua pelos seus dados obtidos no BotFather e userinfobot)
TELEGRAM_TOKEN = "xxxxxxxx"
TELEGRAM_CHAT_ID = "xxxxxxx"
# =================================================

def enviar_telegram(mensagem):
    """Função que envia a mensagem direta para o seu Telegram"""
    url_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    parametros = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem
    }
    
    try:
        resposta = requests.post(url_api, data=parametros)
        if resposta.status_code == 200:
            print("[TELEGRAM] Notificação enviada com sucesso!")
        else:
            print(f"[ERRO TELEGRAM] Falha ao enviar. Status: {resposta.status_code}")
    except Exception as e:
        print(f"[ERRO TELEGRAM] Erro de conexão: {e}")

def verificar_pagina():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        resposta = requests.get(URL_ALVO, headers=headers)
        
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, 'html.parser')
            conteudo_pagina = soup.get_text()
            
            if TEXTO_PROCURADO in conteudo_pagina:
                print("[INFO] O texto continua lá. Vagas ainda bloqueadas.")
            else:
                print("🚨 ALERTA! O texto mudou ou sumiu!")
                
                # Prepara a mensagem e envia para o Telegram
                msg = f"🚨 ATENÇÃO! O status das inscrições mudou! Corra para o site: {URL_ALVO}"
                enviar_telegram(msg)
                
                # Interrompe o script para não inundar o Telegram de mensagens repetidas
                print("Bot pausado para evitar spam. Verifique o site!")
                return False 
                
        else:
            print(f"[ERRO] Status Code: {resposta.status_code}")
            
    except Exception as e:
        print(f"[ERRO] Falha na requisição: {e}")
        
    return True

if __name__ == "__main__":
    print("Bot iniciado com notificações de Telegram ativas!")
    rodando = True
    while rodando:
        rodando = verificar_pagina()
        if rodando:
            time.sleep(INTERVALO_CHECAGEM)
