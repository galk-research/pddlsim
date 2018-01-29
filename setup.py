from setuptools import setup, dist, find_packages

class BinaryDistribution(dist.Distribution):
    def is_pure(self):
        return False

setup(
    name='pddlsim',    
    version='0.1dev',
    package_data={'pddlsim':['external/liblapkt.so','external/siw-then-bfsf']},
    include_package_data=True,
    distclass=BinaryDistribution,
    # packages=['pddlsim','pddlsim/external/fd','pddlsim/executors','pddlsim/successors','pddlsim/services','pddlsim/remote'],
    packages=find_packages(exclude=['experiments'])
)