# The array A contains values [1, X].
# The concept is to find the minimum index i, on which, all the  values
# from 1 to X is found.

def Solution(X, A):
    array_len = len(A)
    # A set() always contains unique values
    unique_vals = set()

    for i in range(array_len):
        unique_vals.add(A[i])
        if len(unique_vals) == X:
            return i

    # Just in case, if the solution doesn't exist
    return -1


if __name__ == "__main__":
    # Running a demo
    X = 5
    A = [1, 3, 1, 4, 2, 3, 5, 4]

    print(f"Answer: {Solution(X, A)}")
