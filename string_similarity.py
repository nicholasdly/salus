
def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculates the Levenshtein distance between two strings, a common number
    used to calculate the difference between two strings.

    s1: The first string
    s2: The second string

    returns: The Levenshtein distance
    """

    # TODO: Can this be made faster?

    # Creates a "distance matrix," which stores the difference between two
    # strings.
    dist_matrix = [[col+row for col in range(len(s2)+1) if col == 0 or row == 0] for row in range(len(s1)+1)]

    # Traverses the distance matrix row by row from left to right, calculating
    # the difference between the two strings.
    for r in range(1, len(dist_matrix)):
        for c in range(1, len(dist_matrix[0])):
            x = min(dist_matrix[r-1][c-1],
                    dist_matrix[r-1][c],
                    dist_matrix[r][c-1])

            if (r-1 == c-1 or (len(s1) == r and len(s2) == c)) and s1[r-1] == s2[c-1]:
                dist_matrix[r].append(x)
            else:
                dist_matrix[r].append(x+1)

    return dist_matrix[-1][-1]

def hamming_distance(s1: str, s2: str) -> int:
    """
    Calculates the Hamming distance between two strings of equal length. Similar
    to the Levenshtein distance, the number can be used to calculate the
    difference between two strings.

    s1: The first string
    s2: The second string
    
    returns: The Hamming distance
    """
    if len(s1) != len(s2):
        raise Exception("Strings must be of equal length when calculating Hamming distance!")

    # For every letter that is not the same, the Hamming distance increases.
    distance = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            distance += 1
    return distance

def edit_similarity(s1, s2):
    """
    """
    s1, s2 = s1.lower(), s2.lower()
    if len(s1) == 0 or len(s2) == 0:
        return 0
    if len(s1) == len(s2):
        return (len(s1) - hamming_distance(s1, s2)) / len(s1)
    return (min(len(s1), len(s2)) - levenshtein_distance(s1, s2)) / min(len(s1), len(s2))

def longest_common_substring(s1, s2):
    """
    """
    substring = ""
    x, y, max_length = 0, 0, 0
    matrix = [[0] * (len(s2) + 1)]

    for r in range(1, len(s1) + 1):
        matrix.append([])

        for c in range(len(s2) + 1):
            if s1[r-1] == s2[c-1] and c != 0:
                matrix[r].append(matrix[r-1][c-1] + 1)
            else:
                matrix[r].append(0)

            if matrix[r][c] > max_length:
                x, y = r, c
                max_length = matrix[r][c]

    while len(substring) != max_length:
        substring = s1[x-1] + substring
        x, y = x-1, y-1
    return substring

def count_matching_chars(s1, s2):
    """
    """
    count = 0
    substring = longest_common_substring(s1, s2)

    if len(substring) == 0:
        return count

    count += len(substring)
    s1, s2 = s1.replace(substring, " "), s2.replace(substring, " ")
    l = zip(s1.split(), s2.split())

    for x, y in l:
        count += count_matching_chars(x, y)
    return count

def sequence_similarity(s1, s2):
    """
    """
    s1, s2 = s1.lower(), s2.lower()
    if len(s1) == 0 or len(s2) == 0:
        return 0
    return 2 * count_matching_chars(s1, s2) / (len(s1) + len(s2))
