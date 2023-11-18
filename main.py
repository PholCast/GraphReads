import json 
# Lee el contenido del archivo JSON
with open('BooksData.json', 'r') as file:
    data = json.load(file)

# Ahora, 'BooksData.json' es un diccionario que contiene la información del archivo JSON
print(data)