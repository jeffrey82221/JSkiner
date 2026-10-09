echo $1
echo $2
cd io
cat /etc/*-release
python --version
yum update -y
yum install epel-release -y
# Install Python
yum install -y gcc make wget openssl-devel bzip2-devel libffi-devel zlib-devel xz-devel
yum install curl -y
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
export PATH="$HOME/.cargo/bin:$PATH"
cd /usr/src
wget https://www.python.org/ftp/python/$1/Python-$1.tgz
tar xzf Python-$1.tgz 
cd Python-$1 
./configure --enable-optimizations 
make altinstall 
rm /usr/src/Python-$1.tgz 
python$2 -V 
# Install pip
yum update -y 
yum install python3-pip -y
rpm -qa | grep -i python3-pip
pip3 -V
# Install python packages
python$2 -m pip install --upgrade pip
python$2 -m pip install -e .
python$2 -m pip install build --upgrade
# Test Package:
cd /io
cd examples
./test.sh
cd ..
# Build wheel
python$2 -m build
cd dist
ls
# Repair wheel
python$2 -m pip install auditwheel
auditwheel repair *.whl