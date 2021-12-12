package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func readToArrays(path string) ([]string, []int, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, nil, err
	}
	defer file.Close()

	var cmds []string
	var values []int
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		s := strings.Split(scanner.Text(), " ")
		i, err := strconv.Atoi(s[1])
		if err != nil {
			panic(err)
		}
		cmds = append(cmds, s[0])
		values = append(values, i)
	}
	return cmds, values, scanner.Err()
}

func parseCmd(cmd string, value int, depth int, x int, y int) (int, int, int) {
	switch cmd {
	case "forward":
		x += value
		depth += y * value
	case "up":
		y -= value
	case "down":
		y += value
	default:
		panic("unknown command")
	}
	return depth, x, y
}

func main() {
	cmds, values, err := readToArrays("input.txt")
	if err != nil {
		panic(err)
	}

	var depth int
	var x int
	var y int
	for i := 0; i < len(cmds); i++ {
		depth, x, y = parseCmd(cmds[i], values[i], depth, x, y)
	}

	score := x * y
	fmt.Printf("Part 1: position (%d, %d), score=%d\n", x, y, score)

	score = x * depth
	fmt.Printf("Part 2: position (%d, %d, %d), score=%d\n", depth, x, y, score)
}
