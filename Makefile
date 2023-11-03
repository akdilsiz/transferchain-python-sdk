build-publish:
	@echo "Building project"
	@rm -rf ./dist
	@python3 setup.py sdist
	@echo "Publishing project"
	@twine upload dist/*
