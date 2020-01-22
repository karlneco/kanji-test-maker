#!/bin/bash
app="hktm"
docker build -t ${app} .
docker run -d -p 10475:80 \
  --name=${app} \
  -v $PWD ${app}
