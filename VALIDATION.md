# Validation

Local verification on Python 3.9.6 using synthetic inputs.

## Tests

```text
test_bad_line_never_echoed (test_redact.Tests) ... ok
test_case_insensitive (test_redact.Tests) ... ok
test_custom_field (test_redact.Tests) ... ok
test_free_text_is_outside_scope (test_redact.Tests) ... ok
test_nested_fields (test_redact.Tests) ... ok
test_no_mutation (test_redact.Tests) ... ok
test_preserve_values (test_redact.Tests) ... ok
test_stream (test_redact.Tests) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.000s

OK
```

## Example

```sh
python3 redact.py sample.jsonl
```

Exit status: 0. A nonzero policy result is expected for the failing example and is not a test failure.

```text
{"event": "login", "user": {"email": "[REDACTED]", "name": "Demo"}, "Authorization": "[REDACTED]", "attempts": [{"password": "[REDACTED]", "success": true}]}
```

These results demonstrate the included fixtures. They do not establish production readiness or performance on real customer data.
