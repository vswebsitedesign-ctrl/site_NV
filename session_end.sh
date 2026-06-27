#!/bin/bash
# Run at end of every successful session
cd /home/chubert/omni-builder/sites/site_NV
CURRENT_BRANCH=$(git branch --show-current)
git add -A
git commit -m "session: $(date '+%Y-%m-%d %H:%M') — $1"
git checkout main
git merge "$CURRENT_BRANCH"
git push origin main
git branch -D "$CURRENT_BRANCH"
if [ -d "snapshots" ]; then
    rm -rf snapshots/
    echo "SNAPSHOTS CLEANED"
fi
echo "PUSHED TO GITHUB — SESSION COMPLETE"
echo "Branch $CURRENT_BRANCH merged and deleted"
