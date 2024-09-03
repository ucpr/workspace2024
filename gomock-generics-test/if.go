package main

// ExampleService is a generic interface
type ExampleService[T any] interface {
	Process(input T) T
}
