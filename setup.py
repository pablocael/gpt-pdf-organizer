from setuptools import setup, find_packages

def read_requirements_file(filename):
    """Read a requirements file and return a list of dependencies."""
    with open(filename, 'r') as file:
        requirements = file.read().splitlines()
    return requirements

setup(
    name="gpt-pdf-organizer",
    version="0.1.2",
    packages=find_packages(),
    install_requires=read_requirements_file("requirements.txt"),
    py_modules=["gpt_pdf_organizer"],
    entry_points={
        "console_scripts": [
            "gpt-pdf-organizer=gpt_pdf_organizer.gpt_pdf_organizer:main"
        ],
    },
)
