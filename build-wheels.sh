cd io
cat /etc/*-release
python --version
yum update -y
yum install epel-release -y
# Install Rust and Cargo
yum makecache
yum -y install rust
yum -y install cargo
# Install Python 3.7
yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel xz-devel 
cd /usr/src
wget https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz
tar xzf Python-3.7.11.tgz 
cd Python-3.7.11 
./configure --enable-optimizations 
make altinstall 
rm /usr/src/Python-3.7.11.tgz 
python3.7 -V 
# Install pip
yum update -y 
yum install python3-pip -y
rpm -qa | grep -i python3-pip
pip3 -V
# Install python packages
python3.7 -m pip3 install --upgrade pip
python3.7 -m pip3 install -e .
python3.7 -m pip3 install build --upgrade
# Test Package:
cd /io
cd examples
./test.sh
cd ..
# Build wheel
python3.7 -m build
cd dist
ls
# Repair wheel
python3.7 -m pip3 install auditwheel
auditwheel repair *.whl