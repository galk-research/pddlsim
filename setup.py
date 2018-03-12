from setuptools import setup, dist, find_packages


class BinaryDistribution(dist.Distribution):

    def is_pure(self):
        return False


setup(
    name='pddlsim',
    version='0.1.5dev',
    classifiers=['Programming Language :: Python :: 2.7',
                 'Development Status :: 2 - Pre-Alpha',
                 'Intended Audience :: Science/Research',
                 'Operating System :: POSIX :: Linux',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 ],
    python_requires='~=2.7',
    install_requires=['six'],
    package_data={'pddlsim': [
        'external/liblapkt.so', 'external/siw-then-bfsf']},
    include_package_data=True,
    distclass=BinaryDistribution,
    # packages=['pddlsim','pddlsim/external/fd','pddlsim/executors','pddlsim/successors','pddlsim/services','pddlsim/remote'],
    packages=find_packages(exclude=['experiments'])
)
