#!/usr/bin/env bash

cd tutorial/ && scrapyd
docker exec -dip 6800:6800 my_flask_app bash -c "cd tutorial/  && scrapyd"
