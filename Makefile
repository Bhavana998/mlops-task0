.PHONY: run docker-build docker-run clean

# Run locally
run:
	python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

# Build Docker image
docker-build:
	docker build -t mlops-task .

# Run Docker container
docker-run: docker-build
	docker run --rm mlops-task

# Extract output files from container (useful for testing)
docker-extract: docker-build
	docker run --rm -v $(PWD):/out mlops-task bash -c "cp metrics.json run.log /out/"

# Clean up generated files
clean:
	rm -f metrics.json run.log
	rm -rf __pycache__

# Format code with black
format:
	black run.py

# Check code with black (dry run)
check-format:
	black --check run.py