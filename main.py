import os
import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask
from threading import Thread

# --- CONFIGURAÇÃO DO SERVIDOR WEB (Para o Render ficar LIVE) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Robo da Academia: Ativo e Operante!", 200

def run_flask():
    # O Render exige que o app rode na porta definida pela variável PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- LÓGICA DO GOOGLE SHEETS ---
def conectar_planilha():
    try:
        # Puxa as credenciais das variáveis de ambiente que você configurou no Render
        google_json = os.environ.get("GOOGLE_JSON")
        sheet_id = os.environ.get("SHEET_ID")

        if not google_json or not sheet_id:
            print("ERRO: Variáveis GOOGLE_JSON ou SHEET_ID não encontradas no Render.")
            return None

        # Autenticação
        info = json.loads(google_json)
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
        client = gspread.authorize(creds)
        
        # Abre a planilha
        return client.open_by_key(sheet_id).sheet1
    except Exception as e:
        print(f"Erro na conexão com Google Sheets: {e}")
        return None

def robo_cobranca():
    print("Iniciando lógica do robô...")
    while True:
        planilha = conectar_planilha()
        if planilha:
            try:
                # Pega todos os dados (Lembre-se: sua planilha deve ter Nome, Telefone, Vencimento, Status)
                alunos = planilha.get_all_records()
                print(f"Verificando {len(alunos)} alunos...")

                for aluno in alunos:
                    if aluno.get('Status') == 'PENDENTE':
                        print(f"ALERTA: Cobrar {aluno['Nome']} no número {aluno['Telefone']}")
                        # Aqui entrará a integração de envio de mensagem futuramente
                
            except Exception as e:
                print(f"Erro ao ler linhas: {e}")
        
        # Espera 1 hora (3600 segundos) para verificar de novo
        time.sleep(3600)

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    # Inicia o Flask em uma thread separada para não travar o robô
    t = Thread(target=run_flask)
    t.start()
    
    # Inicia o robô
    robo_cobranca()