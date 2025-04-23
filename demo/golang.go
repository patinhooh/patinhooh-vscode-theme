// main.go
package main

import (
	"fmt"
	"math"
	"strings"
	"time"
)

// Constants
const Pi = 3.14
const untyped = "untyped constant"

// Variables
var globalVar = "I'm global"

type Person struct {
	Name string
	Age  int
}

type Greeter interface {
	Greet() string
}

func (p Person) Greet() string {
	return fmt.Sprintf("Hi, my name is %s and I'm %d years old.", p.Name, p.Age)
}

// Function with multiple return values
func divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, fmt.Errorf("division by zero")
	}
	return a / b, nil
}

func pointerDemo(ptr *int) {
	*ptr += 1
}

func arraySliceMapDemo() {
	// Array
	var arr = [3]int{1, 2, 3}
	fmt.Println("Array:", arr)

	// Slice
	slice := []string{"a", "b", "c"}
	slice = append(slice, "d")
	fmt.Println("Slice:", slice)

	// Map
	m := map[string]int{"foo": 1, "bar": 2}
	m["baz"] = 3
	delete(m, "bar")
	for k, v := range m {
		fmt.Printf("Map Key: %s, Value: %d\n", k, v)
	}
}

func concurrencyDemo() {
	c := make(chan string)

	go func(msg string) {
		c <- msg
	}("Hello from goroutine!")

	message := <-c
	fmt.Println(message)
}

func main() {
	// Short variable declaration
	x := 10
	y := 20.5
	name := "GoLang"

	// If-else
	if x > 5 {
		fmt.Println("x is greater than 5")
	} else {
		fmt.Println("x is 5 or less")
	}

	// Switch
	switch name {
	case "GoLang":
		fmt.Println("You are using Go!")
	default:
		fmt.Println("Unknown language")
	}

	// For loop
	for i := 0; i < 3; i++ {
		fmt.Println("Loop:", i)
	}

	// Defer
	defer fmt.Println("This runs last (defer demo)")

	// Type conversion
	var i int = int(y)
	fmt.Println("Converted float to int:", i)

	// Call functions
	res, err := divide(10, 2)
	if err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Println("Result of divide:", res)
	}

	// Structs and interfaces
	person := Person{Name: "Alice", Age: 30}
	fmt.Println(person.Greet())

	// Pointers
	num := 5
	pointerDemo(&num)
	fmt.Println("After pointerDemo:", num)

	// Arrays, slices, maps
	arraySliceMapDemo()

	// Goroutine and channels
	concurrencyDemo()

	// Using imported packages
	fmt.Println("Upper:", strings.ToUpper("hello"))
	fmt.Println("Cosine of Pi:", math.Cos(Pi))

	// Time formatting
	fmt.Println("Current time:", time.Now().Format(time.RFC1123))
}
