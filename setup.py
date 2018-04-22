from distutils.core import setup

description = '''This package was designed to be a driver used on a raspberry pi to 
give standard methods for interfacing with a rotary encoder and allow for easier
integration into projects without having to write your own driver for a Rotary Encoder
This was written using a Keyes KY-040 encoder but should be able to work with any 
rotary encoder that has 5 pins, 3 for data, 1 for power, and 1 for ground'''

setup(
    name='RotaryEncoderDriver',
    version='1.0.0',
    packages=['RotaryEncoderDriver'],
    keywords='Rotary Encoder driver drivers keyes ky-040',
    url='https://github.com/superadm1n/RotaryEncoderDriver',
    license='MIT',
    author='Kyle Kowalczyk',
    author_email='kowalkyl@gmail.com',
    description='Driver for Rotary Encoder',
    long_description=description,
)
