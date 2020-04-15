import setuptools

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

setuptools.setup(
    name='datacatalog-util',
    version='0.4.1',
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
        'datacatalog-fileset-enricher',
        'datacatalog-tag-template-processor',
        'datacatalog-tag-template-exporter',
    ),
    setup_requires=('pytest-runner', ),
    tests_require=('pytest-cov', ),
    python_requires='>=3.6',
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
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
