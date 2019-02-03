from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='hamberder',
    version='0.0.0.900',
    description='What the president is really thinking',
    long_description=readme,
    author='Nick Pelikan',
    author_email='nick.pelikan@gmail.com',
    url='https://github.com/npelikan/hamberder',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        "console_scripts": [
            "trumptweets = hamberder:trump_stream"
        ]
    }
)