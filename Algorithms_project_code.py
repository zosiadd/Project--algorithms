class ImageGraph:
    # Graph initialization for image
    def __init__(self, image):
        self.image = image  # Assigning an image to an attribute of a class instance
        self.n = len(image)  # The size of the image (we assume that it is an n x n square array)
        self.edges = set()  # A collection that stores the edges of a graph, eliminating duplicate connections
        self.vertices = {}  # A dictionary storing the vertices of a graph and their attributes
        self.build_graph()  # Calling a method that builds a graph from an image

    # Adding a vertex to a graph - each vertex is identified by coordinates (i, j) in the image
    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = { "color": 0}  # Initialize vertex with default color 0 (no assigned component)

    # Adding edges to the graph - edges represent the neighborhood between two black pixels
    def add_edge(self, u, v):
        if (v, u) not in self.edges and (u, v) not in self.edges:
            self.edges.add((u, v))  # Adding edges between vertices

    # Function builds a neighborhood graph for black pixels in a raster image
    def build_graph(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-way neighborhood (up, down, left, right)
        for i in range(self.n):  # Iteration through the lines of the image
            for j in range(self.n):  # Iteration through image columns
                if self.image[i][j] == 1:  # If the pixel is black:
                    vertex_id = (i, j)  # Pixel coordinates as vertex identifier
                    self.add_vertex(vertex_id)  # Adding a vertex to a graph

                    for di, dj in directions:  # Iteration through possible neighborhood directions
                        ni, nj = i + di, j + dj  # Calculating the coordinates of a neighbora
                        if 0 <= ni < self.n and 0 <= nj < self.n and self.image[ni][nj] == 1:
                            # If the neighbor is within the image boundaries and is black:
                            self.add_edge(vertex_id, (ni, nj))  # Adding edges between vertices

    # The function identifies the disjoint components of the graph and assigns a unique identifier to each component
    def find_connected_components(self):
        visited = set()  # Set of visited vertices
        component_id = 1  # Identifier of the current component

        def dfs(vertex):
            stack = [vertex]  # Stack to store vertices to visit
            while stack:
                current = stack.pop()  # Get a vertex from the stack
                if current not in visited:  # If the vertex has not yet been visited:
                    visited.add(current)  # Mark it as visited
                    self.vertices[current]["color"] = component_id  # Assign a component ID
                    neighbors = [v for u, v in self.edges if u == current] + \
                                [u for u, v in self.edges if v == current]
                    # Finding all neighbors connected by an edge to the current vertex
                    for neighbor in neighbors:  # Adding neighbors to the stack only if they have not yet been visited
                        if neighbor not in visited:
                            stack.append(neighbor)

        for vertex in self.vertices:  # Iteration through all vertices of the graph
            if vertex not in visited:  # If the vertex has not been visited:
                dfs(vertex)  # Call DFS for a new component
                component_id += 1  # Increase the component identifier

        return component_id - 1  # Return the number of disconnected components

    # Function get_colored_image creates image with group component identifier for black pixels
    def get_colored_image(self):
        colored_image = [[0 for _ in range(self.n)] for _ in range(self.n)]  # Blank array n x n
        # Initialization of an empty n x n array, filled with 0 values (white pixels)
        for (i, j), attributes in self.vertices.items():  # Iteration through vertices and their attributes
            colored_image[i][j] = attributes["color"]  # Assigning a color component identifier
        return colored_image  # Returning a color image

    # A function that displays an image with assigned group component identifier
    def display_colored_image(self):
        print("Obraz z identyfikatorami grup:")
        for row in self.get_colored_image():     # Iterate through each row returned by the get_colored_image() method
            print(" ".join(map(str, row)))       # Convert each element in the row list to text,concatenate elements into a string separated by spaces

# Function responsible for retrieving data from the user
def get_user_image():
    try:
        n = int(input("Enter the size of the matrix (n x n): "))
        print("Enter matrix rows, using 0 for black pixels and 1 for white pixels.")
        image = []                         # Initialization of the post list, which will store the entered matrix rows
        for i in range(n):                 # Start the loop iterating n times, that is, as many times as many rows of the matrix selected by the user
            row = input(f"Row  {i + 1}: ")     # Input for each row of digits representing the matrix row
            if len(row) != n or not all(c in '01' for c in row):     # Checking if the length of the entered line = n and if there is a digit 1 or 0
                print("Error: A row must have exactly n characters '0' or '1'.")
                return None           # Return error in case of invalid data
            image.append([int(c) for c in row])     # Converts each character ‘0’ or ‘1’ to an integer and adds a list of numbers to the image liste
        return image    # Return a two-dimensional image list representing the matrix
    except ValueError:          # Checking for an error during data conversion
        print("Error: Please enter the correct integer.")
        return None

# The main() function allows the user to decide whether he wants to use the default matrix or enter his own
def main():
    use_default = input("Do you want to use the default matrix? (yes/no): ").strip().lower()
    if use_default == 'yes':
        image = [
            [0, 1, 0, 0],
            [1, 1, 0, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 0]
        ]

    else:
        image = get_user_image()
        if image is None:
            print("Failed to load the matrix. I am using the default matrix.")
            image = [
                [0, 1, 0, 0],
                [1, 1, 0, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 0]
            ]


    graph = ImageGraph(image)  # Create an object of class ImageGraph, passing it an image
    num_components = graph.find_connected_components()  # We find the number of disconnected components (black spots) in the graph
    colored_image = graph.get_colored_image() # Calling the get_colored_image() method of the graph object returning an array with the identifiers of each stain

    print(f"Number of disjointed white spots: {num_components}") # Print on the screen the number of distributed white spots found, using the value stored in the num_components variable
    print("Image with stain identifiers::")  # Writing out a headline indicating that below is an image with stain identifiers
    for row in colored_image:                # A for loop iterating over each row in the colored_image array
        print(' '.join(map(str, row)))       # Convert each row element row to a character string using the map(str, row) function
                                             # then combines these elements into a single string, separating them with spaces, and prints the result on the screen

# Checking if the script is run directly and not imported as a module

if __name__ == "__main__":
    main()   # Calling the main() function, which contains the main logic of the program
