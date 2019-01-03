from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

requires = [
    'lxml',
    'requests',
]

setup(
    name='ghtrending',
    version='0.1.5rc',
    author='chinsyo',
    author_email='chinsyo@sina.cn',
    license='MIT',
    description='Github Trending Explorer',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chinsyo/ghtrending",
    packages=find_packages(),
    package_dir={'ghtrending': 'ghtrending'},
    package_data={'': ['LICENSE', 'NOTICE']},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False
)
