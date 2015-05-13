.PHONY: test run wsgi deploy upload build

PKG = $(shell python setup.py --fullname).tar.gz
HOSTS = python@114 ubuntu@ucloud
DIR = .

all: clean test

test:
	py.test

run:
	python paxp2/cli.py -c paxp2/res/paxp2.yaml

wsgi:
	uwsgi --yaml paxp2/res/uwsgi.yaml

clean:
	rm -rf paxp2.egg-info .tox dist
	find . -name '*.pyc' -delete
	find . -name '.*~' -delete
	find . -name '__pycache__' -delete
	find . -name '*.log' -delete

pack: clean
	python setup.py sdist --formats=gztar

upload: pack
	for HOST in $(HOSTS); \
	do \
	    ssh $$HOST 'mkdir -p $(DIR)'; \
	    scp dist/$(PKG) $$HOST:$(DIR); \
	    ssh $$HOST 'ln -sf $(DIR)/$(PKG) $(DIR)/paxp2-latest.tar.gz'; \
	done

deploy: upload
	ssh 119 "sudo pip install $(DIR)/$(PKG)"

