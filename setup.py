import ast
import re
import setuptools

with open('pix3_gallery/pix3_gallery.py', 'r') as f:
    version = str(ast.literal_eval(re.search(r'__version__\s=\s+(.*)', f.read()).group(1)))

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='pix3_gallery',
    version=version,
    description='Pix3 photo gallery',
    long_description=long_description,
    maintainer='Tobi Wulff',
    maintainer_email='tobi@swulff.de',
    url='https://github.com/tobiw/pix3_gallery',
    license='GPLv3',
    packages=['pix3_gallery'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pix3-admin=pix3_gallery.cli:main',
        ]
    },
)
