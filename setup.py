from setuptools import setup


setup(
    name='pivotal',
    version='0.0.1',
    description='Pivotal API v3.1 Implementation (incomplete)',
    url='https://github.com/HireIQ/pivotal',
    package_dir={'': 'src'},
    py_modules=['pivotal'],
    license='MIT License',
    install_requires=[
        'lxml',
        'requests'
    ]
)
