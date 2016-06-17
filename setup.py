name, version = 'automation_resources', '0.0.1'

from setuptools import setup, find_packages

setup(
    name=name,
    version=version,
    install_requires=[
        'setuptools'
        ],
    py_modules=[
        'GenerateCSV',
        'ValidateJsonSchema',
        'jsonextract',
        ],
    package_dir={'': '.'},
    zip_safe=False,
    description='Shared test automation resources',
    )

