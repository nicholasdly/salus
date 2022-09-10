"""
Nicholas Ly
ShellHacks 2022
Schonfeld Street ID Challenge
"""

import csv
import time

# TODO: Make search engine into a class!

def get_levenshtein_distance(s1: str, s2: str) -> int:
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

def get_hamming_distance(s1: str, s2: str) -> int:
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

def search(data: list, priorities: list, query: str) -> list:
    """
    Sorts the dataset by relevance to query.

    data: The complete dataset list of dictionaries
    priorities: The street ID order of priority
    query: The user input search term

    returns: A list of tuples containing security ID, difference from query, and
    level of priority, sorted by relevance to the query
    """
    results = {}

    # TODO: "results" start as dictionary but leave function as list?
    # TODO: Existence of both "priorities" and "p" seems repetitive.

    # Traverse dataset by street ID from highest to lowest priority.
    for p in range(len(priorities) - 9):  # TODO: Don't forget to remove the '- 9'!
        for security in data:
            security_id = security["security_id"]
            street_id = security[priorities[p]]

            # Because the Hamming distance calculation is faster, prefer that
            # when possible (strings are of same length).
            if len(query) == len(street_id):
                dist = get_hamming_distance(query, street_id)
            else:
                dist = get_levenshtein_distance(query, street_id)

            # If a security has already been recorded, check if its different
            # street ID has causes an increase in relevance.
            if security_id in results:
                if dist > results[security_id][0] or (dist == results[security_id][0] and p > results[security_id][1]):
                    continue
            
            results[security_id] = (dist, p)

    return sorted(results.items(), key=lambda tup: tup[1])

def main():
    """
    The main function of the search engine.
    """
    # Save street ID priority order (lower index, higher priority).
    priorities = []
    with open("assets/priorities.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            priorities.append(row[0])

    # Save all securities in a list of dictionaries, keyed by security ID.
    data = []
    with open("assets/securities_small.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    query = input("Search financial securities: ")
    start = time.time()

    # Save all search results in a list of tuples, containing their security ID,
    # difference from query, and level of priority.
    results = search(data, priorities, query)
    end = time.time()

    print(f"({round(end-start, 2)} seconds)\n")
    for i in range(5):
        print(results[i][0])
    
    expand = input("\nExpand for more results? (y/n) ")

    if expand.lower() == "y":
        print()
        for i in range(5, 25):
            print(results[i][0])


if __name__ == "__main__":
    main()