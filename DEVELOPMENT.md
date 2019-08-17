# Development

## Building the package
```bash
pipenv run python3 setup.py sdist bdist_wheel
```

## Uploading the package
```bash
pipenv run python3 -m twine upload --skip-existing dist/*
```
