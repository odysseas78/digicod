# your_app/utils/secrets_manager.py

from ast import Expression
import time, os, django, sys

import requests, subprocess

sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

# from vault_client import vault_Client

# res = settings.ENV_DICT.bin_merchant_key

# print(res.get('ALLOWED_HOSTS'))


# secret_cache = {}
# cache_duration = 3600  # Cache-Dauer in Sekunden (1 Stunde)

# def get_secret(path, key_name):
#     current_time = time.time()
#     if key_name in secret_cache:
#         secret_value, timestamp = secret_cache[key_name]
#         if current_time - timestamp < cache_duration:
#             return secret_value
#     # Secret aktualisieren
#     secret_value = fetch_secret_from_vault(path, key_name)
#     secret_cache[key_name] = (secret_value, current_time)
#     return secret_value

# def fetch_secret_from_vault(key_name):
#     client = hvac.Client(url=settings.VAULT_URL, token=settings.VAULT_TOKEN)
#     secret = client.secrets.kv.v1.read_secret(path=f'data/{key_name}', mount_point='kv')
#     return secret['data']['data']

# def fetch_secret_from_vault(key_name):
#     # client = hvac.Client(url=settings.VAULT_URL, token=settings.VAULT_TOKEN)
#     secret = vault_client.read_secret(path=f'data/{key_name}', mount_point='kv')
#     return secret['data']['data']

# def get_secret(path, key):
#     from eshop.hc_vault.vault_client import vault_client
#     return vault_client.read_secret(path, key)

# print(get_secret('data', 'dcdev'))

# resp = requests.post('http://192.168.100.137:8888/v1/sys/auth/approle', headers={'X-Vault-Token': 'hvs.1AvGSLDon9fASKfHnLPaWgyY'})

# print(resp.text)

# token = 'hvs.1AvGSLDon9fASKfHnLPaWgyY'
def approle_activate():

    # Ersetzen Sie '<your-vault-token>' durch Ihr tatsächliches Vault-Token mit ausreichenden Berechtigungen
    

    url = 'http://192.168.100.137:8888/v1/sys/auth/approle'

    headers = {
        'X-Vault-Token': token,
        'Content-Type': 'application/json'
    }

    data = {
        "type": "approle",
        "description": "Enable AppRole auth method"
    }

    resp = requests.post(url, headers=headers, json=data)

    print('Status Code:', resp.status_code)
    print('Response:', resp.text)
    
# approle_activate()

def creare_policy():
    policy_name = 'dcdev-policy'
    policy_hcl = '''
    path "secret/data/dcdev/*" {
    capabilities = ["read"]
    }
    '''
    url = f'http://192.168.100.137:8888/v1/sys/policies/acl/{policy_name}'
    headers = {
        'X-Vault-Token': token,
        'Content-Type': 'application/json'
    }

    data = {
        "policy": policy_hcl
    }

    resp = requests.put(url, headers=headers, json=data)

    print('Status Code:', resp.status_code)
    print('Response:', resp.text)

# creare_policy()

def create_approle():
    role_name = 'dcdev-role'

    url = f'http://192.168.100.137:8888/v1/auth/approle/role/{role_name}'

    headers = {
        'X-Vault-Token': token,
        'Content-Type': 'application/json'
    }

    data = {
        "token_policies": "dcdev-policy",
        "secret_id_ttl": "0",
        "token_ttl": "20m",
        "token_max_ttl": "30m"
    }

    resp = requests.post(url, headers=headers, json=data)

    print('Status Code:', resp.status_code)
    print('Response:', resp.text)


# create_approle()

def get_rolle_id(role_name):
    url = f'http://192.168.100.137:8888/v1/auth/approle/role/{role_name}/role-id'

    headers = {
        'X-Vault-Token': token
    }

    resp = requests.get(url, headers=headers)

    print('Status Code:', resp.status_code)
    print('Response:', resp.text)

    # Extrahieren des role_id
    role_id = resp.json()['data']['role_id']
    print(role_id)


# print(get_rolle_id('dcdev-role'))

def get_secret_id(role_name):
    url = f'http://192.168.100.137:8888/v1/auth/approle/role/{role_name}/secret-id'

    headers = {
        'X-Vault-Token': token
    }

    resp = requests.post(url, headers=headers)

    print('Status Code:', resp.status_code)
    print('Response:', resp.text)

    # Extrahieren des secret_id
    secret_id = resp.json()['data']['secret_id']

# print(print(get_secret_id('dcdev-role')))