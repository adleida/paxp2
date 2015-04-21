.PHONY: test run wsgi deploy upload build

PKG=$(shell python setup.py --fullname).tar.gz
HOST=119
DIR=/tmp

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
	find . -name '*.log' -delete

pack: clean
	python setup.py sdist --formats=gztar

upload: pack
	scp dist/$(PKG) $(HOST):$(DIR)

deploy: upload
	ssh 119 "sudo pip install $(DIR)/$(PKG)"

