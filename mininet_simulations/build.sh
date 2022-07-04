#!/bin/bash
rm -rf dist
mkdir dist

cp -R ../controllers ../gym_envs ../utils ./data ../Pipfile ./**/*.py ./deploy.sh ./dist

pipenv run 3to2 dist -w -n --no-diffs

rm -rf ../scripts/dist
cp -R dist ../scripts


