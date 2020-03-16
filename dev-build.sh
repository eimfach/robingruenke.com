#!/bin/bash

rm -rf stylesheets/inline/critical
mkdir stylesheets/inline/critical

pipenv run python compile.py

node build-critical-css.js

echo '------> Rerun .journal complilation to include inline css'
pipenv run python compile.py