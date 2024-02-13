run: 
	python3 src/sync.py

test:
	python3 tests/sync_test.py

clean:
	rm -f src/data.json