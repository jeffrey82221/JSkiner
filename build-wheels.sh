echo $1
echo $2
cd /io
cat /etc/*-release
# Use the prebuilt CPython shipped with the manylinux image
PYBIN=/opt/python/cp$(echo $2 | tr -d .)-cp$(echo $2 | tr -d .)/bin
ls /opt/python
export PATH="$PYBIN:$HOME/.cargo/bin:$PATH"
python -V
yum install curl -y
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
export PATH="$HOME/.cargo/bin:$PATH"
# Install python packages
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install build --upgrade
# Test Package:
cd /io/examples
./test.sh
cd /io
# Build wheel
python -m build
cd dist
ls
# Repair wheel
python -m pip install auditwheel
auditwheel repair *.whl
