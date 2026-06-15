from google.oauth2 import id_token
from google.auth.transport import requests
import google

# (Receive token by HTTPS POST)
# ...
CLIENT_ID = "116760937607954145668"
token = "AFx_qI597r2Q7m1Ga2BucdDs4RfcmURxQhWZojbY36yCg9vX1uMqmdLO3sU1Mvtwyl4qbYVXlmb_Yt7ZMUBfhewC5miGkd1V1-03BoTS2KdUDYHq4bVDlGY15lBoQFRM_wY3DEDmePC2"
# try:
    # Specify the CLIENT_ID of the app that accesses the backend:
    # idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

    # Or, if multiple clients access the backend server:
    # idinfo = id_token.verify_oauth2_token(token, requests.Request())
    # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
    #     raise ValueError('Could not verify audience.')

    # If the request specified a Google Workspace domain
    # if idinfo['hd'] != DOMAIN_NAME:
    #     raise ValueError('Wrong domain name.')

    # ID token is valid. Get the user's Google Account ID from the decoded token.
#     userid = idinfo['sub']
#     print(userid)
# except ValueError:
#     print('invalid token')
#     pass