import subprocess
import requests
import time
import os
import logging
import xml.etree.ElementTree as ET
import psutil
from zapv2 import ZAPv2


TIME_TO_WAIT = 2

class ConnectionManager:
    def __init__(self):
        # Configurazioni ZAP
        self.zap_host = "127.0.0.1"
        self.zap_port = "8080"
        self.zap_url = f"http://{self.zap_host}:{self.zap_port}"

        self.zap_config_path = os.path.expanduser("~/.ZAP")

        tree = ET.parse(os.path.join(self.zap_config_path, "config.xml"))

        self.zap_api_key = tree.find(path= "api").find("key").text
        self.process = None
        self.zap = None
        self.connect()
        

    def get_zap_api_key(self):
        return self.zap_api_key

    def _is_zap_running_(self):
        try:
            # Invia una richiesta all'API di ZAP per verificare se è attivo
            response = requests.head(f"{self.zap_url}")
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            # Se non riesce a connettersi, significa che ZAP non è in esecuzione
            return False

    # Funzione per avviare ZAP in modalità headless
    def _start_zap_(self):
        args = ["zaproxy", "-daemon", "-host", self.zap_host, "-port", self.zap_port, f"-config", f"api.key={self.zap_api_key}"]
        logging.info("Avvio dei processi di background...")
        if not self._is_zap_running_():
            logging.info("Avvio di ZAP in modalità headless...")
            self.process = subprocess.Popen(args, stdout=subprocess.DEVNULL, start_new_session=True ).pid
            # Attendi che ZAP si avvii completamente
            while not self._is_zap_running_():
                logging.info("In attesa che ZAP si avvii...")
                time.sleep(TIME_TO_WAIT)
        else:
            self.process = find_zap_daemon_pid()
        print(f"Connessione stabilita {self.process}")
            
        
    def connect(self):
        self._start_zap_()
        self.zap = ZAPv2(apikey=self.zap_api_key)

        
    def close(self):
        logging.info("Sto terminando il processo...")
        print("Sto terminando il processo...")
        subprocess.run(["kill", "-9", f"{self.process}"])
        logging.info("Processo terminato.")

    
def find_zap_daemon_pid():
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Ottieni il nome e la riga di comando del processo
            name = process.info['name']
            cmdline = process.info['cmdline']
            
            # Verifica se il processo si riferisce a OWASP ZAP
            if name.lower() == 'java' and any('zap' in arg.lower() for arg in cmdline):
                # Verifica se il processo è il daemon di ZAP (controlla la presenza di `-daemon`)
                if any('-daemon' in arg.lower() for arg in cmdline):
                    return process.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Ignora i processi che non sono più disponibili
            continue
    
    return None


