.PHONY: metrics
metrics:
	go run github.com/open-telemetry/opentelemetry-collector-contrib/cmd/telemetrygen@latest metrics --duration 5s --otlp-insecure

.PHONY: traces
traces:
	go run github.com/open-telemetry/opentelemetry-collector-contrib/cmd/telemetrygen@latest traces --otlp-insecure --duration 5s

.PHONY: logs
logs:
	go run github.com/open-telemetry/opentelemetry-collector-contrib/cmd/telemetrygen@latest logs --otlp-insecure --duration 5s

.PHONY: start-collector
start-collector:
	docker run -p 4317:4317 -v $$(pwd)/config.yaml:/etc/otelcol-contrib/config.yaml ghcr.io/open-telemetry/opentelemetry-collector-releases/opentelemetry-collector-contrib
