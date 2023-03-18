cd io
cat /etc/*-release
python --version
yum update -y 
yum install epel-release -y
yum update -y 
yum install python3-pip -y
rpm -qa | grep -i python3-pip
pip3 -V
pip3 install --upgrade pip
pip3 install -e .
pip3 install build --upgrade
python3 -m build
cd dist
ls
cd ..