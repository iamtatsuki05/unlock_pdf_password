import tempfile
from pathlib import Path

import streamlit as st

from unlock_pdf_password.unlock_pdf_password import unlock_pdf, unlock_pdf_password


def app():
    st.title("PDF Unlocker")

    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    password_length = st.number_input(
        "Enter maximum password length:", min_value=1, value=4
    )
    password_start_length = st.number_input(
        "Enter starting password length:", min_value=0, value=0
    )
    password_in_number = st.checkbox("Include numbers", True)
    password_in_lower = st.checkbox("Include lowercase letters", True)
    password_in_upper = st.checkbox("Include uppercase letters", True)
    password_in_sign = st.checkbox("Include special characters", True)

    if st.button("Unlock PDF"):
        if uploaded_file is None:
            st.error("Please upload a PDF file.")
        else:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".pdf"
            ) as temp_input_file:
                temp_input_file.write(uploaded_file.getvalue())
                input_pdf_path = temp_input_file.name

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
            result = unlock_pdf(
                input_pdf_path=input_pdf_path,
                password=password,
                output_pdf_path=None,
            )
            if result:
                st.success(f"PDF unlocked successfully! Password: {password}")
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".pdf"
                ) as temp_output_file:
                    result.save(temp_output_file.name)
                    with open(temp_output_file.name, 'rb') as f:
                        pdf_bytes = f.read()
                    st.download_button(
                        label="Download unlocked PDF",
                        data=pdf_bytes,
                        file_name=f"unlocked_{Path(input_pdf_path).name}",
                        mime="application/octet-stream",
                    )
            else:
                st.error("Failed to unlock PDF.")
        else:
            st.error("Password not found.")


if __name__ == "__main__":
    app()
