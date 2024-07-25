from setuptools import setup, find_packages

setup(
    name='jmvbd',
    version='1.0.5',
    packages=find_packages(),
    py_modules=['jmvbd'],
    install_requires=[
        'requests',
        'yt_dlp',
    ],
    entry_points={
        'console_scripts': [
            'jmvbd=jmvbd:main',  # Assuming 'main' is the entry point function in mvbackdrops.py
        ],
    },
    author='Cody St Pierre',
    author_email='codystpierre0@gmail.com',
    description='Jellyfin Movie Video Backdrop Downloader',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nxllxvxxd/JMVBD',  # Update this if you have a GitHub repo
)
