PY=python

.PHONY: test type lint train deploy clean dashboard

test:
	pytest -q

type:
	mypy blocksmith

lint:
	ruff check .

train:
	$(PY) -m blocksmith.train

deploy:
	$(PY) -m blocksmith.deploy --dry --shape hollow_box --w 8 --d 8 --h 4

dashboard:
	streamlit run dashboard/app.py

clean:
	rm -f blocksmith_mlp.joblib
	rm -rf __pycache__ blocksmith/__pycache__ .pytest_cache .mypy_cache
