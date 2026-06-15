import subprocess

import os.path
import os

import boto3

# If modifying these scopes, delete the file token.json.
from googleapiclient.http import MediaFileUpload

def backup_postgres_db(host, database_name, port, user, password, dest_file, verbose):
    """
    Backup postgres db to a file.
    """
    if verbose:
        try:
            process = subprocess.Popen(
                ['pg_dump',
                 '--dbname=postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database_name),
                 '-Fc',
                 '-f', dest_file,
                 '-v'],
                stdout=subprocess.PIPE
            )
            output = process.communicate()[0]
            if int(process.returncode) != 0:
                print('Command failed. Return code : {}'.format(process.returncode))
                exit(1)
            return output
        except Exception as e:
            print(e)
            exit(1)
    else:

        try:
            process = subprocess.Popen(
                ['pg_dump',
                 '--dbname=postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database_name),
                 '-f', dest_file],
                stdout=subprocess.PIPE
            )
            output = process.communicate()[0]
            if process.returncode != 0:
                print('Command failed. Return code : {}'.format(process.returncode))
                exit(1)
            return output
        except Exception as e:
            print(e)
            exit(1)

# SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']

def db_bu_upload_gdrive():
    # from config.settings import env_dict
    backup_postgres_db(env_dict.get('DB_HOST'), env_dict.get('DB_NAME'), env_dict.get('DB_PORT'), env_dict.get('DB_USER'),
                       env_dict.get('DB_PASSWORD'), 'digicod_db', False)
    os.system('gpg -r haupt -e digicod_db')
    session = boto3.Session(
        aws_access_key_id=env_dict.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=env_dict.get('AWS_SECRET_ACCESS_KEY'),
    )
    s3 = session.resource('s3')
    # Filename - File to upload
    # Bucket - Bucket to upload to (the top level directory under AWS S3)
    # Key - S3 object name (can contain subdirectories). If not specified then file_name is used
    s3.meta.client.upload_file(Filename='digicod_db.gpg', Bucket='digicod', Key='digicod_db.gpg')

    os.system('rm -rf digicod_db digicod_db.gpg')


# db_bu_upload_gdrive()



# backup_postgres_db('10.251.167.203', 'dcdev2', '5432', 'dcdev', 'Od_290178', './digicod_db', True)
