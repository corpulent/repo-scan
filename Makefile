ORGANIZATION = agolub
CONTAINER = repo-scan
VERSION = 1.0.0

build :
	docker build --rm -t $(ORGANIZATION)/$(CONTAINER):$(VERSION) .

run :
	docker run --rm --name $(CONTAINER) \
		-v ${PWD}/main.py:/srv/main.py \
		-v ${PWD}/reposcan:/srv/reposcan \
		-it $(ORGANIZATION)/$(CONTAINER):$(VERSION) \
			python /srv/main.py \
				-l 10 \
				-d 2021-01-01

init:
	pip install -r requirements.txt

test:
	py.test tests

.PHONY: init test