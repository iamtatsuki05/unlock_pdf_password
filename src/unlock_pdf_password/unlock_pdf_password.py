import itertools
import string

import pikepdf


def unlock_pdf_password(
    input_pdf_path,
    output_pdf_path,
    password_in_number=True,
    password_in_lower=True,
    password_in_upper=True,
    password_in_sign=True,
    password_length=None,
):
    chars = []
    is_flag = False
    counter = 0
    if password_in_number:
        chars.extend(list(string.digits))
    if password_in_lower:
        chars.extend(list(string.ascii_lowercase))
    if password_in_upper:
        chars.extend(list(string.ascii_uppercase))
    if password_in_sign:
        chars.extend(list(string.punctuation))
    while is_flag != True:
        counter += 1
        for password in itertools.product(chars, repeat=counter):
            try:
                password = "".join(password)
                pdf = pikepdf.open(input_pdf_path, password=password)
                pdf_unlocked = pikepdf.new()
                pdf_unlocked.pages.extend(pdf.pages)
                pdf_unlocked.save(output_pdf_path)
                is_flag = True
            except:
                print(f"{password} is not correct.")
    print(f"Password is {password}.")