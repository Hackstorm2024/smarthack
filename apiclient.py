import requests

from config import API_KEY, BASE_URL

session_id = ""

# porneste o sesiune si returneasa id-ul sesiuni
def start_session():
    headers = {
        'API-KEY': API_KEY,
        "accept": "*/*"
    }

    try:
        # face request-ul catre server si memoreaza raspunsu-l
        # in variabila response
        response = requests.post(BASE_URL+"session/start", headers=headers)

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
def end_session(): 
    headers = {
        'API-KEY': API_KEY,
        "accept": "*/*"
    }

    try:
        # face request-ul catre server si memoreaza raspunsu-l
        # in variabila response
        response = requests.post(BASE_URL+"session/end", headers=headers)

        # verifica daca a inchis sesiunea cu succes 
        if response.status_code == 200:

            # returneaza True daca a inschis sesiunea cu succes
            # si text-ul de la response
            return True
            
        else:
            # daca response da faild, returnam False cu raspunsul
            return False
        
    except requests.exceptions.RequestException as e:
        # In cazul unei erori a functii request returnam False si mesajul de eroare
        return False

def play_round(data, session): # data = informatiile pe care la dam ca answer

    headers = {
        'API-KEY': API_KEY,
        'SESSION-ID': session
    }

    try:
        # face request-ul catre server si memoreaza raspunsu-l
        # in variabila response
        response = requests.post(BASE_URL+"play/round", headers=headers, json=data)

        # verifica daca a inchis sesiunea cu succes 
        if response.status_code == 200:

            # returneaza True daca a inschis sesiunea cu succes
            # si text-ul de la response
            return response.json()  # Successful response

            
        else:
            
            return False, response.json()
           
    except requests.exceptions.RequestException as e:
        # In cazul unei erori a functii request returnam False si mesajul de eroare
        return False, e