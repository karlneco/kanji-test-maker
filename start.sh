#!/bin/bash
app="kanji-test-maker"
docker build -t ${app} .
docker run -p 9473:9473 \
  --name=${app} \
  --env-file ~/kanji_test.env \
  -v $PWD/migrations:/app/migrations \
  -v $PWD/instance:/app/instance ${app}
