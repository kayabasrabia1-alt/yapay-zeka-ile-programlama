import os

def read_user_file(filename):
    # Zafiyetli kod: Dosya yolu doğrulanmadan kök dizinle birleştiriliyor
    base_dir = "/var/www/uploads/"
    file_path = base_dir + filename
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()