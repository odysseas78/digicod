import os, sys
import subprocess
sys.path.insert(0, '/home/dcback')
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from django.core.mail import send_mail
from pprint import pprint


# Überprüfen, ob der gunicorn-Service ausgeführt wird
# if "active (running)" in str(subprocess.check_output(['systemctl', 'status', 'prices_sync'])):
#     print("Der gunicorn-Service ist ausgeführt.")
#     # Fügen Sie hier den Code ein, den Sie ausführen möchten, wenn der Service ausgeführt wird
# else:
#     print("Der prices_sync-Service DOWN.")
    # send_mail('prices_sync inactive', 'prices_sync inactive' , 'info@digicod.eu', ['admin@digicod.eu'], fail_silently=False)

# if os.system('systemctl status prices_sync | grep -q "Active: active (running)"') != 0:
#     send_mail('prices_sync inactive', 'prices_sync inactive' , 'info@digicod.eu', ['admin@digicod.eu'], fail_silently=False)
send_mail('malakies dfgsdgfsdfg', 'sdfgsdfgsdf dfg dfgsdfg' , 'info@digicod.eu', ['admin@digicod.eu'], fail_silently=False)