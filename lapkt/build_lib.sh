# do conditionally?

if [ ! -d "LAPKT-dev" ]; then
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
make clean
make depend
make libff

cd ../../../succ_gen
echo "-- Construct libfbplanner.so --"
scons -j 8
# cp libfbplanner.so 

