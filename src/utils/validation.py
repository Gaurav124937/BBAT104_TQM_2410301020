from __future__ import annotations
from datetime import datetime

def require_text(value: str, field_name: str) -> str:
    cleaned=(value or "").strip()
    if not cleaned:
        raise ValueError(f"{field_name} is required.")
    return cleaned

def non_negative_integer(value: int, field_name: str) -> int:
    try:
        number=int(value)
    except (TypeError,ValueError) as exc:
        raise ValueError(f"{field_name} must be a whole number.") from exc
    if number < 0:
        raise ValueError(f"{field_name} cannot be negative.")
    return number

def iso_date(value: str, field_name: str = "Date") -> str:
    cleaned=require_text(value, field_name)
    try:
        datetime.strptime(cleaned,"%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD format.") from exc
    return cleaned

def positive_id(value: int, field_name: str = "ID") -> int:
    try:
        number=int(value)
    except (TypeError,ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid number.") from exc
    if number <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")
    return number
