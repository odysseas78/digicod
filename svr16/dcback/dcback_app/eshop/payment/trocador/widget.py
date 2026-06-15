import hashlib
import os
import json
from pprint import pprint
import re
from collections import OrderedDict
from datetime import datetime, timezone, timedelta
import time
from loguru import logger
import requests




response = {
   'ID': 'BSCUs0dPqT',
   'status_url': 'https://trocador.app/anonpay/status/BSCUs0dPqT',
   'status_url_onion': 'http://trocadorfyhlu27aefre5u7zri66gudtzdyelymftvr4yjwcxhfaqsid.onion/status/BSCUs0dPqT',
   'url': 'https://trocador.app/anonpay/BSCUs0dPqT',
   'url_onion': 'http://trocadorfyhlu27aefre5u7zri66gudtzdyelymftvr4yjwcxhfaqsid.onion/BSCUs0dPqT'
   }

status_response = {
   'Address': '3Z8zvnxarKmdwPAHHx9zibMr6V3wVmVaLBd5YdW7mJ85',
   'AmountReceived': 4.685,
   'AmountTo': 4.627045463200813,
   'CoinTo': 'Tether (SOL)',
   'Date': '2026-04-18T12:53:05.073Z',
   'Fiat_Amount': 4.62,
   'Fiat_Equiv': 'USD',
   'ID': 'BSCUs0dPqT',
   'Payment Transaction Hash': '41J8mFNRuHKhuZ6TnUjgQgkYdGNV6ojw5oYGLjwVMzZCMFUDMeUYU6LaCXALyNrX9dntdzAkDpWmz4SARenQr1eq',
   'Status': 'finished'
   }

resp = {
   'ID': 'nv5zU7HJUR',
 'status_url': 'https://trocador.app/anonpay/status/nv5zU7HJUR',
 'status_url_onion': 'http://trocadorfyhlu27aefre5u7zri66gudtzdyelymftvr4yjwcxhfaqsid.onion/status/nv5zU7HJUR',
 'url': 'https://trocador.app/anonpay/nv5zU7HJUR',
 'url_onion': 'http://trocadorfyhlu27aefre5u7zri66gudtzdyelymftvr4yjwcxhfaqsid.onion/nv5zU7HJUR'
 }


def genPayment(usdt_sol_address, fiat, amount, description, email='coxah@web.de', name="digicod.eu"):
   generator_url = f"https://trocador.app/anonpay/?ticker_to=usdt&network_to=SOL&address={usdt_sol_address}&fiat_equiv={fiat}&amount={amount}&name={name}&{description}=ertyrty&email={email}&ticker_from=sol&network_from=Mainnet&bgcolor=0a0a0aFF&direct=False"
   r = requests.get(generator_url)
   return r.json()

def getStatus():
   r = requests.get(response.get("status_url"))
   return r.json()


# res = genPayment()
res = getStatus()
pprint(res)

# FueJay1nmDTbyqeLEhb3nLPhHDWuJTpBTRcbtkVGeYxF