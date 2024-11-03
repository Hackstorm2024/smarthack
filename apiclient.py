import requests
import json
from config import API_KEY, BASE_URL

session_id = ""

# porneste o sesiune si returneasa id-ul sesiuni
def start_session(api_key, base_url):
    headers = {
        'API-KEY': api_key,
        "accept": "*/*"
    }

    try:
        # face request-ul catre server si memoreaza raspunsu-l
        # in variabila response
        response = requests.post(base_url+"session/start", headers=headers)

        # verifica daca a create o sesiune cu succes
        if response.status_code == 200:
            return response.text.strip() # returneaza id-ul de sesiunea
        
        else:
            # daca response da faild, returnam False cu raspunsul
            return False, response.status_code, response.text
        
    except requests.exceptions.RequestException as e:
        # In cazul unei erori a functii request returnam False si mesajul de eroare
        return False, str(e)


# inchide o sesiune
def end_session(api_key, base_url): 
    headers = {
        'API-KEY': api_key,
        "accept": "*/*"
    }

    try:
        # face request-ul catre server si memoreaza raspunsu-l
        # in variabila response
        response = requests.post(base_url+"session/end", headers=headers)

        # verifica daca a inchis sesiunea cu succes 
        if response.status_code == 200:
            print("YES!")
            # returneaza True daca a inschis sesiunea cu succes
            # si text-ul de la response
            return response.text
            
        else:
            
            # daca response da faild, returnam False cu raspunsul
            return response.status_code, response.text
        
    except requests.exceptions.RequestException as e:
        print("DEFAP!")
        # In cazul unei erori a functii request returnam False si mesajul de eroare
        return False

def play_round(data, session, base_url, api_key):
    headers = {
        'API-KEY': api_key,
        'SESSION-ID': session
    }

    try:
        response = requests.post(base_url + "play/round", headers=headers, json=data)

        if response.status_code == 200:
            return response.json().get('demand', [])  # Ensure it returns a list or empty list
        else:
            print(f"Error in play_round: {response.status_code} - {response.text}")
            return []  # Return an empty list in case of an error

    except requests.exceptions.RequestException as e:
        print(f"Request exception in play_round: {e}")
        return []  # Return an empty list if there’s an exception

    

# session_id = start_session()
# print(session_id)

# for i in range(42):
#     with open(f'day_{i}.json', 'r') as f:
#         day_data = json.load(f)  # Load the JSON data as a dictionary

#         print(play_round(day_data, session_id))
#         print('tried for ',i)

# print(end_session())
