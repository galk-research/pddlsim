if [ -z "$(ls -A 'LAPKT-dev')" ]; then
echo "-- init git submodule --"
    git submodule init
    git submodule update
fi
cd LAPKT-dev

echo "-- Compile shared LAPKT --"
#this line adds -fPIC to the flags
sed -i "19s/.*/\tcommon_env.Append( CCFLAGS = ['-O3','-Wall', '-std=c++0x', '-DNDEBUG', '-fPIC'] )/" SConstruct
scons

echo "-- Make libff library --"
cd external/libff
sed -i "15s/.*/CFLAGS  =  -O6 -Wall -ansi \$(TYPE) \$(ADDONS) -fPIC/" Makefile
make clean
make depend
make libff

echo "-- Construct libfbplanner.so --"
cd ../../../succ_gen
scons -j 8