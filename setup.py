import os
from pathlib import Path

from setuptools import find_packages, setup

PROJECT_ROOT_DIR = Path(__file__).resolve().parent

with open(Path(PROJECT_ROOT_DIR, 'README.rst')) as readme_file:
    README = readme_file.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Python version is given implicitly by Django version. If Django 3.2 requires Python 3.6, this project automatically also needs Python 3.6.
# Django version is defined in "requirements.txt"
# Right now, we need Python 3.8. Because in Python 3.8 type hints with Protocols were introduced.
setup(
    name='django-bootstrap-modal-forms',
    version='2.2.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django plugin for creating AJAX driven forms in Bootstrap modal.',
    long_description=README,
    url='https://github.com/trco/django-bootstrap-modal-forms',
    author='Uros Trstenjak',
    author_email='uros.trstenjak@gmail.com',
    install_requires=[
        'Django>=3.2',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
