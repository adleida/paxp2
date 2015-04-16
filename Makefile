.PHONY: test run wsgi deploy upload build

all: clean test

test:
	py.test

run:
	python paxp2/cli.py -c paxp2/res/config.yaml

wsgi:
	uwsgi paxp2.ini

clean:
	rm -rf paxp2.egg-info .tox dist
	find . -name '*.pyc' -delete
	find . -name '.*~' -delete
	find . -name '__pycache__' -delete

build:
	python setup.py sdist

upload:
	scp dist/*.gz 119:/tmp

deploy:
	echo deploy

