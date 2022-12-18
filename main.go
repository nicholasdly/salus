package main

import (
	"fmt"
	"encoding/csv"
	"log"
	"os"
	"strings"
	"sort"
)

//
// Given two integers as input, return the larger of the two integers.
//
func maxInt(a int, b int) int {
	if a < b {
		return b
	}
	return a
}

//
// Given two strings as input, return the length of their longest common substring.
//
func relation(query string, identifier string) int {
	m := len(query)
	n := len(identifier)
	result := 0

	// Create dynamic programming matrix to store common substring computations
	matrix := make([][]int, m+1)
	for i := 0; i < m+1; i++ {
		matrix[i] = make([]int, n+1)
	}

	// Computes all common substring lengths; most recent largest being the longest
	for i := 0; i <= m; i++ {
		for j := 0; j <= n; j++ {
			if i == 0 || j == 0 {
				matrix[i][j] = 0
			} else if query[i - 1] == identifier[j - 1] {
				matrix[i][j] = matrix[i-1][j-1] + 1
				result = maxInt(result, matrix[i][j])
			} else {
				matrix[i][j] = 0
			}
		}
	}

	return result
}

func main() {
	// Opens the CSV file
	file, err := os.Open("data/securities.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Reads the CSV
	fmt.Printf("Reading financial security data from CSV file... ")
	csvReader := csv.NewReader(file)
	data, err := csvReader.ReadAll()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Done.\n")

	// Prompt user for search query
	var query string
	fmt.Printf("Enter search query :: ")
	fmt.Scanln(&query)
	fmt.Println()

	// Processes security relation data
	fmt.Printf("Searching through %v securities... ", len(data[1:]))
	relations := make(map[int]int)
	keys := make([]int, len(relations))
	for i, line := range data {
		if i > 0 {
			identifier := strings.Join(line, "")
			keys = append(keys, i)
			relations[i] = relation(query, identifier)
		}
	}
	fmt.Println("Done.")

	// Sort security relation data
	fmt.Printf("Sorting %v securities... ", len(relations))
	sort.SliceStable(keys, func(i int, j int) bool {
		return relations[keys[i]] > relations[keys[j]]
	})
	fmt.Println("Done.\n")
	
	// Print top 5 results
	for _, key := range keys[:5] {
		fmt.Printf("Record #%v", key)
		fmt.Printf(", %v matching characters:\n", relations[key])
		fmt.Printf("%v\n\n", data[key])
	}
}
