.PHONY: train run test lint clean

train:
	python train.py

run:
	sudo venv/bin/python ids.py

run-count:
	sudo venv/bin/python ids.py --count 100

test:
	python -m pytest tests/ -v

lint:
	python -m py_compile src/capture.py src/features.py src/detector.py src/alerter.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
