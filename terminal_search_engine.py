"""
Nicholas Ly (lynichol@msu.edu)
ShellHacks 2022
September 11, 2022
"""

from security_data import SecurityData
import constants as const

def main():
    securities = SecurityData()

    while True:
        query = input("\nSearch security identifiers or type \"quit\" to exit: ")
        if query.lower() == "quit":
            exit()

        results = securities.get_search_results(query)

        print("Most relevant results:\n")
        for i in range(const.RESULT_DISPLAY):
            ### print(f"{i+1}:  {results[i]}\n")
            print(f"{i+1}.  {securities.data[results[i][0]]}\n")

        selection = input("Select a security (1-5) or type anything else to quit: ")
        if not selection.isdigit() or int(selection) > 5 or int(selection) < 1:
            quit()
        
        # Calculates the index of the selected security's street ID in the
        # priority list.
        p_index = len(securities.priorities) - results[int(selection) - 1][1][1]

        securities.refresh_priorities(p_index)

if __name__ == "__main__":
    main()
