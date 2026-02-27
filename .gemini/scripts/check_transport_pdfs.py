import pdfplumber
import os

def check_pdf(path):
    if os.path.exists(path):
        with pdfplumber.open(path) as pdf:
            print(f"{path}: {len(pdf.pages)} pages")
    else:
        print(f"Not found: {path}")

base = "Docs/Bt-core/chunk/Vol 4 Host Controller Interface/"
check_pdf(base + "Part A UART Transport Layer/source.pdf")
check_pdf(base + "Part B USB Transport Layer/source.pdf")
check_pdf(base + "Part C Secure Digital (SD) Transport Layer/source.pdf")
check_pdf(base + "Part D Three-wire UART Transport Layer/source.pdf")
