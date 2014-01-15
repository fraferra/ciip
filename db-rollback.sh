#!/bin/bash
dropdb local100
createdb local100
pg_restore --verbose --clean --no-acl --no-owner -d local100 b013.dump
python manage.py syncdb
./manage.py migrate ciip 0001 --fake
python manage.py migrate ciip
