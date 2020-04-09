import setuptools

try:
    from pypandoc import convert_file
    read_md = lambda f: convert_file(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setuptools.setup(
    name='datacatalog-util',
    version='0.1.0',
    author='Marcelo Miranda',
    author_email='mesmacosta@gmail.com',
    description='A package to manage Google Cloud Data Catalog'
    ' helper commands and scripts',
    platforms='Posix; MacOS X; Windows',
    packages=setuptools.find_packages(where='./src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'datacatalog-util = datacatalog_util:main',
        ],
    },
    include_package_data=True,
    install_requires=(
        'google-cloud-datacatalog',
        'pandas',
        'tabulate',
        'datacatalog-tag-manager',
    ),
    setup_requires=('pytest-runner', ),
    tests_require=('pytest-cov', ),
    python_requires='>=3.6',
    license="MIT license",
    long_description=read_md('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    url='https://github.com/mesmacosta/datacatalog-util',
    zip_safe=False,
)
