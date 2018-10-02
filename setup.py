from setuptools import setup


setup(
    name='kbase_workspace_utils',
    version='0.0.12',
    description='KBase Workspace object downloaders and uploaders',
    author='KBase Team',
    author_email='info@kbase.us',
    url='https://github.com/kbase/kbase_workspace_utils',
    package_dir={'': 'src'},
    packages=['kbase_workspace_utils'],
    install_requires=[
        'python-dotenv>=0.8.2',
        'requests>=2.19.1',
        'biopython>=1.72'
    ],
    python_requires='>=3'
)
