cd io
cat /etc/*-release
python --version
yum update -y
yum install epel-release -y
# Install Rust and Cargo
yum makecache
yum -y install rust
yum -y install cargo
# Install pip
yum update -y 
yum install python3-pip -y
rpm -qa | grep -i python3-pip
pip3 -V
# Install python packages
pip3 install --upgrade pip
pip3 install -e .
pip3 install build --upgrade
# Test Package:
cd examples
./test.sh
cd ..
# Build wheel
python3 -m build
cd dist
ls
cd ..