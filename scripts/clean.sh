#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT" || exit 1
echo "Cleaning up project at: $PROJECT_ROOT"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
[ -d "build" ] && rm -rf build && echo "Removed build/"
[ -d ".venv" ] && rm -rf .venv && echo "Removed .venv/"
[ -d "dist" ] && rm -rf dist && echo "Removed dist/"
[ -d ".pytest_cache" ] && rm -rf .pytest_cache && echo "Removed .pytest_cache/"

echo "Cleanup complete!"
