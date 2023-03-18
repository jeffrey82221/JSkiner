cd io
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install twine
python -m pip install pexpect
python -m pip install maturin
python -m pip install build --upgrade
python -m build
cd dist
ls
cd ..
echo $TWINE_USERNAME