#!/usr/bin/env bash

curl -o $HOME/google_appengine_1.9.22.zip https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.22.zip
unzip -q -d $HOME $HOME/google_appengine_1.9.22.zip
python test_runner.py $HOME/google_appengine
