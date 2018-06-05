from setuptools import setup, find_packages


setup(
    name='mosaik-batterysim',
    version='1.0.0',
    author='Mathilde Badoual',
    author_email='mathilde.badoual@gmail.com',
    description=('A simple simulator for battery profiles.'),
    long_description=(open('README.md').read()),
    url='https://github.com/mathildebadoual/mosaik-batterysim',
    install_requires=[
        'arrow>=0.4.2',
        'mosaik-api>=2.0',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mosaik-batterysim = batterysim.mosaik:main',
        ],
    },
    license='MIT',
)
