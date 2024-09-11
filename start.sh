#!/bin/bash
app="kanji-test-maker"
docker build -t ${app} .
docker run -d -p 9473:80 \
  --name=${app} \
  --env-file ~/kanji_test.env \
  -v $PWD/migrations:/app/migrations \
  -v $PWD/instance:/app/instance ${app}
