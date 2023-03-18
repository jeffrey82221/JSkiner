cd io
cat /etc/*-release
yum update -y 
yum install epel-release -y
yum update -y 
yum install python3-pip -y
rpm -qa | grep -i python3-pip
pip3 -V
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