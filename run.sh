#!/bin/bash
source env/bin/activate
which python
gunicorn main:app -b 127.0.0.1:5000 -w 6 --log-file -
