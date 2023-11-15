#!/usr/bin/env bash

set -e
set -x
mypy scripts --ignore-missing-imports
black automation --line-length 90
isort --recursive automation -l 90 -m 3 --up
