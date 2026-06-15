import os

with open('prodfiles2.txt', 'r') as f:
      text = f.read()
#   first_chars = [char for char in text.split()]
incld = ''
for lin in text.split():
    os.system(f"zip -r dcprod.zip {lin}")

# os.system("ssh user@dcprod.loc 'cd /home/dcback/eshop/ && zip -r migrations.zip migrations && mv migrations.zip /home/dc/'")
# os.system("ssh user@dcprod.loc 'cd /home/dcback/ && source ~/.zshrc && echo user | sudo -S sh /home/dcback/systemd/bash/start.sh'")
psww = 'user'
os.system("ssh user@dcprod.loc 'rm -rf /home/dcback/*'")
os.system("scp dcprod.zip user@dcprod.loc:/home/dcback/")
os.system("rm -rf dcprod.zip")
os.system(f"ssh user@dcprod.loc 'cd /home/dcback/ && unzip dcprod.zip && mv .env_prod .env && rm -rf dcprod.zip\
           && source ~/.zshrc && poetry update && poetry run python manage.py migrate && echo {psww} | sudo -S sh /home/dcback/systemd/bash/stop.sh && \
          echo {psww} | sudo -S sh /home/dcback/systemd/bash/remove.sh && echo {psww} | sudo -S sh /home/dcback/systemd/bash/hardlink.sh && echo {psww} | sudo -S sh /home/dcback/systemd/bash/start.sh && echo {psww} | sudo -S sh /home/dcback/systemd/bash/restart.sh && echo {psww} | sudo -S systemctl restart nginx'")

# os.system(f"sh /home/dcback/delcontent.sh && mv /home/dcback/dcprod.zip /home/dcback/deploy/ && cd /home/dcback/deploy/ && \
#           unzip dcprod.zip && mv .env_prod .env && rm -rf dcprod.zip")
# os.system(f"rsync -avzr /home/dcback/deploy/ ")
# os.system(f"ssh user@dcprod.loc 'cd /home/dcback && source ~/.zshrc && poetry update'")

# os.system(f"ssh user@dcprod.loc 'cd /home/ && mkdir dc && cd dc && mkdir dcprod'")
# os.system(f"scp dcprod.zip user@dcprod.loc:/home/dcback/")
# os.system(f"ssh user@dcprod.loc 'cd /home/dcback && unzip dcprod.zip && rm -rf dcprod.zip'")
# os.system(f"rm -rf dcprod.zip")

# os.system(f"zip -r cdnx.zip cdnx")
# os.system(f"scp cdnx.zip user@dcprod.loc:/home/dcback/")
# os.system(f"ssh user@dcprod.loc 'cd /home/dcback && unzip cdnx.zip && rm -rf cdnx.zip'")
# os.system(f"rm -rf cdnx.zip'")

# print(incld)
# os.system("zip -r small_v.zip /home/dcback/cdnx/media/ ")
# os.system(f"rsync -avr --exclude='*media/' --include='*media/brands/' --exclude='*node_modules/' --exclude='*package-lock.json' /home/dcback/cdnx/ user@guiworker.loc:/home/dcback/cdnx/")