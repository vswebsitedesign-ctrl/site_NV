#!/bin/bash
# Run this at the start of every AI session — before any changes
cd /home/chubert/omni-builder/sites/site_NV
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H%M')
BRANCH="session-$DATE-$TIME"
git checkout -b "$BRANCH"
echo "BRANCH CREATED: $BRANCH"
echo "If this session goes wrong: git checkout main && git branch -D $BRANCH"
