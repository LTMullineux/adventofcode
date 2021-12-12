package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func readToArray(path string) ([]int, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []int
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		s := scanner.Text()
		i, err := strconv.Atoi(s)
		if err != nil {
			panic(err)
		}
		lines = append(lines, i)
	}
	return lines, scanner.Err()
}

func sum(seq []int) int {
	var result int
	for _, i := range seq {
		result += i
	}
	return result
}

func windowSum(seq []int, n int) []int {
	var result []int
	for i := 0; i < len(seq)-n+1; i++ {
		window_sum := sum(seq[i : i+n])
		result = append(result, window_sum)
	}
	return result
}

func countIncreases(seq []int) int {
	var result int
	for i := 1; i < len(seq); i++ {
		if seq[i] > seq[i-1] {
			result++
		}
	}
	return result
}

func main() {
	lines, err := readToArray("input.txt")
	if err != nil {
		panic(err)
	}

	// n := 1
	sums := windowSum(lines, 1)
	increases := countIncreases(sums)
	fmt.Printf("Part 1: %d\n", increases)

	// n := 3
	sums = windowSum(lines, 3)
	increases = countIncreases(sums)
	fmt.Printf("Part 1: %d\n", increases)
}
