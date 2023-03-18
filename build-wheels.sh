cd io
python -m pip3 install --upgrade pip
pip3 install -e .
pip3 install twine
pip3 install pexpect
pip3 install maturin
pip3 install build --upgrade
python -m build
cd dist
ls
cd ..