run:
	python paxp2/cli.py

wsgi:
	uwsgi paxp2.ini

clean:
	rm -rf paxp2.egg-info .tox
