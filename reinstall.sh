sudo -H pip uninstall pddlsim
python setup.py bdist_wheel
sudo -H pip install dist/pddlsim-0.1.dev0-py2-none-any.whl