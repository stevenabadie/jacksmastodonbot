from setuptools import setup

setup(
    name='jacksmastodonbot',
    version='0.1',
    description='A simple Mastodon bot that posts movie quotes from IMDb quote pages.'',
    url='https://gitlab.com/stevenabadie/jacksmastodonbot',
    author='Steven Abadie',
    license='GNU General Public License v3 (GPLv3)',
    packages=['jacksmastodonbot'],
    install_reguires=[
        'beautifulsoup4',
        'Mastodon.py',
        'requests',
    ],
    zip_safe=False
)
