"""
Nicholas Ly (lynichol@msu.edu)
ShellHacks 2022
September 11, 2022

Although not used in the final submission of this project to the hackathon, I
had began my approach to the task by doing research in string metrics and
similarity algorithms! I began with Levenshtein distance, and utilized Hamming
distance to make calculating edit distance faster. I realized sequence pattern
matching was more accurate to the "human eye," and switched to Gestalt pattern
matching. It was then I realized the Python difflib module uses the same
process; albiet slightly modified for speed.

For more information on string metrics:
https://en.wikipedia.org/wiki/String_metric
"""

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculates the Levenshtein distance between two strings, a common number
    used to calculate the difference between two strings. For more information:
    https://en.wikipedia.org/wiki/Levenshtein_distance

    s1: The first string
    s2: The second string

    returns: The Levenshtein distance
    """
    # Creates a "distance matrix," which stores the difference (or "distance")
    # between two strings.
    dist_matrix = [[col+row for col in range(len(s2)+1) if col == 0 or \
                    row == 0] for row in range(len(s1)+1)]

    # Traverses the distance matrix row by row from left to right, calculating
    # the difference between the two strings using the differences stored in the
    # matrix.
    for r in range(1, len(dist_matrix)):
        for c in range(1, len(dist_matrix[0])):
            x = min(dist_matrix[r-1][c-1],
                    dist_matrix[r-1][c],
                    dist_matrix[r][c-1])

            if (r-1 == c-1 or (len(s1) == r and len(s2) == c)) and \
                s1[r-1] == s2[c-1]:
                dist_matrix[r].append(x)
            else:
                dist_matrix[r].append(x+1)

    return dist_matrix[-1][-1]

def hamming_distance(s1: str, s2: str) -> int:
    """
    Calculates the Hamming distance between two strings of equal length. Similar
    to the Levenshtein distance, the number can be used to calculate the
    difference between two strings. For more information:
    https://en.wikipedia.org/wiki/Hamming_distance

    s1: The first string
    s2: The second string
    
    returns: The Hamming distance
    """
    if len(s1) != len(s2):
        raise Exception("Strings must be of equal length when calculating Hamming distance!")

    distance = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            distance += 1
    return distance

def edit_distance(s1: str, s2: str) -> int:
    """
    Utilizing both Levenshtein and Hamming distance, calculate an edit distance
    between two strings.

    s1: The first string
    s2: The second string

    return: The edit distance between two strings.
    """
    if len(s1) == 0 or len(s2) == 0:
        return 0

    # The Hamming distance is faster to compute than the Levenshtein distance
    # when both strings are of the same length.
    if len(s1) == len(s2):
        return hamming_distance(s1, s2)
    return levenshtein_distance(s1, s2)

def longest_common_substring(s1: str, s2: str) -> str:
    """
    Finds the longest common substring between two strings, using a matrix and
    dynamic programming. For more information on the topic:
    https://en.wikipedia.org/wiki/Longest_common_substring_problem

    s1: The first string
    s2: The second string

    return: The longest common substring
    """
    x, y = 0, 0
    max_length = 0
    matrix = [[0] * (len(s2) + 1)]

    # Traverse the matrix row by row from left to right, calculating the longest
    # sequence of matching characters.
    for r in range(1, len(s1) + 1):
        matrix.append([])

        for c in range(len(s2) + 1):
            if s1[r-1] == s2[c-1] and c != 0:
                matrix[r].append(matrix[r-1][c-1] + 1)
            else:
                matrix[r].append(0)

            # If a new longest common substring is found, save the length of the
            # new substring and the coordinates of this value.
            if matrix[r][c] > max_length:
                x, y = r, c
                max_length = matrix[r][c]

    # Move backward through the matrix from the saved coordinates to form the
    # longest common substring.
    substring = ""
    while len(substring) != max_length:
        substring = s1[x-1] + substring
        x, y = x-1, y-1
    return substring

def gestalt_similarity(s1: str, s2: str) -> float:
    """
    Calculates a similarity rating between two strings based off of the Gestalt
    pattern matching algorithm. For more information:
    https://en.wikipedia.org/wiki/Gestalt_Pattern_Matching

    s1: The first string
    s2: The second string
    
    returns: A float value inbetween 0-1 that represents the similarity between
    the two strings. (A rating of 1 means the strings are identical, a rating of
    0 means the string do have any matching characters.)
    """
    if len(s1) == 0 or len(s2) == 0:
        return 0

    def count_matching_chars() -> int:
        """
        A recursive function that calculates the number of matching characters
        in a string, as well as the number of matching characters in the parts
        of the string that did not originally match.

        returns: The total number of matching characters in a string and in its nonmatching substrings.
        """
        count = 0
        substring = longest_common_substring(s1, s2)

        if len(substring) == 0:
            return count

        count += len(substring)
        s1, s2 = s1.replace(substring, " "), s2.replace(substring, " ")
        l = zip(s1.split(), s2.split())

        # Perform the same computation on the parts of the string that did not
        # match.
        for x, y in l:
            count += count_matching_chars(x, y)
        return count

    return 2 * count_matching_chars() / (len(s1) + len(s2))
