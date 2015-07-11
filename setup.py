try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


setup(
    name='babynames',
    version='0.0.1',
    description=('Command line script that returns the arithmetic mean of '
                 'the rank of male children within the top 1000 results over '
                 'a given period of time.'),
    long_description=open('README.md').read(),
    license='GPLv2',
    author='',
    author_email='',
    include_package_data=True,
    packages=['babynames'],
    url='https://github.com/inirudebwoy/interview-task',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
