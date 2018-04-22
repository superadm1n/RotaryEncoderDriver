# RotaryEncoderDriver

Python Module to act as a driver on a Raspberry Pi for a Rotary encoder, this was written using a Keyes KY-040
rotary encoder but should work for other encoders that have 3 data pins, a
power pin, and a ground pin.

## Installing

Instructions to install the driver into your environment

Clone the Git repo and run setup.py

Python3:
```
git clone https://github.com/superadm1n/RotaryEncoderDriver
cd RotaryEncoderDriver
python3 setup.py
```

Python2:
```
git clone https://github.com/superadm1n/RotaryEncoderDriver
cd RotaryEncoderDriver
python2 setup.py
```

## Using the Driver
The easiest way to integrate the driver into your project is to 
subclass the Driver class and overwrite the "on_" methods to 
handle the events of the rotary encoder, for an example of this
view the last if statement in the EncoderDriver.py file


## Authors

* **Kyle Kowalczyk** - *Initial work* - [Superadm1n](https://github.com/superadm1n)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


