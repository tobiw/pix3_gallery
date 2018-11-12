import ast
import re
import setuptools

with open('pix3_gallery/pix3_gallery.py', 'r') as f:
    version = str(ast.literal_eval(re.search(r'__version__\s=\s+(.*)', f.read()).group(1)))

setuptools.setup(
    name='pix3_gallery',
    version=version,
    maintainer='Tobi Wulff',
    maintainer_email='tobi@swulff.de',
    url='http://www.github.com',
    packages=['pix3_gallery'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pix3-admin=pix3_gallery.cli:main',
        ]
    },
)
