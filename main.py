"""
Nicholas Ly (lynichol@msu.edu)
ShellHacks 2022
September 11, 2022
"""

from security_data import SecurityData
import constants as const

import time  # Used for seeing how long searches take.

def main():
    data = SecurityData()
    query = input("Search security identifiers: ")

    start = time.time()
    results = data.get_search_results(query)
    t = round(time.time() - start, 3)
    print(f"{len(results)} securities sorted after: {t} seconds.\n")

    print("Most relevant results:\n")
    for result in results[:const.RESULT_DISPLAY]:
        ### print(result)
        print(f"{data.data[result[0]]}\n")

if __name__ == "__main__":
    main()
