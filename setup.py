import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-bootstrap-modal-forms',
    version='2.0.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django plugin for creating AJAX driven forms in Bootstrap modal.',
    long_description=README,
    url='https://github.com/trco/django-bootstrap-modal-forms',
    author='Uros Trstenjak',
    author_email='uros.trstenjak@gmail.com',
    install_requires=[
        'Django>=1.8',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
