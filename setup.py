from setuptools import setup, find_packages

setup(
    name='gpt-pdf-organizer',
    version='0.1.2',
    packages=find_packages(),
    py_modules=['gpt_pdf_organizer'],
    entry_points={
        'console_scripts': [
            'gpt-pdf-organizer=gpt_pdf_organizer.gpt_pdf_organizer:main'
        ],
    },
)
