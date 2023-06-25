#!/usr/bin/env bash
if [ "$RUN_TESTS" = "True" ]
  then
  uvicorn --host 0.0.0.0 --port 8080 sources.main:application & sleep 3; pytest
else
  uvicorn --host 0.0.0.0 --port 8080 sources.main:application
fi