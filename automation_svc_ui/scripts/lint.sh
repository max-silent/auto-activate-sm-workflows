#!/usr/bin/env bash

set -e
set -x
mypy scripts --ignore-missing-imports
black automation
isort --recursive automation
