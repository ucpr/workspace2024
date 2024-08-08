package main

import (
	"context"
	"log"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp"
	"go.opentelemetry.io/otel/sdk/metric"
)

const meterName = "github.com/ucpr/workspace2024/tlgen/app"

func main() {
	ctx := context.Background()

	exporter, err := otlpmetrichttp.New(
		ctx,
		otlpmetrichttp.WithEndpoint("localhost:4318"),
		otlpmetrichttp.WithInsecure(),
	)
	if err != nil {
		log.Fatalf("Failed to create the collector exporter: %v", err)
	}

	meterProvider := metric.NewMeterProvider(metric.WithReader(
		metric.NewPeriodicReader(exporter, metric.WithInterval(5*time.Second)),
	))
	defer meterProvider.Shutdown(ctx)
	otel.SetMeterProvider(meterProvider)

	meter := otel.Meter(meterName)
	counter, err := meter.Int64Counter("counter")
	if err != nil {
		log.Fatalln(err)
	}

	for {
		counter.Add(ctx, 1)
		log.Println("counter incremented")
		time.Sleep(1 * time.Second)
	}
}
