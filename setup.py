from setuptools import setup

requires = [
    'lxml',
    'requests',
]

setup(
    name='ghtrending',
    version='0.0.2',
    description='Github Trending',
    packages=['ghtrending'],
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'ghtrending':'ghtrending'},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False
)
