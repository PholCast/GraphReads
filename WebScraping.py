from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from datetime import datetime

def getBookLinks():

    mainLinks = [
                "https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once",
                "https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=2",
                "https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=3"
                ]

    bookLinks = []
    for link in mainLinks:
        html = urlopen(link)
        objetoBS = BeautifulSoup(html.read(), features="html.parser")

        targetAnchor = objetoBS.find_all("a",{"class":"bookTitle"})

        currentLinks = [a["href"] for a in targetAnchor]

        currentLinks = list(map(lambda x: "https://www.goodreads.com"+x,currentLinks))
        
        bookLinks += currentLinks

    return bookLinks

def convertDate(dateString):
     
     # Remove "First published" from the string
     date_without_prefix = dateString.split(' ', 2)[-1]

     # Convert the remaining date to the desired format
     formatted_date = datetime.strptime(date_without_prefix, '%B %d, %Y').strftime('%d/%m/%Y')

     return formatted_date  # Output: 11/07/1960


def getData(dictionary, link):
    
        html = urlopen(link)
        objetoBS = BeautifulSoup(html.read(), features="html.parser")
        
        

        title = objetoBS.find("h1",{"class":"Text Text__title1"}).get_text()


        author = objetoBS.find("span",{"class":"ContributorLink__name"}).get_text()
        rating = objetoBS.find("div",{"class":"RatingStatistics__rating"}).get_text()

        date = objetoBS.find("p",{"data-testid":"publicationInfo"}).get_text()
        date = convertDate(date)

        genresSpan = objetoBS.find_all("span",{"class":"BookPageMetadataSection__genreButton"})

        genresList = []

        for i in range(3):
             genre = genresSpan[i].find("span").get_text()
             genresList.append(genre)

        print("Generos: ",genresList)
        print("Fecha: ",date)
        print("Titulo: ",title)
        print("Autor: ",author)
        print("Calificacion: ",rating)

        data[title] = {"Autor": author,"Fecha Publicacion":date,"Precio":None,"Calificacion":rating, "Generos":genresList}

        return data
        








data = {}


bookLinks = getBookLinks()

for i in range(len(bookLinks)):
     
    data = getData(data,bookLinks[i])
# print(bookLinks)
# print("\n\n EL LEN ES: ",len(bookLinks))


    








fileName = "BooksData.json"

#Guardar los datos en un archivo JSON
with open(fileName, 'w') as file:
     json.dump(data, file, indent=4)  # La función dump convierte el diccionario a formato JSON y lo guarda en el archivo