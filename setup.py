import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pwdriver',
    version='0.26.9',
    license='MIT',
    author='Jinmoo Han',
    author_email='jinmoo21@naver.com',
    description='It will download a WebDriver, and then set basic configuration automatically.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jinmoo21/pwdriver',
    packages=setuptools.find_packages(),
    classifiers=[
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
    install_requires=[
        'selenium>=4.8.0',
        'Appium-Python-Client>=2.8.1',
        'requests>=2.28.2',
        'setuptools>=67.0.0'
    ]
)
