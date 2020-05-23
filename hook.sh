#!/bin/bash

WORK_DIR=$( basename "${BASH_SOURCE[0]}" )

pushd "${WORK_DIR}"

pipenv run python hook.py "${@}"
