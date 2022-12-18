
# Used for CSV file processing and data representation; along with pyarrow,
# pandas can read a CSV file much faster than Python's built in csv module.
import pandas as pd

# Used for longest common substring computation; pylcs is powered by C++ and
# therefore much faster than any individually written script or built-in
# Python module.
import pylcs

class Salus:
    """
    Represents the Salus financial security identifier search engine.
    """

    def __init__(self) -> None:
        """
        Initializes the Salus financial security identifier search engine.
        """
        self._data = None  # The financial security dataframe

    def read(self, filename: str) -> None:
        """
        Reads a given CSV file using pandas and pyarrow, creating the
        financial security dataframe, and generates a simplified vector
        space model for each financial security.

        filename -- string: Filepath of CSV
        """
        self._data = pd.read_csv(
            filename,
            keep_default_na=False,
            engine='pyarrow'
        )
        self._data['vsm'] = self._data.astype(str).values.sum(axis=1)

    def query(self, term: str, results: int = 1) -> list[pd.Series]:
        """
        Queries the financial security dataframe for the most relevant
        financial securities based off of longest common substring to a
        specified search term.

        term -- string: Search term
        results -- int (default=1): Maximum length of list of query results 

        returns -> list: List of most relevant financial securities as pandas series
        """
        # Must have read a CSV file before querying
        if self._data is None:
            raise AttributeError('Salus must read a CSV file before querying!')
        
        indices = []
        for index, vsm in enumerate(self._data['vsm']):
            score = pylcs.lcs_string_length(term, vsm)
            indices.append( (score, index) )
        indices.sort()
        return [ self._data.iloc[indices[-i-1][1]] for i in range(min(results, len(indices))) ]

def main():
    salus = Salus()
    salus.read('data/securities.csv')
    results = salus.query('FJUN')
    
    for series in results:
        print(series.values)

if __name__ == "__main__":
    main()
