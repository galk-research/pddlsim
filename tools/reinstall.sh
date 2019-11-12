# run from root directory `./tools/reinstall.sh`
sudo -H pip uninstall pddlsim
python setup.py bdist_wheel
sudo -H pip install dist/$(ls dist -t | head -n1)