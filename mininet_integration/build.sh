#!/bin/bash
rm -rf dist

mkdir dist
cp -R ../controllers ./dist
cp -R ../gym_envs ./dist
cp -R ../utils ./dist

mkdir dist/data
cp -R ./data ./dist

cp ../Pipfile ./dist
cp ./*.py ./dist
cp ./deploy.sh ./dist

pipenv run 3to2 dist -w

rm -rf ../scripts/dist
cp -R dist ../scripts


