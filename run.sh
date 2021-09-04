#!/bin/bash

# flask settings
export FLASK_APP=run.py
export FLASK_DEBUG=0

flask run --host=0.0.0.0 --port=8082
