thieme-dl - download PDFs from eref.thieme.de

- [INSTALLATION](#installation)
- [DESCRIPTION](#description)
- [DEVELOPER INSTRUCTIONS](#developer-instructions)
- [FAQ](#faq)
- [BUGS](#bugs)
- [COPYRIGHT](#copyright)

# INSTALLATION

To start it right away for windows 64-bit:
    ./thieme-dl-x64.exe

If you use this, you don't need a python interpreter because everything is packed for you. 

# DESCRIPTION
**thieme-dl** is a command-line program to download PDFs from eref.thieme.de. It requires the Python interpreter, version 2.7, or 3.2+, and it is not platform specific. It should work on your Unix box, on Windows or on macOS. It is released to the public domain, which means you can modify it, redistribute it or use it however you like.

# USAGE
The application needs no arguments.

You have to input an ebook suffix.
Example:

https://eref.thieme.de/ebooks/pdf/1120492/240460103_002_005_004_001.pdf -> "ebooks/pdf/1120492/240460103%s.pdf"

https://eref.thieme.de/ebooks/pdf/2343785/236920105_001.pdf -> "ebooks/pdf/2343785/236920105%s.pdf"

https://eref.thieme.de/ebooks/pdf/cs_18124224/184890105_001.pdf -> "ebooks/pdf/cs_18124224/184890105%s.pdf"


# DEVELOPER INSTRUCTIONS

To build it right away for your operating system:

    pyinstaller ./main.py --onefile --add-binary "./driver/geckodriver.exe;./driver"

Most users do not need to build thieme-dl and can download an .exe file.

To run thieme-dl as a developer, you clone this repo and 
    
    pip install -r requirements.txt

then you can simple run `main.py`.

# FAQ

coming soon

# BUGS

Bugs and suggestions should be reported at: https://github.com/LukasWestholt/thieme-dl/issues. Unless you were prompted to or there is another pertinent reason (e.g. GitHub fails to accept the bug report), please do not send bug reports via personal email.

# COPYRIGHT

thieme-dl is released into the public domain by the copyright holders.

This README file was originally written by Lukas Westholt and is likewise released into the public domain.