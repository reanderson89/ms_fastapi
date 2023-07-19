#!/usr/bin/env bash

DIRS=(
    app/models
    app/actions
    app/routers
)

# these are easy fixes
AUTO_FIX=(
    F401       # remove unused imports
    UP039      # parentheses after class definition
    Q002       # single quote docstring
    E401       # multiple imports on one line
    F841       # unused variables
)

for DIR in "${DIRS[@]}"
do
    for RULE in "${AUTO_FIX[@]}"
    do
        echo "Linting ${DIR} with ruff rule ${RULE}"
        ruff check ${DIR} --select ${RULE} --fix
    done
done

echo "Git commit message:  Linting fixups for: unused imports, parentheses after class definition, single quote docstring, multiple imports on one line and unused variables"