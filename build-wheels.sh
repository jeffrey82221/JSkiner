python -m pip install --upgrade pip
pip install -e .
pip install twine
pip install pexpect
pip install maturin
pip install build --upgrade
python -m build
cd dist
ls
cd ..