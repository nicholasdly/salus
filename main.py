from security_data import SecurityData

import time

def main():
    data = SecurityData()
    
    query = input("Search financial securities: ")

    start = time.time()
    results = data.get_search_results(query)
    t = round(time.time() - start, 3)
    print(f"{len(results)} securities sorted after: {t} seconds.\n")

    print("Top 5 results:")
    for result in results[:10]:
        print(result)
        print(data.data[result[0]])

if __name__ == "__main__":
    main()
