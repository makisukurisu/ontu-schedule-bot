from decouple import config

API_TOKEN = config('API_TOKEN', default=None)
if not API_TOKEN:
    print("API_TOKEN not found in .env")
    API_TOKEN = input("Enter API_TOKEN for telegram bot: ")
    with open('.env', 'a+', encoding='UTF-8') as file:
        file.write(f'API_TOKEN={API_TOKEN}')
    print("Saved API_TOKEN to .env")

API_URL = config('API_URL', default=None)
if not API_URL:
    print("API_URL not found in .env")
    API_URL = input("Enter API_URL for admin server of bot: ")
    with open('.env', 'a+', encoding='UTF-8') as file:
        file.write(f'API_URL={API_URL}')
    print("Saved API_URL to .env")