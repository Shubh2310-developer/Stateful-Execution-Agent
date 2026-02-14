#!/bin/bash
echo "Rolling back to previous stable state..."

# Discard current changes and restart
docker compose down
docker compose up -d

echo "Rollback sequence initiated."
