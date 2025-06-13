#!/bin/bash
set -e  # stop on first error

echo "Running Python tests with pytest..."
pytest --cov=burger

echo "Running Rust tests with cargo..."
cargo test

echo "All tests completed successfully!"
