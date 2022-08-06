import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pwdriver',
    version='0.25.1',
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
    python_requires='>=3.7',
    install_requires=[
        'certifi>=2022.6.15',
        'chardet>=5.0.0',
        'idna>=3.3',
        'requests>=2.28.1',
        'selenium>=4.3.0',
        'urllib3>=1.26.11',
        'Appium-Python-Client>=2.6.0'
    ]
)
