"""
Nicholas Ly (lynichol@msu.edu)
ShellHacks 2022
September 11, 2022
"""

import constants as const

import csv      # Used to read and save information from asset files.
import difflib  # Used to compare and calculate the similarity between strings.

class SecurityData:
    """
    A class which represents a large database of security identifiers.
    """

    def __init__(self):
        """
        Initalizes class by reading and saving all provided information by asset
        files.
        """
        self.data, self.priorities = None, None

        # Save all securities as a list of dictionaries, each dictionary being a
        # security.
        print("\nReading security data...")
        with open(const.PATH_SECURITIES) as file:
            reader = csv.DictReader(file)
            self.data = [row for row in reader]

        # Save street ID priority list.
        print("Reading priority data...\n")
        with open(const.PATH_PRIORITIES) as file:
            reader = csv.reader(file)
            self.priorities = [row[0] for row in reader]

    def get_search_results(self, query):
        """
        Given a query, creates a sorted copy of the database from most to least
        relevant/similar.

        query: A string used as the "search term."
        
        returns: A sorted list of tuples, containing the index of each security,
        its similarity to the query, and the street ID priority.
        """
        results = {}  # Search results are saved in a dictionary for speed.
        
        s = difflib.SequenceMatcher(a=query.lower())

        # Iterate through all securities and their street IDs.
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

        # Return search results as a list, sorting by priority and similarity
        # to the query.
        return sorted(results.items(), key=lambda x: x[1], reverse=True)
    