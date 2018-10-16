init:
	conda install --yes -c conda-forge --file requirements.txt

test:
	nosetests tests
