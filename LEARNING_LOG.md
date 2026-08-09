# LEARNING_LOG

## Flask
- Python web framework
- Receive a browser request
- Connect a URL to a Python function
- Return a web page
- Run a local web server

## Jinja
- Template engine for Python
- **Flask** uses it to turn an HTML template containing placeholders into finished HTML

## SQLite
- 

## JavaScript
-

## Unittest
- A unit test checks on small unit of code, such as a function or method.
- An assertion compares the actual result with the expected result.
- Test method names begin with `test_` so **unittest** can discover and run them automatically.
- A subTest lets one test method check several similar cases.
- A route integration test checks whether a Flask route, validation logic, and database work together correctly.
- **Flask**'s test client simulates browser requests without running a live server.
- Tests use a temporary database so they do not change real application data.
- `setUp` prepares the test environment, while `tearDown` restores the original settings and removes temporary files.