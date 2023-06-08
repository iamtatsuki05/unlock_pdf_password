import itertools
import string
from pathlib import Path
from typing import Optional, Union

import pikepdf

def unlock_pdf_password(
    input_pdf_path: Union[str, Path],
    output_pdf_path: Union[str, Path],
    password_in_number: bool = True,
    password_in_lower: bool = True,
    password_in_upper: bool = True,
    password_in_sign: bool = True,
    password_length: Optional[int] = None,
    password_start_length: Optional[int] = None,
) -> int:
    chars = []
    counter = password_start_length - 1 if password_start_length else 0

    if password_in_number:
        chars.extend(list(string.digits))
    if password_in_lower:
        chars.extend(list(string.ascii_lowercase))
    if password_in_upper:
        chars.extend(list(string.ascii_uppercase))
    if password_in_sign:
        chars.extend(list(string.punctuation))

    while True:
        if password_length is not None and counter >= password_length:
            print("Password not found")
            return 0

        counter += 1
        for password in itertools.product(chars, repeat=counter):
            try:
                password = "".join(password)
                with pikepdf.open(input_pdf_path, password=password) as pdf:
                    pdf_unlocked = pikepdf.new()
                    pdf_unlocked.pages.extend(pdf.pages)
                    pdf_unlocked.save(output_pdf_path)
                print(f"Password is {password}.")
                return 0
            except pikepdf.PasswordError:
                print(f"{password} is not correct.")
