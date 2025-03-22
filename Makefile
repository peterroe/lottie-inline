publish:
	make clean
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

clean:
	rm -rf dist build src/**/*.egg-info
