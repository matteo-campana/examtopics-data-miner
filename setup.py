from setuptools import setup, find_packages

setup(
    name='html-data-miner',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python console application for HTML data mining',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)