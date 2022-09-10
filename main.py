from security_data import SecurityData

import time

def main():
    data = SecurityData()
    
    query = input("Search financial securities: ")

    start = time.time()
    results = data.search(query)
    t = round(time.time() - start, 3)
    print(f"{len(results)} securities sorted after: {t} seconds.\n")

    print("Top 5 results:")
    for result in results[:5]:
        print(data[result[0]])

    expand = input("\nExpand for more securities? (y/n) ")
    if expand.lower() == "y":
        count = input("How many? ")
        for result in results[5:count]:
            print(data[result[0]])

if __name__ == "__main__":
    main()
