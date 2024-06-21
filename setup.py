from setuptools import setup, dist, find_packages


class BinaryDistribution(dist.Distribution):

    def is_pure(self):
        return False


setup(
    name='pddlsim',
    version='0.1.13dev',
    classifiers=['Programming Language :: Python :: 3.10',
                 'Development Status :: 2 - Pre-Alpha',
                 'Intended Audience :: Science/Research',
                 'Operating System :: POSIX :: Linux',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 ],
    python_requires='~=3.10',
    install_requires={"unified-planning": ["engines"],},
    tests_require=['pytest'],
    include_package_data=True,
    distclass=BinaryDistribution,
    # packages=['pddlsim','pddlsim/external/fd','pddlsim/executors','pddlsim/successors','pddlsim/services','pddlsim/remote'],
    packages=find_packages(exclude=['experiments'])
)
