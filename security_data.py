"""
Nicholas Ly (lynichol@msu.edu)
ShellHacks 2022
September 11, 2022
"""

import constants as const

import csv      # Used to read and save information from asset files.
import difflib  # Used to compare and calculate the similarity between strings.
import time     # Used for seeing how long searches take.

class SecurityData:
    """
    A class which represents a large database of security identifiers.
    """

    def __init__(self):
        """
        Initalizes class by reading and saving all provided information from
        asset files.
        """
        self.data, self.priorities = None, None

        print("\nReading security data...")
        with open(const.PATH_SECURITIES, "r") as file:
            reader = csv.DictReader(file)
            self.data = [row for row in reader]

        print("Reading priority data...")
        with open(const.PATH_PRIORITIES, "r") as file:
            self.priorities = file.read().split()

    def get_search_results(self, query: str) -> list:
        """
        Given a query, creates a sorted copy of the database from most to least
        relevant/similar.

        query: A string used as the "search term."
        
        returns: A sorted list of tuples, containing the index of each security,
        its similarity to the query, and the street ID priority.
        """
        results = {}

        start = time.time()
        s = difflib.SequenceMatcher(a=query.lower())

        print("\nSearching through securities, please wait...")
        for index, security in enumerate(self.data):
            for street_id in security:

                # Skip computations that involve empty street IDs.
                if len(security[street_id]) > 0:
                    s.set_seq2(security[street_id].lower())
                    similarity = s.quick_ratio()

                    # Do not allow results to be overwritten unless they provide
                    # a security a higher similarity rating.
                    if index in results and results[index][0] > similarity:
                        continue

                    # Priority is based off position in list; higher number
                    # means higher priority.
                    priority = len(self.priorities) - self.priorities.index(street_id)

                    results[index] = (similarity, priority)

        t = round(time.time() - start, 3)
        print(f"{len(results)} securities sorted after: {t} seconds.\n")

        # Return search results as a list, sorting by priority and similarity.
        return sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    def refresh_priorities(self, p_index: int) -> None:
        """
        Refreshes priority order, moving the street ID of the specified index to
        the front of the list and updating the priority.txt file likewise.

        p_index: The index of the street ID to be moved.
        """
        p = self.priorities.pop(p_index)
        self.priorities.insert(0, p)

        with open(const.PATH_PRIORITIES, "w") as file:
            file.write("\n".join(self.priorities))
