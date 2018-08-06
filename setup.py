from setuptools import setup


setup(
    name='kbase_workspace_utils',
    version='0.0.3',
    description='KBase Workspace object downloaders and uploaders',
    author='KBase Team',
    author_email='scanon@lbl.gov',
    url='https://github.com/kbase/kbase_workspace_utils',
    package_dir={'': 'src'},
    packages=['kbase_workspace_utils'],
    python_requires='>=3'
)
