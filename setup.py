from setuptools import setup, find_packages

setup(
    name="txnurse",
    version="0.9",
    packages=find_packages(),

    install_requires=['lxml>=3.2.0',
                      'beautifulsoup4>=4.6.0',
                      'requests>=2.9.0'],

    entry_points={'console_scripts': ['txnurse=txnurse:main']},

    author="Aldehir Rojas",
    author_email="hello@aldehir.com",
    description="Look up Texas registered nurses by license number.",
    license="MIT",
    keywords="tx nurse registered license",
    url="https://github.com/aldehir/txnurse"
)
