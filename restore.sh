#!/bin/bash
# Usage: bash restore.sh snapshots/TIMESTAMP_label
cd /home/chubert/omni-builder/sites/site_NV
SNAPSHOT_DIR=$1
if [ -z "$SNAPSHOT_DIR" ] || [ ! -d "$SNAPSHOT_DIR" ]; then
    echo "ERROR: provide a valid snapshot directory"
    echo "Available snapshots:"
    ls snapshots/
    exit 1
fi
cp "$SNAPSHOT_DIR/build.py" build.py
cp "$SNAPSHOT_DIR/theme/base.html" theme/base.html
cp "$SNAPSHOT_DIR/data/pages.json" data/pages.json
cp "$SNAPSHOT_DIR/Master_Report.json" Master_Report.json
cp "$SNAPSHOT_DIR/assets/images/"*.webp assets/images/ 2>/dev/null || true
echo "RESTORED FROM: $SNAPSHOT_DIR"
echo "Run python3 build.py to rebuild"
