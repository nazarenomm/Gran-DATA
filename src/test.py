import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE + "usuario", json={
    "nombre": "jose",
    "apellido": "pereyra",
    "mail": "jpereyra@gmail.com",
    "contraseña": "1234",
    "telefono": 1234
})

print("Status Code:", response.status_code)
print("Response Text:", response.text)  # Imprime el contenido crudo de la respuesta
try:
    print("JSON Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("La respuesta no es JSON.")

input()

response = requests.get(BASE + "usuario/1")
print("Status Code:", response.status_code)
print("Response Text:", response.text)
try:
    print("JSON Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("La respuesta no es JSON.")
