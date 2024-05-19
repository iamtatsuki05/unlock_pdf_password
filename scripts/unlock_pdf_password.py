import logging
from pathlib import Path
from typing import Optional, Union

import fire

from unlock_pdf_password.unlock_pdf_password import unlock_pdf, unlock_pdf_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def unlock_pdf_password_wrapper(
    input_pdf_path: Union[str, Path],
    output_pdf_path: Union[str, Path],
    password_length: int = None,
    password_start_length: int = None,
    password_in_number: Optional[bool] = True,
    password_in_lower: Optional[bool] = True,
    password_in_upper: Optional[bool] = True,
    password_in_sign: Optional[bool] = True,
) -> None:
    input_pdf_path = Path(input_pdf_path)
    output_pdf_path = Path(output_pdf_path)
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    password = unlock_pdf_password(
        input_pdf_path=input_pdf_path,
        password_length=password_length,
        password_start_length=password_start_length,
        password_in_number=password_in_number,
        password_in_lower=password_in_lower,
        password_in_upper=password_in_upper,
        password_in_sign=password_in_sign,
    )

    if password:
        unlock_pdf(
            input_pdf_path=input_pdf_path,
            output_pdf_path=output_pdf_path,
            password=password,
        )
        logger.info(f'PDF unlocked successfully! Password: {password}')
    logger.error('Password not found')


if __name__ == '__main__':
    fire.Fire(unlock_pdf_password)
