def transpose_matrix_inplace(matrix):
    # Create a temporary dictionary to store the transposed values
    transposed = {}
    for (row, col), value in matrix.items():
        transposed[(col, row)] = value
    
    # Clear the original matrix and update it with the transposed values
    matrix.clear()
    matrix.update(transposed)

# Example usage:
matrix = {
    (0, 0): 1, (0, 1): 2, (0, 2): 3,
    (1, 0): 4, (1, 1): 5, (1, 2): 6,
    (2, 0): 7, (2, 1): 8, (2, 2): 9
}

transpose_matrix_inplace(matrix)

# Output the modified matrix
for key, value in sorted(matrix.items()):
    print(f"{key}: {value}")
