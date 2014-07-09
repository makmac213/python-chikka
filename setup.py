import chikka

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name=chikka.__app_name__,
    version=chikka.__version__,
    description=chikka.__description__,
    author=chikka.__author__,
    author_email=chikka.__author_email__,
    packages=['chikka'],
    install_requires=['requests==2.0.1'],
    url=chikka.__app_url__,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'License :: Freeware',
    ),
    download_url=chikka.__download_url__,
)