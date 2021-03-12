# Repos scan

Fetch public trending GitHub repos by date and language,  run a quick dependency check, and give each one a score (naive).  Work in progress.

Python 3.4 and up.

## Env

```shell script
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

Using Makefile

```
make init
make test
make run
```

Run the script directly

```
python main.py -l 10 -d 2021-01-01
```

Simple backend job runner.

<img width="529" alt="Screen Shot 2021-03-12 at 4 21 01 PM" src="https://user-images.githubusercontent.com/849403/110999863-0c7b6300-834f-11eb-935f-ed92732c29fe.png">
