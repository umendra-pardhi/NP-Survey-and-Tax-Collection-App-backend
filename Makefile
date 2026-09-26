.PHONY: run dev install test clean

HOST=0.0.0.0
PORT=8000

dev:
	uvicorn app.main:app --host $(HOST) --port $(PORT) --reload

run:
	uvicorn app.main:app --host $(HOST) --port $(PORT)

install:
	pip install -r requirements.txt

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete