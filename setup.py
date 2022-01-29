import io
import os
import re
import setuptools


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(
            text_type(r':[a-z]+:`~?(.*?)`'),
            text_type(r'``\1``'),
            fd.read()
        )


setuptools.setup(
    name="web_scraping",
    version="0.0.1",
    url="https://github.com/mario-koddenbrock/web-scraping",
    license='MIT',

    author="Mario Koddenbrock & Christoph Lange",
    author_email="projectdatascience22@gmail.com",

    description="Private data science project on news content from tagesschau.de",
    long_description=read("README.rst"),
    long_description_content_type='test/x-rst',
    packages=setuptools.find_packages(exclude=('tests')),
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'web_magpie=web_scraping.cli:cli_group'
        ],
    },
)
