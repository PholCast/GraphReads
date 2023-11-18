from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from datetime import datetime
import random

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
     try:
      formatted_date = datetime.strptime(date_without_prefix, '%B %d, %Y').strftime('%d/%m/%Y')
     except:
      months = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
      formatted_date= date_without_prefix.replace(",","")
      formatted_date = formatted_date.split(" ")

      formatted_date = f"{formatted_date[1]}/{str(months.index(formatted_date[0])+1)}/{formatted_date[2]}"

     return formatted_date


def getData(dictionary, link):
    
        html = urlopen(link)
        objetoBS = BeautifulSoup(html.read(), features="html.parser")
        
        
        try:
            title = objetoBS.find("h1",{"class":"Text Text__title1"}).get_text()
        except Exception as e:
            print("Hubo una tragedia:",e)
            return dictionary





        author = objetoBS.find("span",{"class":"ContributorLink__name"}).get_text()
        rating = objetoBS.find("div",{"class":"RatingStatistics__rating"}).get_text()

        date = objetoBS.find("p",{"data-testid":"publicationInfo"}).get_text()
        date = convertDate(date)

        genresSpan = objetoBS.find_all("span",{"class":"BookPageMetadataSection__genreButton"}) 

        genresList = []
        
        for i in range(len(genresSpan)):
             if i == 3:
                 break
             genre = genresSpan[i].find("span").get_text()
             genresList.append(genre)
             
        
        button = objetoBS.find("button",{"class":"Button Button--buy Button--medium Button--block"})

        spanPrice = button.find("span").get_text()

        price = round(random.uniform(0.50,20.99),2)
        
        if "$" in spanPrice:
            price = float(spanPrice.split("$")[-1])
        

            
            


        
        print("Precio: ",price)
        print("Generos: ",genresList)
        print("Fecha: ",date)
        print("Titulo: ",title)
        print("Autor: ",author)
        print("Calificacion: ",rating)

        dictionary[title] = {"Autor": author,"Fecha Publicacion":date,"Precio":price,"Calificacion":rating, "Generos":genresList}

        return dictionary
        








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