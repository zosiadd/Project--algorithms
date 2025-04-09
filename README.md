# Project-algorithms
The goal of this project is to process a raster image represented as an n x n array of black and white pixels, and to identify and label all distinct black regions (connected components). The solution consists of three main steps:

Graph Construction
Black pixels are treated as graph vertices. Edges are added between neighboring black pixels using 4-connectivity (top, bottom, left, right).

Connected Components Detection
A Depth-First Search (DFS) algorithm is used to explore the graph and detect distinct connected components, each representing a separate black region.

Region Labeling
Each black pixel is assigned a unique identifier corresponding to its region, creating a result matrix that visually distinguishes individual blobs.

Example:



![image](https://github.com/user-attachments/assets/3f5dd0c4-8cf7-4d9d-bd9b-2d5e78cb9cfb)




Output:
Number of distinct black regions
Matrix with labeled regions (black pixels marked with region IDs, white pixels as 0)

The program supports both user-defined and default input matrices and gracefully handles invalid input by falling back to the default option.

This project was carried out as part of student projects by: zosiadd and Aleksandra Gałczyńska
