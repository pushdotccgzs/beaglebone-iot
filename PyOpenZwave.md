# Installing py-openzwave #

first get the sources:
```
 git clone git://github.com/maartendamen/py-openzwave.git
```
additional packages needed:
```
 sudo apt-get install g++ libudev-dev cython python-dev
```
form the README:
First build the openzwave library:
```
 cd openzwave/cpp/build/linux; make
```
Then the python library:
```
 python setup.py build
 sudo python setup.py install
```
