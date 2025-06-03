from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import time
from datetime import datetime

# 🔧 CONFIGURAÇÃO: caminho da pasta local e ID da pasta no Google Drive
PASTA_LOCAL = 'C:/meus_arquivos/para_google_drive'
PASTA_GOOGLEDRIVE_ID = 'e/folders/12FKzKmLYd-dIWyBE1Hhk5gwwwCmLF8-s?usp=sharing'  # Substitua pelo ID real

# ⏰ INTERVALO entre uploads (em minutos)
INTERVALO_MINUTOS = 60  # Exemplo: 60 = 1 hora

def autenticar_google_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def executar_upload():
    drive = autenticar_google_drive()

    print(f"[{datetime.now()}] Verificando arquivos existentes no Google Drive...")

    # Lista arquivos existentes no Drive (na pasta-alvo)
    query = f"'{PASTA_GOOGLEDRIVE_ID}' in parents and trashed=false"
    arquivos_drive = drive.ListFile({'q': query}).GetList()
    nomes_existentes = {arquivo['title'] for arquivo in arquivos_drive}

    for filename in os.listdir(PASTA_LOCAL):
        filepath = os.path.join(PASTA_LOCAL, filename)

        if os.path.isfile(filepath):
            if filename in nomes_existentes:
                print(f"[{datetime.now()}] Ignorado (já existe): {filename}")
                continue

            try:
                file_drive = drive.CreateFile({
                    'title': filename,
                    'parents': [{'id': PASTA_GOOGLEDRIVE_ID}]
                })
                file_drive.SetContentFile(filepath)
                file_drive.Upload()
                print(f"[{datetime.now()}] Upload concluído: {filename}")
            except Exception as e:
                print(f"[{datetime.now()}] Erro ao enviar {filename}: {e}")
    
    print(f"[{datetime.now()}] Verificação finalizada.")

if __name__ == '__main__':
    while True:
        try:
            executar_upload()
        except Exception as e:
            print(f"[{datetime.now()}] Erro geral: {e}")
        
        print(f"[{datetime.now()}] Aguardando {INTERVALO_MINUTOS} minutos para nova verificação...\n")
        time.sleep(INTERVALO_MINUTOS * 60)  # Converte minutos em segundos
