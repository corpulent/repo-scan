ORGANIZATION = agolub
CONTAINER = repo-scan
VERSION = 1.0.0

build:
	docker build --rm -t $(ORGANIZATION)/$(CONTAINER):$(VERSION) .

run:
	docker run --rm --name $(CONTAINER) \
		-v ${PWD}/main.py:/srv/main.py \
		-v ${PWD}/repos:/srv/src/repos \
		-v ${PWD}/reposcan:/srv/reposcan \
		-it $(ORGANIZATION)/$(CONTAINER):$(VERSION) \
			python3 /srv/main.py \
				-l 3 \
				-d 2021-01-01 \
				-s true

init:
	pip install -r requirements.txt

test:
	py.test tests

.PHONY: init test build run