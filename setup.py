#!/usr/bin/env python

import os
from setuptools import setup, find_packages
 
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

setup(
    name='Twitnerario',
    version='1.0',
    author='Moreno Cunha',
    author_email='moreno.pinheiro@gmail.com',
    url='https://github.com/morenopc/twitnerario',
    packages=find_packages(),
    include_package_data=True,
    description='Agende e receba lembretes (tweets) com o horario que seu onibus ira passar.',
    install_requires=open('%swsgi/openshift/requirements.txt' % os.environ.get('OPENSHIFT_REPO_DIR', PROJECT_ROOT)).readlines(),
)
