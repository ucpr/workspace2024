package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"go.uber.org/mock/gomock"

	mock "github.com/ucpr/workspace2024/gomock-generics-test/mock"
)

func TestExampleServiceWithGenerics(t *testing.T) {
	ctrl := gomock.NewController(t)
	mockService := mock.NewMockExampleService[int](ctrl)

	mockService.EXPECT().Process(10).Return(20)
	result := mockService.Process(10)
	assert.Equal(t, 20, result)
}
