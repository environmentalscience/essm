# -*- coding: utf-8 -*-
#
# This file is part of essm.
# Copyright (C) 2017-2019 ETH Zurich, Swiss Data Science Center.
#
# essm is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# essm is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with essm; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
"""Environmental Science using Symbolic Math."""

import datetime
import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.1,<1.8',
        'matplotlib>=1.5.1',
        'sphinxcontrib-bibtex>=0.3.5',
    ],
    'generator': ['yapf>=0.16.2', ],
    'tests':
        tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.6.2',
    'setuptools_scm>=3.1.0',
]

install_requires = [
    'sympy>=1.3',
    'six>=1.10.0',
]

packages = find_packages()

version_template = """\
# -*- coding: utf-8 -*-
#
# This file is part of essm.
# Copyright (C) 2017-%d ETH Zurich, Swiss Data Science Center.
#
# essm is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# essm is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with essm; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
\"\"\"Version information for ESSM.\"\"\"

__version__ = {version!r}
""" % (datetime.date.today().year, )

setup(
    name='essm',
    use_scm_version={
        'local_scheme': 'dirty-tag',
        'write_to': os.path.join('essm', 'version.py'),
        'write_to_template': version_template,
    },
    description=__doc__,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    keywords='symbolic math environmental science',
    license='GPLv2',
    author='Stan Schymanski',
    author_email='schymans@gmail.com',
    url='https://github.com/environmentalscience/essm',
    project_urls={
        'Changelog': (
            'https://github.com/environmentalscience/essm'
            '/blob/master/CHANGES.rst'
        ),
        'Docs': 'https://essm.rtfd.io/',
    },
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={},
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 1 - Planning',
    ],
)
