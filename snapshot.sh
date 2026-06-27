#!/bin/bash
# Run before every risky change — pass a label as argument
# Usage: bash snapshot.sh "before changing hero function"
cd /home/chubert/omni-builder/sites/site_NV
LABEL=${1:-"snapshot"}
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
SNAPSHOT_DIR="snapshots/${TIMESTAMP}_${LABEL// /_}"
mkdir -p "$SNAPSHOT_DIR/data"
mkdir -p "$SNAPSHOT_DIR/assets/images"
mkdir -p "$SNAPSHOT_DIR/theme"
cp build.py "$SNAPSHOT_DIR/"
cp theme/base.html "$SNAPSHOT_DIR/theme/"
cp data/pages.json "$SNAPSHOT_DIR/data/"
cp Master_Report.json "$SNAPSHOT_DIR/"
cp assets/images/*.webp "$SNAPSHOT_DIR/assets/images/" 2>/dev/null || true
echo "SNAPSHOT SAVED: $SNAPSHOT_DIR"
echo "TO RESTORE: bash restore.sh $SNAPSHOT_DIR"
