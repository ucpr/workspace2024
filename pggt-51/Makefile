GO ?= go
BIN := $(abspath ./bin)

$(BIN)/buf:
	GOBIN=$(BIN) go install github.com/bufbuild/buf/cmd/buf@latest

$(BIN)/protoc-gen-go:
	GOBIN=$(BIN) go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

.PHONY: proto
proto: $(BIN)/buf $(BIN)/protoc-gen-go
	rm -rf gen && $(BIN)/buf generate && $(BIN)/buf generate --template ./buf.gen.tag.yaml
