#! /bin/sh
rm -r dist
mkdir dist/
python3 setup.py bdist_egg
ls -l dist/
cp -r dist/* SPARK_DOCKER/marlabs_bi_jobs-0.0.0-py3.6.egg
ls -l SPARK_DOCKER/

