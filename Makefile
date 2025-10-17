PY=python

.PHONY: train deploy clean

train:
	$(PY) -m blocksmith.train

deploy:
	$(PY) -m blocksmith.deploy

clean:
	rm -f blocksmith_mlp.joblib
	rm -rf __pycache__ blocksmith/__pycache__
