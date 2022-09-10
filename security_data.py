import csv
import string_similarity

class SecurityData:
    """
    """

    def __init__(self):
        """
        """
        # Save street ID priority order (lower index, higher priority).
        self.priorities = []
        with open("assets/priorities.csv") as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                self.priorities.append((index, row[0]))

        # Save all securities in a list of dictionaries, keyed by security ID.
        self.data = []
        with open("assets/securities_small.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.data.append(row)

    def __repr__(self):
        """
        """
        return str(self.data)

    def __str__(self):
        """
        """
        return "[" + ",\n".join([str(security) for security in self]) + "]"

    def __iter__(self):
        """
        """
        for security in self.data:
            yield security

    def __getitem__(self, index):
        """
        """
        return self.data[index]

    def search(self, query):
        """
        """
        results = {}
        for index, security in enumerate(self):
            for id in security.values():
                if len(id) > 0:
                    score = string_similarity.sequence_similarity(query, id)
                    if index in results and results[index] > score:
                        continue
                    results[index] = score

        return sorted(results.items(), key=lambda x: x[1], reverse=True)
    