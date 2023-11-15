#!/bin/bash -x

# directory/directories where the auto-linting will be executed
SRC_DIRS=${1:-"automation_svc_ui"}
echo "Running auto-linting for source code in ${SRC_DIRS}."
echo "NOTE: Code duplication issues canot be fixed by auto linting."

for src_dir in ${SRC_DIRS}
do
    [[ ! -d ./${src_dir} ]] \
        && echo "Running lint fix with incorrect directory context. Directory ${src_dir} not present" \
        && exit 1
done

mypy ${SRC_DIRS} --ignore-missing-imports
echo "Done with mypy"

autoflake \
    --remove-all-unused-imports \
    --recursive \
    --remove-unused-variables \
    --in-place \
    --exclude=__init__.py \
    ${SRC_DIRS}
echo "Done with autoflake"

black ${SRC_DIRS} --line-length 90
echo "Done with black"

isort ${SRC_DIRS} -l 90 -m 3 --up
echo "Done with isort"
