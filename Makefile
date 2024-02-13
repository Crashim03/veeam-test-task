run: 
	python3 src/sync.py

test: clean
	cp -r tests/assets tests/source_folder
	python3 src/sync.py < tests/test1.txt

clean:
	rm -f src/data.json