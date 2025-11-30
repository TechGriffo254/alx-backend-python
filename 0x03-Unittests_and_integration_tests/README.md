# 0x03. Unittests and Integration Tests

## Description
This project covers unit testing and integration testing in Python using the `unittest` framework. It focuses on testing patterns such as mocking, parametrization, and fixtures.

## Learning Objectives
- The difference between unit and integration tests
- Common testing patterns such as mocking, parametrizations and fixtures
- How to use `unittest.mock` to mock external dependencies
- How to use `parameterized` for test parametrization

## Requirements
- All files interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All files should end with a new line
- The first line of all files should be exactly `#!/usr/bin/env python3`
- Code should use the pycodestyle style (version 2.5)
- All files must be executable
- All modules, classes and functions must have documentation
- All functions and coroutines must be type-annotated

## Files
- `utils.py` - Generic utilities for github org client
- `client.py` - A github org client
- `fixtures.py` - Test fixtures for integration tests
- `test_utils.py` - Unit tests for utils module
- `test_client.py` - Unit and integration tests for client module

## Installation
```bash
pip install parameterized requests
```

## Running Tests
```bash
# Run all tests
python -m unittest discover

# Run specific test file
python -m unittest test_utils.py
python -m unittest test_client.py

# Run with verbose output
python -m unittest discover -v
```

## Tasks

### 0. Parameterize a unit test
Test the `utils.access_nested_map` function with parameterized inputs.

### 1. Parameterize a unit test
Test that `utils.access_nested_map` raises `KeyError` for invalid inputs.

### 2. Mock HTTP calls
Test `utils.get_json` by mocking `requests.get` to avoid external HTTP calls.

### 3. Parameterize and patch
Test the `utils.memoize` decorator to ensure methods are only called once.

### 4. Parameterize and patch as decorators
Test `GithubOrgClient.org` returns correct value using mocked `get_json`.

### 5. Mocking a property
Test `GithubOrgClient._public_repos_url` by mocking the `org` property.

### 6. More patching
Test `GithubOrgClient.public_repos` with mocked dependencies.

### 7. Parameterize
Test `GithubOrgClient.has_license` with different license configurations.

### 8. Integration test: fixtures
Create integration tests using fixtures to test end-to-end functionality.

## Author
ALX Backend Python Project
