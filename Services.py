from Graph import Graph

class Services:
    def __init__(self, graph):
        self.graph = graph

    def list_books_by_author(self, author):
        # Obtener los libros del autor ordenados por fecha de lanzamiento
        books = [(neighbor, weight) for neighbor, weight in self.graph.list[author]]
        books.sort(key=lambda x: self.graph.list[x[0]][0][1])  # Ordenar por fecha de lanzamiento
        return books

    def recommend_books_by_genre_and_decade(self, book, n):
        # Obtener libros del mismo género y década que el libro dado
        genre, _ = self.graph.list[book][1]
        decade = int(self.graph.list[book][2][0][-2:]) // 10 * 10  # Obtener década del año de publicación
        
        recommended_books = [(neighbor, weight) for neighbor, weight in self.graph.list if
                            neighbor != book and self.graph.list[neighbor][1][0] == genre
                            and int(self.graph.list[neighbor][2][0][-2:]) // 10 * 10 == decade]
        return recommended_books[:n]


grafo = Graph()
grafo.load_from_json("BooksData.json")

services = Services(grafo)

# Listar los libros del autor X ordenados por fecha de lanzamiento
author_books = services.list_books_by_author("Stephen King")
print("Libros de Stephen King ordenados por fecha de lanzamiento:")
for book, date in author_books:
    print(f"{book} - Fecha de lanzamiento: {date}")

# Recomendar N libros del mismo género y de la misma década que el libro X
"""recommendations = services.recommend_books_by_genre_and_decade("The Shining", 3)
print("\nRecomendaciones para libros similares a 'The Shining':")
for book, _ in recommendations:
    print(book)"""
