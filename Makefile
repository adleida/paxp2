run:
	python paxp2/cli.py -c paxp2/res/config.yaml

wsgi:
	uwsgi paxp2.ini

clean:
	rm -rf paxp2.egg-info .tox
