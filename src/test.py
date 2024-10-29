import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE + "usuario", json={
    "nombre": "pedro",
    "apellido": "herrera",
    "mail": "pedroh@gmail.com",
    "contraseña": "1234pehe",
    "telefono": 1234329923
})

print("Status Code:", response.status_code)
print("Response Text:", response.text)  # Imprime el contenido crudo de la respuesta
try:
    print("JSON Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("La respuesta no es JSON.")

input()

response = requests.get(BASE + "usuario/2")
print("Status Code:", response.status_code)
print("Response Text:", response.text)
try:
    print("JSON Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("La respuesta no es JSON.")
