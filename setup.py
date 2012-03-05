from distutils.core import setup

setup(
    name='asin2jan',
    version='1.0',
    description='ASIN to JAN/EAN converter',
    install_requires=['pit', 'argparse'], 
    py_modules=[
        'asin2jan',
        ],
    )

