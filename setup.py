from setuptools import setup, dist, find_packages


class BinaryDistribution(dist.Distribution):
    def is_pure(self):
        return False


setup(
    name='pddlsim',    
    version='0.1dev',
    package_data={'pddlsim':['external/libfdplanner.so','external/planners/siw-then-bfsf']},
    include_package_data=True,
    distclass=BinaryDistribution,
    packages=['pddlsim','pddlsim/external/fd','pddlsim/executors','pddlsim/successors'],
    # packages=find_packages('pddlsim')
)