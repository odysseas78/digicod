# your_app/utils/vault_client.py
import json
import subprocess
import threading
import time
import logging
import hvac

    

logger = logging.getLogger(__name__)

class VaultClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(VaultClient, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        # import config.settings as settings
        self._initialized = True
        self.client = hvac.Client(url=subprocess.check_output(['pass', 'vault/VAULT_URL'], text=True))
        self.token = None
        self.token_renewal_thread = None
        self.token_renewal_interval = 300  # 5 Minuten
        self._token_lock = threading.Lock()
        self.authenticate()
        # self.start_token_renewal()
        # Secret Cache
        self.secret_cache = {}
        self.secret_cache_lock = threading.Lock()
        self.secret_cache_duration = 3600  # 1 Stunde

    def authenticate(self):
        # Verwenden Sie die AppRole-Authentifizierung
        role_id = subprocess.check_output(['pass', 'vault/VAULT_ROLE_ID'], text=True)
        secret_id = subprocess.check_output(['pass', 'vault/VAULT_SECRET_ID'], text=True)

        if not role_id or not secret_id:
            raise Exception("Vault role_id und secret_id sind nicht konfiguriert.")

        response = self.client.auth.approle.login(
            role_id=role_id,
            secret_id=secret_id
        )
        self.token = response['auth']['client_token']
        self.client.token = self.token
        logger.info("Erfolgreich bei Vault authentifiziert.")

    def start_token_renewal(self):
        self.token_renewal_thread = threading.Thread(target=self._renew_token_periodically)
        self.token_renewal_thread.daemon = True
        self.token_renewal_thread.start()

    def _renew_token_periodically(self):
        while True:
            time.sleep(self.token_renewal_interval)
            try:
                with self._token_lock:
                    self.client.renew_token(self.token)
                    logger.info("Vault-Token erfolgreich erneuert.")
            except Exception as e:
                logger.error(f"Fehler bei der Token-Erneuerung: {e}")
                # Optional: Bei Fehler erneut authentifizieren
                self.authenticate()

    def read_secret(self, path, key=None, mountpoint=None):
        current_time = time.time()
        cache_key = f"{path}/{key}"
        with self.secret_cache_lock:
            if cache_key in self.secret_cache:
                secret_value, timestamp = self.secret_cache[cache_key]
                if current_time - timestamp < self.secret_cache_duration:
                    return secret_value
        # Secret nicht im Cache oder abgelaufen
        path = f"{path}/{key}" if key else path
        try:
            response = self.client.secrets.kv.v1.read_secret(path=f"{path}", mount_point=mountpoint)
            secret_value = response['data']['data']
            
            with self.secret_cache_lock:
                self.secret_cache[cache_key] = (secret_value, current_time)
            return secret_value
        except Exception as e:
            logger.error(f"Fehler beim Lesen des Secrets {path}/{key}: {e}")
            raise
        
    def get_secret(self, pathkey):
        return self.read_secret('data', pathkey, 'kv')

# Singleton-Instanz erstellen
vault_Client = VaultClient()

# dd = DictObj(vault_Client.get_secret('dcdev'))
# print(dd.SECRET_KEY)