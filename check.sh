#!/usr/bin/env bash
# Script to run static analysis checks on Python sources
# usage to check files:
# ./check


SOURCES="**/*.py"

command_exists() {
    type "$1" &>/dev/null ;
}

execute() {
    if command_exists $1 ; then
        echo "Executing $1..."
        $1 $SOURCES
    else
        echo "Skipping $1 (not installed)."
    fi
}

execute_vulture() {
    if command_exists vulture ; then
        echo "Executing vulture..."
        vulture $SOURCES whitelist.py
    else
        echo "Skipping vulture (not installed)."
    fi
}

execute_pep8() {
    if command_exists pep8 ; then
        echo "Executing pep8..."
        pep8 --ignore=E402 $SOURCES
    else
        echo "Skipping pep8 (not installed)."
    fi
}

execute_pyflakes() {
    if command_exists pyflakes ; then
        echo "Executing pyflakes..."
        pyflakes $SOURCES
    else
        echo "Skipping pyflakes (not installed)."
    fi
}

execute_pylint() {
    if command_exists pylint ; then
        echo "Executing pylint..."
        pylint $SOURCES
    else
        echo "Skipping pylint (not installed)."
    fi
}

execute_vulture
execute_pyflakes
execute_pep8
execute_pylint