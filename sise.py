
PATH_SECURITIES = "assets/securities.csv"
PATH_PRIORITIES = "assets/priorities.txt"

class SISE:
    """
    Represents the Security Identifier Search Engine.
    """

    def __init__(self, container):
        """
        Initializes SISE by reading and storing all financial security data.
        """
        self.container = container
        self.columns = []
        self.data = []

        # Reads financial security data from file
        with open(PATH_SECURITIES) as database:
            self.columns = database.readline()[:-1].split(',')
            self.data = [row[:-1] for row in database]

    def __lcs(self, s1: str, s2: str) -> int:
        """
        Finds the length of the longest common substring between two strings,
        using dynamic programming.

        s1: The first string
        s2: The second string

        return: The length of the longest common substring
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

        return max_length

    def get_raw_relevancy(self, query):
        """
        Returns sorted relevancy data based off of longest common substring
        (LCS), in a list of tuples containing the length of the LCS and the
        index of the security.

        query: The search term string

        return: The sorted relevancy data list
        """
        results = []
        for index, security in enumerate(self.data):
            lcs = self.__lcs(query.lower(), str(security).lower())
            results.append((lcs, index))
        return sorted(results, reverse=True)

    # def processData(self):
    #     results = pd.DataFrame(
    #         [row.split(',') for row in self.get_results()],
    #         columns=self.columns
    #     )
    #     return results
