class ImageGraph:
    # Inicjalizacja grafu dla obrazu.
    def __init__(self, image):
        self.image = image  # Przypisanie obrazu do atrybutu instancji klasy
        self.n = len(image)  # Rozmiar obrazu (zakładamy, że jest to tablica kwadratowa n x n)
        self.edges = set()  # Zbiór przechowujący krawędzie grafu, eliminujący duplikaty połączeń
        self.vertices = {}  # Słownik przechowujący wierzchołki grafu i ich atrybuty
        self.build_graph()  # Wywołanie metody budującej graf na podstawie obrazu

    # Dodanie wierzchołka do grafu - każdy wierzchołek jest identyfikowany przez współrzędne (i, j) na obrazie
    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = { "color": 0}  # Inicjalizacja wierzchołka z domyślnym kolorem 0 (brak przypisanego komponentu)

    # Dodanie krawędzi do grafu - krawędzie reprezentują sąsiedztwo między dwoma czarnymi pikselami
    def add_edge(self, u, v):
        if (v, u) not in self.edges and (u, v) not in self.edges:
            self.edges.add((u, v))  # Dodanie krawędzi między wierzchołkami

    # Funkcja buduje graf sąsiedztwa dla czarnych pikseli w obrazie rastrowym
    def build_graph(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Sąsiedztwo 4-kierunkowe (góra, dół, lewo, prawo)
        for i in range(self.n):  # Iteracja przez wiersze obrazu
            for j in range(self.n):  # Iteracja przez kolumny obrazu
                if self.image[i][j] == 1:  # Jeśli piksel jest czarny:
                    vertex_id = (i, j)  # Współrzędne pikselu jako identyfikator wierzchołka
                    self.add_vertex(vertex_id)  # Dodanie wierzchołka do grafu

                    for di, dj in directions:  # Iteracja przez możliwe kierunki sąsiedztwa
                        ni, nj = i + di, j + dj  # Obliczenie współrzędnych sąsiada
                        if 0 <= ni < self.n and 0 <= nj < self.n and self.image[ni][nj] == 1:
                            # Jeśli sąsiad jest w granicach obrazu i jest czarny:
                            self.add_edge(vertex_id, (ni, nj))  # Dodanie krawędzi między wierzchołkami

    # Funkcja identyfikuje rozłączne komponenty grafu i przypisuje każdemu komponentowi unikalny identyfikator
    def find_connected_components(self):
        visited = set()  # Zbiór odwiedzonych wierzchołków
        component_id = 1  # Identyfikator aktualnego komponentu

        def dfs(vertex):
            stack = [vertex]  # Stos do przechowywania wierzchołków do odwiedzenia
            while stack:
                current = stack.pop()  # Pobierz wierzchołek ze stosu
                if current not in visited:  # Jeśli wierzchołek nie został jeszcze odwiedzony:
                    visited.add(current)  # Oznacz go jako odwiedzonego
                    self.vertices[current]["color"] = component_id  # Przypisz identyfikator komponentu
                    neighbors = [v for u, v in self.edges if u == current] + \
                                [u for u, v in self.edges if v == current]
                    # Znalezienie wszystkich sąsiadów połączonych krawędzią z aktualnym wierzchołkiem
                    for neighbor in neighbors:  # Dodanie sąsiadów do stosu tylko wtedy, gdy nie zostały jeszcze odwiedzone
                        if neighbor not in visited:
                            stack.append(neighbor)

        for vertex in self.vertices:  # Iteracja przez wszystkie wierzchołki grafu
            if vertex not in visited:  # Jeśli wierzchołek nie został odwiedzony:
                dfs(vertex)  # Wywołaj DFS dla nowego komponentu
                component_id += 1  # Zwiększ identyfikator komponentu

        return component_id - 1  # Zwróć liczbę rozłącznych komponentów

    # Funkcja get_colored_image tworzy obraz z identyfikatorami grup dla czarnych pikseli
    def get_colored_image(self):
        colored_image = [[0 for _ in range(self.n)] for _ in range(self.n)]  # Pusta tablica n x n
        # Inicjalizacja pustej tablicy n x n, wypełnionej wartościami 0 (białe piksele)
        for (i, j), attributes in self.vertices.items():  # Iteracja przez wierzchołki i ich atrybuty
            colored_image[i][j] = attributes["color"]  # Przypisanie koloru (identyfikatora komponentu)
        return colored_image  # Zwrócenie kolorowego obrazu

    # Funkcja wyświetlająca obraz z przypisanymi identyfikatorami grup
    def display_colored_image(self):
        print("Obraz z identyfikatorami grup:")
        for row in self.get_colored_image():     # Iteracja przez kazdy wiersz zwrocony przez metode get_colored_image()
            print(" ".join(map(str, row)))       # Konwersja każdego elementu z listy row na tekst,łączenie elementów w string oddzielony spacjami

# Funkcja odpowiedzialna za pobranie danych od uzytkownika
def get_user_image():
    try:
        n = int(input("Podaj rozmiar macierzy (n x n): "))
        print("Wprowadź wiersze macierzy, używając 0 dla czarnych pikseli i 1 dla białych pikseli.")
        image = []                         # Inicjalizacja postej listy, ktora bedzie przechowywać wprowadzone wiersze macierzy
        for i in range(n):                 # Rozpoczecie petli iterujacej n razy, czyli tyle razy ile wierszy macierzy wybral uzytkownik
            row = input(f"Wiersz {i + 1}: ")     # Wprowadzenie dla kazdego wiersza cyfr reprezentujacych wiersz macierzy
            if len(row) != n or not all(c in '01' for c in row):     # Sprawdzenie czy dlugosc wprowadzonego wiersza = n i czy jest cyfra 1 V 0
                print("Błąd: Wiersz musi mieć dokładnie n znaków '0' lub '1'.")
                return None           # Zwrocenie bledu w przypadku nieprawidlowych danych
            image.append([int(c) for c in row])     # Konwertuje każdy znak '0' lub '1' na liczbę całkowitą i dodaje listę liczb do listy image
        return image    # Zwrocenie dwuwymiarowej listy image reprezentujacej macierz
    except ValueError:          # Sprawdzenie czy podczas konwersji danych nie pojawil sie blad
        print("Błąd: Proszę wprowadzić poprawną liczbę całkowitą.")
        return None

# Funkcja main() pozwala uzytkownikowi zadecydowac czy chce on uzyc domyslnej macierzy, czy wprowadzic wlasna
def main():
    use_default = input("Czy chcesz użyć domyślnej macierzy? (tak/nie): ").strip().lower()
    if use_default == 'tak':
        image = [
            [0, 1, 0, 0],
            [1, 1, 0, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 0]
        ]

    else:
        image = get_user_image()
        if image is None:
            print("Nie udało się wczytać macierzy. Używam domyślnej macierzy.")
            image = [
                [0, 1, 0, 0],
                [1, 1, 0, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 0]
            ]


    graph = ImageGraph(image)  # Tworzymy obiekt klasy ImageGraph, przekazując mu obraz
    num_components = graph.find_connected_components()  # Znajdujemy liczbę rozłącznych komponentów (czarnych plam) w grafie
    colored_image = graph.get_colored_image() # Wywołanie metody get_colored_image() obiektu graph zwracajacej macierz z identyfikatorami poszczególnych plam

    print(f"Liczba rozłącznych białych plam: {num_components}") # Wypisanie na ekranie liczby znalezionych rozlacznych bialych plam, korzystajac z wartosci przechowywanej w zmiennej num_components
    print("Obraz z identyfikatorami plam:")  # Wypisanie nagłówka informujacego, ze poniżej znajduje sie obraz z identyfikatorami plam
    for row in colored_image:                # Pętla for iterująca po kazdym wierszu w macierzy colored_image
        print(' '.join(map(str, row)))       # Konwersja kazdego elementu wiersza row na łańcuch znaków za pomocą funkcji map(str, row),
                                             # następnie łączy te elementy w jeden łańcuch, oddzielając je spacjami, i wypisuje wynik na ekranie

# Sprawdzenie czy skrypt jest uruchamiany bezpośrednio, a nie importowany jako moduł

if __name__ == "__main__":
    main()   # Wywołanie funkcji main(), zawierajacej glowna logike programu