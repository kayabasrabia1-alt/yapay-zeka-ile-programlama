import os

def ping_host(user_ip):
    # Zafiyetli kod: Kullanıcı girdisi doğrudan kabuk komutuna gönderiliyor
    os.system("ping -c 1 " + user_ip)