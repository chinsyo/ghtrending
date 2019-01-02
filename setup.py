from setuptools import setup

requires = [
    'lxml',
    'requests',
]

setup(
    name='ghtrending',
    version='0.1.4',
    license='MIT',
    description='Github Trending',
    author='chinsyo',
    author_email='chinsyo@sina.cn',
    packages=['ghtrending'],
    package_dir={'ghtrending': 'ghtrending'},
    package_data={'': ['LICENSE', 'NOTICE']},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False
)
