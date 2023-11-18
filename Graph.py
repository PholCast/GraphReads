import json

class Graph:
    def __init__(self):
        self.list = {}  # Lista de adyacencia
        self.size = 0   # Número de nodos
        self.nodes = []  # Lista de nodos

    def add_vertex(self, v):
        if v in self.list:
            print(f"El nodo {v} ya existe")
            return
        else:
            self.list[v] = []
            self.size = len(self.list)

    def add_edge(self, v1, v2, weight):
        if not v1 in self.list:
            self.add_vertex(v1)
        if not v2 in self.list:
            self.add_vertex(v2)

        # Verificar si la relación ya existe antes de agregarla
        existing_edges = [neighbor for neighbor, _ in self.list[v1]]
        if v2 in existing_edges:
            print(f"La relación entre {v1} y {v2} ya existe.")
        else:
            self.list[v1].append((v2, weight))

    def load_from_json(self, json_file):
        with open(json_file) as f:
            data = json.load(f)

        # agregando los conceptos (de los que salen las instancias)...
        self.add_vertex("Libro")
        self.add_vertex("Autor")
        self.add_vertex("Fecha Publicacion")
        self.add_vertex("Precio")
        self.add_vertex("Calificacion")
        self.add_vertex("Genero")
        
        for book, attributes in data.items():
            
            self.add_vertex(book) # Nodo para el libro
            self.add_edge(book, "Libro", 11) # relación con el concepto libro
            
            for attribute, value in attributes.items():
                
                if attribute =="Autor":
                    self.add_vertex(value)  # Nodos pal autor
                    self.add_edge(book, value, 1) 
                    self.add_edge(value, book, 2) 
                    # la relación que indica que es 
                    self.add_edge(value, "Autor", 11) 
                
                if attribute =="Fecha Publicacion":
                    self.add_vertex(value)  # Nodo pa la fecha 
                    self.add_edge(book, value, 3) 
                    self.add_edge(value, book, 4) 
                    # la relación que indica que es 
                    self.add_edge(value, "Fecha Publicacion", 11) 
                    
                if attribute == "Precio":
                    self.add_vertex(value)  # Nodo pal precio 
                    self.add_edge(book, value, 5) 
                    self.add_edge(value, book, 6) 
                    # la relación que indica que es 
                    self.add_edge(value, "Precio", 11) 
                    
                if attribute == "Calificacion":
                    self.add_vertex(value)  # Nodo pal score o rate idk
                    self.add_edge(book, value, 7) 
                    self.add_edge(value, book, 8)  
                    # la relación que indica que es 
                    self.add_edge(value, "Calificacion", 11) 
                
                if attribute == "Generos":
                    for genre in value:
                        self.add_vertex(genre)  # Nodo pal género
                        self.add_edge(book, genre, 9)  
                        self.add_edge(genre, book, 10) 
                        # la relación que indica que es 
                        self.add_edge(genre, "Genero", 11) 
                
    def print_graph(self):
        for node, edges in self.list.items():
            print(f"{node}: {edges}")
    
    def printGrafoFacherito(self):
        for node, edges in self.list.items():
            edge_str = ", ".join(f"{neighbor} ({weight})" for neighbor, weight in edges)
            print(f"{node} -> {edge_str}")

    # Según entiendo, la idea es que usar la lista de adyacencia para obtener un nodo de interés, 
    # y a partir de es nodo obtener información apartir de las relaciones...
    
    # este método me podría servir para simplificar algo...
    def isRelated(self, v1, v2, weight):
        for node, relation in self.list[v1]:
            if node == v2 and relation == weight:
                return True
        return False
    
    def getNodesByWeight(self, v, weight):
        nodes = []
        for node, relation in self.list[v]:
            if relation == weight:
                nodes.append(node)
        return nodes
    
    def FirstFunction(self, author):
        
        if not self.isRelated(author, "Autor", 11):
            print(" El autor no existe ....")
            return None
        
        books = []
        
        relations = self.list[author]
        for relation in relations:
            if relation[1] == 2:
                books.append(relation[0])
                print(relation[0])
        
        return books
    
    def SecondFunction(self, book):
        
        if not self.isRelated(book, "Libro", 11):
            print(" El libro no existe ....")
            return None
        
        books = []
        genres = []
        booksFromGenres = []
        
        relations = self.list[book]
        for relation in relations:
            if relation[1] == 9:
                genres.append(relation[0])
                print(relation[0])
        
        for genre in genres:
            genre_relations = self.list[genre]
            for relation in genre_relations:
                if relation[1] == 10:
                    booksFromGenres.append(relation[0])
                    print(relation[0])
        
        # Aquí se filtra el tema de la decada...
        # primero ver cual sería la decada del libro dado :
        
        relations = self.list[book]
        for relation in relations:
            if relation[1] == 3:
                targetDate = relation[0]
        
        targetYear = int(targetDate.split("/")[-1])
        # Calcular la década
        targetDecade = (targetYear // 10) * 10
        
        print("el año de publicación del libro es: ", targetDate)
        
        # ahora mirar que libros son de esa misma decada
        for book in booksFromGenres:
            relations = self.list[book]
            for relation in relations:
                if relation[1] == 3:
                    date = relation[0]
            
            if not date:
                print ("wtf dizque no tiene fecha")
            
            # Extraer el año de la fecha
            año = int(date.split("/")[-1])
            # Calcular la década
            decada = (año // 10) * 10
            
            if decada == targetDecade:
                books.append(book)
                print("libro que es de la misma decada :", book, " que se publicó en el :", date)
                
        return books
    
    def ThridFunction(self, genre):
        
        # se meterá todo en un diccionario pa después ordenarlo 🧐
        authors = {}
        
        books = self.getNodesByWeight(genre, 10)
        
        if books == []:
            print("no hay libros con ese genero ")
            return None
        
        for book in books:
            author = self.getNodesByWeight(book, 1)
            
            if not len(author) == 1:
                print("dizque el libro tiene varios autores")
                return None
            
            author = author[0]
            if author:
                if author not in authors:
                    authors[author] = 1
                else:
                    authors[author] += 1
        
        # Ordenar el diccionario por los valores en orden descendente
        orderedAuthors = dict(sorted(authors.items(), key=lambda x: x[1], reverse=True))

        # Imprimir el diccionario ordenado
        print(orderedAuthors)
        
        return orderedAuthors
    
    def ForthFunction(self, genres, score):
        
        genresbooks = []
        
        for genre in genres:
            
            books = self.getNodesByWeight(genre, 10)
            
            if books == []:
                print("no hay libros con ese genero ")
                return None
            
            for book in books:
            
                # Puntaje como string
                string_score = self.getNodesByWeight(book, 7)[0]

                # Convertir la cadena a un número decimal (punto flotante)
                decimal_score = float(string_score)

                # Verificar si el puntaje decimal es mayor que el número entero
                if decimal_score > score:
                    genresbooks.append(book)
    
        print (genresbooks)
        return genresbooks
        
    
    def FifthFunction(self, genres, amount):
        
        shoppingList = []
        
        pricedBooks = {}
        
        for genre in genres:
            
            books = self.getNodesByWeight(genre, 10)
            
            if books == []:
                print("no hay libros con ese genero ")
                return None
            
            for book in books:
                if book not in pricedBooks:
                    price = self.getNodesByWeight(book, 5)[0]
                    pricedBooks[book] = price
                    
        # Ordenar el diccionario por los valores en orden ascendente
        orderedBooksByPrice = dict(sorted(pricedBooks.items(), key=lambda x: x[1], reverse=False))
        
        currentAmount = 0
        
        for book, price in orderedBooksByPrice.items():
            if currentAmount > amount:
                break
            shoppingList.append(book)
            print("Se agregó el libro ", book, " con precio ", price, " a la lista de compras")
            currentAmount += price
        
        print(shoppingList)
        return shoppingList
        
# Ejemplo de uso
grafo = Graph()
grafo.load_from_json("BooksData.json")
grafo.print_graph()
print (grafo.isRelated('New Moon', 'Stephenie Meyer', 1))
print (grafo.isRelated('New Moon', 'The Foundation Trilogy', 2)) 

books = grafo.FifthFunction(["Fiction"], 14.99)

#Holocaust
#The God of Small Things
#Judy Blume: [("Are You There God? It's Me, Margaret", 2), ('Autor', 11)]