#!/bin/bash

WORK_DIR=$( dirname "${BASH_SOURCE[0]}" )

pushd "${WORK_DIR}"

pipenv run python hook.py "${@}"
