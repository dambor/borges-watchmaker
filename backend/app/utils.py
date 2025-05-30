# utils.py
from datetime import datetime
import random
import string

def generate_reference_number() -> str:
    """Generate a unique reference number like REP-2025-001"""
    year = datetime.now().year
    random_part = ''.join(random.choices(string.digits, k=3))
    return f"REP-{year}-{random_part}"

def format_cpf_for_display(cpf: str) -> str:
    """Format CPF for display: 12345678901 -> 123.456.789-01"""
    cpf_digits = ''.join(filter(str.isdigit, cpf))
    if len(cpf_digits) == 11:
        return f"{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"
    return cpf
