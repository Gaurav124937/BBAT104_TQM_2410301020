# Validation Test Matrix

| Test | Expected |
|---|---|
| Blank book title | Reject |
| Blank member name | Reject |
| Negative quantity | Reject |
| Quantity 0 | Accept |
| Invalid book/member ID | Reject |
| Blank due date | Reject |
| Invalid due date format | Reject |
| Valid `YYYY-MM-DD` date | Accept |

Run:
`python -m unittest tests/test_validation.py`
