import setuptools

setuptools.setup(
    name="medieval_city_generator",
    version="1.0",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'shapely==1.7.1',
        'fiona==1.8.20',
        'geopandas==0.9.0',
        'pytest==6.2.4'
        ]
)
