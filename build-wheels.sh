set -e
echo $1
echo $2
cd /io
cat /etc/*-release
# Use the Python interpreters preinstalled in the manylinux image
TAG=cp$(echo $2 | tr -d .)-cp$(echo $2 | tr -d .)
export PATH="/opt/python/$TAG/bin:$HOME/.cargo/bin:$PATH"
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
python$2 -V
# Install python packages
python$2 -m pip install --upgrade pip
python$2 -m pip install -e .
python$2 -m pip install build --upgrade
# Test Package:
cd /io/examples
./test.sh
# Build wheel
cd /io
python$2 -m build
cd dist
ls
# Repair wheel
python$2 -m pip install auditwheel
auditwheel repair *.whl
