echo $1
echo $2
cd io
cat /etc/*-release
python --version
yum update -y
yum install epel-release -y
# Install Rust and Cargo
yum makecache
yum -y install rust
yum -y install cargo
# Install Python
yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel xz-devel 
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
python$2 -m pip3 install --upgrade pip
python$2 -m pip3 install -e .
python$2 -m pip3 install build --upgrade
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
python$2 -m pip3 install auditwheel
auditwheel repair *.whl