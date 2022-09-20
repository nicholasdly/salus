
from security_tree import AVLTree
import constants

from difflib import SequenceMatcher 
from csv import DictReader
from time import time

### Current method of data retrieval is slow; takes between 60-90 seconds to process all data.

# TODO: Rather than keeping security and similarity data separate, keep security
# data inside of the security data. Balance the tree by similarity rating
# instead of index, and retrieve the right-most tree nodes for results.

class SISE:
    """
    Represents the Security Identifier Search Engine (SISE).
    """
    
    def __init__(self):
        """
        Initializes the search engine.
        """
        self.data = AVLTree()
        self.similarities = []
        self.priorities = []
        self.query = self.getQuery()

    def processData(self):
        """
        Reads all security and priority data, creates an AVL tree of the security data, and generates a list .
        """
        print("Reading priority data...")
        with open(constants.PATH_PRIORITIES, "r") as file:
            self.priorities = file.read().split()

        print("Reading security data...")
        with open(constants.PATH_SECURITIES, "r") as file:
            reader = DictReader(file)

            print("Processing data...")
            for index, row in enumerate(reader):

                # Inserts each financial security into the tree
                self.data.root = self.data.insert(self.data.root, index, row)

                # Calculates and saves highest similarity ratio
                self.similarities.append( (index, 0, None, None) )
                reviewer = SequenceMatcher(a=self.query)
                for key, value in row.items():
                    reviewer.set_seq2(value.lower())
                    ratio = reviewer.quick_ratio()
                    if ratio > self.similarities[index][1]:
                        self.similarities[index] = (index, ratio, key, value)
        
        # Sorts data by similarity ratio
        self.similarities = sorted(
            self.similarities,
            key=lambda x: x[1],
            reverse=True
        )

    def getQuery(self):
        """
        Retrieves search term from user input.
        """
        # TODO: Prompt user for input rather than using a hard-coded string.
        s = "FJUN"
        return s.lower()

    def getResults(self):
        """
        Returns most relevant securities (based on similarity ratio).
        """
        return self.similarities

def main():
    sise = SISE()

    start = time()
    sise.processData()
    results = sise.getResults()
    end = time()

    # # Prints top 10 results
    # for result in results[:10]:
    #     print(result)

    print(f"{len(results)} results in {round(end - start, 4)} seconds.")

if __name__ == "__main__":
    main()
