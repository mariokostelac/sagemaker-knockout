# Development

## Building the package
```bash
pipenv run python3 setup.py sdist bdist_wheel
```

## Uploading the package
```bash
pipenv run python3 -m twine upload --skip-existing dist/*
```

## Testing the package locally
The first step necessary for testing is to make sure it's installed in some local virtual env.
I usually create a new directory and run
```bash
pipenv install --editable ../sagemaker-knockout
```
in it.

To run the current version, type
```bash
pipenv run python -m sagemaker_knockout run
```

If you do not have something listening to port 8443, run `nc -l localhost 8443` in another tab.
