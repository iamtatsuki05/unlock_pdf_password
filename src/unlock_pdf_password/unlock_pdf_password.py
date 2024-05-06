import itertools
import logging
import string
from pathlib import Path
from typing import Optional, Union

import pikepdf
from tqdm.auto import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_char_set(
    numbers: bool, lowercase: bool, uppercase: bool, special_chars: bool
) -> list[str]:
    chars = []
    if numbers:
        chars.extend(string.digits)
    if lowercase:
        chars.extend(string.ascii_lowercase)
    if uppercase:
        chars.extend(string.ascii_uppercase)
    if special_chars:
        chars.extend(string.punctuation)
    return chars


def find_password(
    input_pdf_path: Union[str, Path],
    chars: list[str],
    password_length: int,
    password_start_length: int,
) -> str:
    for length in tqdm(range(password_start_length, password_length + 1)):
        for password_tuple in itertools.product(chars, repeat=length):
            password = ''.join(password_tuple)
            try:
                with pikepdf.open(input_pdf_path, password=password):
                    logger.info(f'Password found: {password}')
                    return password
            except pikepdf.PasswordError:
                logger.debug(f'Tried password: {password} - Incorrect')
    logger.error('Password not found')
    return ''


def unlock_pdf(
    input_pdf_path: Union[str, Path],
    password: str,
    output_pdf_path: Optional[Union[str, Path]] = None,
) -> Union[pikepdf.Pdf, bool]:
    try:
        with pikepdf.open(input_pdf_path, password=password) as pdf:
            pdf_unlocked = pikepdf.new()
            pdf_unlocked.pages.extend(pdf.pages)
            if output_pdf_path is not None:
                pdf_unlocked.save(output_pdf_path)
        return pdf_unlocked
    except pikepdf.PasswordError:
        return False


def unlock_pdf_password(
    input_pdf_path: Union[str, Path],
    password_length: int = None,
    password_start_length: int = None,
    password_in_number: Optional[bool] = True,
    password_in_lower: Optional[bool] = True,
    password_in_upper: Optional[bool] = True,
    password_in_sign: Optional[bool] = True,
) -> Union[str, bool]:
    input_pdf_path = Path(input_pdf_path)

    if password_length is None or password_start_length is None:
        logger.error('Password length and start length must be specified')
        return False

    chars = create_char_set(
        numbers=password_in_number,
        lowercase=password_in_lower,
        uppercase=password_in_upper,
        special_chars=password_in_sign,
    )
    password = find_password(
        input_pdf_path=input_pdf_path,
        chars=chars,
        password_length=password_length,
        password_start_length=password_start_length,
    )
    return password
