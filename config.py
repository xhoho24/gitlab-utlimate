import os
Var = os.environ.get

APP_ID= int(Var("APP_ID"))
API_HASH = Var("API_HASH")
BOT_TOKEN = Var("BOT_TOKEN")
LOG_CHANNEL = int(Var("LOG_CHANNEL"))
ADMIN = Var("ADMIN")
IP = Var("PROXY")
PROXY = {'http':'socks5://'+IP,'https':'socks5://'+IP,}