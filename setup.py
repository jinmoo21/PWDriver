import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pwdriver',
    version='0.1.4',
    license='MIT',
    author='Jinmoo Han',
    author_email='jinmoo21@naver.com',
    description='It will download a WebDriver, and then set basic configuration automatically.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jinmoo21/pwdriver',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'certifi>=2020.11.8',
        'chardet>=3.0.4',
        'idna>=2.10',
        'msedge-selenium-tools>=3.141.3',
        'requests>=2.25.0',
        'selenium>=3.141.0',
        'urllib3>=1.26.2'
    ]
)