import os

# Вытягиваем токен из .env файла, который игнорируется гитом
with open('.env', 'r') as file:
    line = file.readline()
    os.environ[line[:line.find("=")]] = line[line.find("=") + 1:]

token = os.environ['token']
