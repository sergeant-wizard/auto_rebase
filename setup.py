from setuptools import setup


setup(
    packages=['auto_rebase'],
    maintainer='Ryo Miyajima',
    description='Rebase all your PRs',
    license='TBD',
    author='Ryo Miyajima',
    maintainer_email='sergeant.wizard@gmail.com',
    version='0.0.0',
    name='auto_rebase',
    install_requires=[
        'gitpython',
        'requests',
    ],
    entry_points={
        'console_scripts': ['auto_rebase=auto_rebase.auto_rebase:main'],
    }
)
