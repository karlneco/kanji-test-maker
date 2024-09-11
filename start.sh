#!/bin/bash
app="kanji-test-maker"
docker build -t ${app} .
docker run -p 7953:7953 \
  --name=${app} \
  --env-file ~/kanji_test.env \
  -v $PWD/migrations:/app/migrations \
  -v $PWD/instance:/app/instance ${app}
