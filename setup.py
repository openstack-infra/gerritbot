# Copyright 2011 OpenStack, LLC
# Copyright 2012 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import setuptools


from gerritbot.openstack.common import setup
from gerritbot.version import version_info as version

requires = setup.parse_requirements()
tests_require = setup.parse_requirements(['tools/test-requires'])
depend_links = setup.parse_dependency_links()


def read_file(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setuptools.setup(
    name="gerritbot",
    version=version.canonical_version_string(always=True),
    author='Hewlett-Packard Development Company, L.P.',
    author_email='openstack@lists.launchpad.net',
    description="Gerrit IRC Bot.",
    license="Apache License, Version 2.0",
    url="https://github.com/openstack-ci/gerritbot",
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    setup_requires=['setuptools_git>=0.4'],
    cmdclass=setup.get_cmdclass(),
    install_requires=requires,
    dependency_links=depend_links,
    tests_require=tests_require,
    test_suite="nose.collector",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    entry_points={
        "console_scripts": ["gerritbot = gerritbot.bot:main"]
    }
)
