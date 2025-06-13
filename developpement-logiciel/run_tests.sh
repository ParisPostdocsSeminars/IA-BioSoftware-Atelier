#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "Running tests with coverage..."

pytest --cov=burger --cov-report=term-missing

echo "Tests and coverage report completed."
