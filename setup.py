from setuptools import setup
import re

def read(f):
    with open(f) as file:
        return file.read()

_version_re = re.compile(r'__version__\s+=\s+(.*)')
version = str(_version_re.search(read('ash/__init__.py').decode('utf-8')).group(1)).strip("'")

setup(name='ash',
      version=version,
      description='The Ansible SHell',
      # long_description=read('README.rd') + '\n\n' + read('HISTORY.rd'),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Ansible :: Shell :: cli',
      ],
      keywords='ash ansible shell cli prompt-toolkit pt',
      url='https://github.com/Nani-o/ash',
      author='Sofiane Medjkoune',
      author_email='sofiane@medjkoune.fr',
      license='MIT',
      packages=['ash'],
      install_requires=[
          'ansible',
          'prompt_toolkit'
      ],
      entry_points={
          'console_scripts': ['ash=ash.main:main'],
      },
      include_package_data=True,
      zip_safe=False)
