.PHONY: all results charts check

all: results charts

results:
	python3 analysis.py

charts:
	python3 generate_charts.py

check: all
	git diff --exit-code -- results charts
