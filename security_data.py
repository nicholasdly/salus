import csv
import difflib

class SecurityData:
    """
    """

    def __init__(self):
        """
        """
        # Save street ID priority list.
        self.priorities = []
        with open("assets/priorities.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                self.priorities.append(row[0])

        # Save all securities as a list of dictionaries, each dictionary being a security.
        self.data = []
        with open("assets/securities.small.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.data.append(row)

    def get_search_results(self, query):
        """
        """
        results = {}
        s = difflib.SequenceMatcher(a=query.lower())

        for index, security in enumerate(self.data):
            for street_id in security:
                if len(security[street_id]) > 0:
                    s.set_seq2(security[street_id].lower())
                    similarity = s.quick_ratio()

                    priority = 11 - self.priorities.index(street_id)

                    if index in results and results[index][0] > similarity:
                        continue
                    results[index] = (similarity, priority)

        return sorted(results.items(), key=lambda x: x[1], reverse=True)
    