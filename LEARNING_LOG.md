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

## Python
- `date.fromisoformat()` validates ISO date strings and rejects impossible calendar dates.
- `date.today()` allows validation rules to compare submitted dates with the current local date.
- `urllib.parse.urlparse()` separates a URL into parts so its scheme and hostname can be validated.
- Empty optional form values can be normalized to `None` so sqlite3 stores SQL `NULL`.

## SQLite
- SQL `LIKE` performs partial text matching, and `%` represents any sequence of characters.
- Dynamic filters can build SQL conditions while keeping user values in separate parameters.
- SQL `ORDER BY` sorts query results by one or more columns.
- SQL placeholders protect data values, but they cannot replace SQL keywords or column names.
- A whitelist can safely map user-selected options to trusted SQL sorting clauses.
- SQL `COUNT(*)` counts rows, and `GROUP BY` creates groups that can be counted separately.
- ISO dates stored as `YYYY-MM-DD` text remain sortable in chronological order.
- `CHECK` constraints provide database-level limits in addition to Python validation.

## CSS
- CSS Grid arranges elements into rows and columns.
- `repeat(auto-fit, minmax(...))` creates responsive columns that adjust to the available width.

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
