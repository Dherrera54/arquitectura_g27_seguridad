from hashlib import new
import requests
from flask import Flask
from random import randint, random
import json

def random_character():
    return random_character.choices[randint(0, random_character.size)]

random_character.choices = "qwertyuipoasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890-_+*!/#$?&"
random_character.size = len(random_character.choices) - 1


def generate_keys(lenght):
    key = ''
    while len(key) < lenght:
        key = key + random_character()
    return key


def build_token():
    return generate_keys(37) + '.' + generate_keys(72) + '.' + generate_keys(42)

def build_altered_token(token):
    size = len(token)-1
    index = randint(0, size)
    current_character = token[index]
    new_character = random_character()
    while new_character == current_character:
        new_character = random_character()
    
    altered_token = token[:index] + new_character
    if index != size:
        altered_token = altered_token + token[index + 1:]
    return altered_token
    

def attack(token):
    choice = randint(0,2)
    if choice == 0: # attack without a token
        return {"Type": "Not Token Attack", "Token used": "", "Status code": requests.get('http://localhost:5000/paciente/2').status_code}
    
    if choice == 1: # attack with a random token
        random_token = build_token()
        headers = {"Authorization": "Bearer " + build_token()}
        return {"Type":"Random Token Attack", "Token used": random_token, "Status code": requests.get('http://localhost:5000/paciente/2', headers = headers).status_code}
    
    if choice == 2: # attack using an altered token
        altered_token = build_altered_token(token)
        headers = {"Authorization": "Bearer " + altered_token}
        return {"Type": "Altered Token Attack", "Token used" : altered_token, "Status code": requests.get('http://localhost:5000/paciente/2', headers = headers).status_code}
        

def correct_request(token):
    headers = {"Authorization": "Bearer " + token}
    return requests.get('http://localhost:5000/paciente/2', headers = headers)

if __name__ == '__main__':

    # login with correct credentilas to optain a valid token
    credentials = {"nombre": "EstebanPalacios123", "contrasena": "esteban2021"}
    data = json.loads(requests.post('http://localhost:5000/login', json = credentials).content)
    correct_token = data["token"]

    attack_count = 0
    total_attends = 100
    attack_probability = 0.5
    successful_attack_count = 0
    iter = 1
    print("Correct token:", correct_token)
    while attack_count < 100:
        possible_attack = random() < attack_probability
        if possible_attack:
            attack_count = attack_count + 1
            attack_info =  attack(correct_token)
            success = attack_info["Status code"] == 200
            if success:
                successful_attack_count = successful_attack_count + 1
            print(str(iter) + ")", f"Attack({attack_count}) -> Attack Info: {attack_info} -> {'Passed' if success else 'Not passed'}")
        else:
            print(str(iter)+ ")", "Correct Request -> Responce:",correct_request(correct_token))
        iter = iter + 1 

    print("Execution ended.")
    print("Successfull attacks: ", successful_attack_count)