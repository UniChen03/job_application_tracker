# LEARNING_LOG

## Flask
- Python web framework
- Receive a browser request
- Connect a URL to a Python function
- Return a web page
- Run a local web server
- `request.args` reads query-string values from URLs, such as `/?status=Applied`.
- A GET filter puts its selection in the URL without changing application data.

## Jinja
- Template engine for Python
- **Flask** uses it to turn an HTML template containing placeholders into finished HTML

## SQLite
- SQL `LIKE` performs partial text matching, and `%` represents any sequence of characters.
- Dynamic filters can build SQL conditions while keeping user values in separate parameters.
- SQL `ORDER BY` sorts query results by one or more columns.
- SQL placeholders protect data values, but they cannot replace SQL keywords or column names.
- A whitelist can safely map user-selected options to trusted SQL sorting clauses.

## JavaScript
-

## Unittest
- A unit test checks one small unit of code, such as a function or method.
- An assertion compares the actual result with the expected result.
- Test method names begin with `test_` so **unittest** can discover and run them automatically.
- A subTest lets one test method check several similar cases.
- A route integration test checks whether a Flask route, validation logic, and database work together correctly.
- **Flask**'s test client simulates browser requests without running a live server.
- Tests use a temporary database so they do not change real application data.
- `setUp` prepares the test environment, while `tearDown` restores the original settings and removes temporary files.
- Test-driven development follows Red, Green, and Refactor: write a failing test, make it pass, then improve the code while tests remain green.