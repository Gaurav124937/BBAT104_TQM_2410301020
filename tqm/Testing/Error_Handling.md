# Error Handling Standard

Expected user/input errors should be raised as `ValueError` and displayed at
the UI boundary. Unexpected exceptions should be logged with workflow context
using `log_exception()`. User-facing messages should avoid leaking technical
implementation details.
