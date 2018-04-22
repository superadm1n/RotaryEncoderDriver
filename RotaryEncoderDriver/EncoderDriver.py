"""
MIT License

Copyright (c) 2018 Kyle Kowalczyk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import RPi.GPIO as gpio
import time


class Driver:

    '''This class is the "driver" for the Keyes KY-040 rotary encoder, its designed
    to be inherited by a child class and the "on_" methods overwritten in the child class
    to handle what the programmer wants to do when there is an event on the knob.
    '''

    def __init__(self, clk, dt, sw):

        '''Sets the GPIO mode, initializes the data structure for keeping
        track of the GPIO pins and initalizes the GPIO pins

        :param clk: BCM GPIO pin number that the clk pin is connected to
        :param dt: BCM GPIO pin number that the dt pin is connected to
        :param sw: BCP GPIO pin number that the sw pin is connected to.
        '''

        gpio.setmode(gpio.BCM)
        self.kill_flag = False
        self.clk = clk
        self.dt = dt
        self.sw = sw
        self.states = {'clk': 1, 'dt': 1, 'sw': 1}
        self._initialize_GPIO()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        gpio.cleanup()

    def _initialize_GPIO(self):

        '''Ment to be called by the __init__ method to initilize the GPIO pins as
        input pins

        :return: nothing
        '''

        gpio.setup(self.clk, gpio.IN)
        gpio.setup(self.dt, gpio.IN)
        gpio.setup(self.sw, gpio.IN)

    def _wait_for_reset(self):

        '''This method will loop until all of the GPIO pins return to a state of 1 (power on pin)
        this is so you dont get a bunch of unintended events and have a turn or press handled
        multiple times in error

        :return: Nothing
        '''

        # grabs the initial status of the 'sw' pin to detect if it was pressed later on
        # so we can run code on release of the button
        swState = gpio.input(self.sw)

        while True:

            # gets the state of each GPIO Pin
            stateClk, stateDt, stateSw = self._get_gpio_state()

            # checks for changes in the state of each of the GPIO pins and if there
            # were changes it updates the value in the class dictionary
            self._update_state_dictionary(stateClk, stateDt, stateSw)

            # If all the pins have power back to them (meaning we are in a rest state)
            if self.states['clk'] == 1 and self.states['dt'] == 1 and self.states['sw'] == 1:
                time.sleep(.001)  # waiting will allow us to not get incorrect results

                # detects if the event was a button press and if it was it will run the
                # on_release() method to handle code on the button release
                if swState == 0:
                    self.on_release()
                # breaks out of loop because at this point we are in a rest state on the
                # rotary encoder
                break

    def _analyze_state(self):

        '''This method will check the state of the pins and based on the state
        will call the proper method to handle the encoder event

        :return:
        '''

        if self.states['clk'] == 0 and self.states['dt'] == 1:
            self.on_right()

        if self.states['dt'] == 0 and self.states['clk'] == 1:
            self.on_left()

        if self.states['sw'] == 0:
            self.on_press()

    def _get_gpio_state(self):

        '''Gathers the state of the GPIO pins.

        :return: state of CLK, DT, and SW pins
        '''

        stateClk = gpio.input(self.clk)
        stateDt = gpio.input(self.dt)
        stateSw = gpio.input(self.sw)

        return stateClk, stateDt, stateSw

    def _update_state_dictionary(self, stateClk, stateDt, stateSw):

        '''Checks if the states provided in the method are updated to what
        we have recorded in the self.states dictionary and if it is new
        it updates the self.states dictionary key with the proper value

        :param stateClk: State of the CLK pin
        :type stateClk: int
        :param stateDt: State of the DT pin
        :type stateDt: int
        :param stateSw: State of the SW pin
        :type stateSw: int
        :return: Nothing
        '''

        if stateClk != self.states['clk']:
            self.states['clk'] = stateClk
        if stateDt != self.states['dt']:
            self.states['dt'] = stateDt
        if stateSw != self.states['sw']:
            self.states['sw'] = stateSw

    def on_right(self):

        '''Overwrite this method to handle an event when the knob is turned right

        :return: Nothing by default
        '''

        return

    def on_left(self):

        '''Overwrite this method to handle an event when the knob is turned left

        :return: Nothing by default
        '''

        return

    def on_press(self):

        '''Overwrite this method to handle an event when the knob is pressed down

        :return: Nothing by default
        '''

        return

    def on_release(self):

        '''Overwrite this method to handel an event when the know is released

        :return: Nothing by default
        '''

        return

    def run_loop(self):

        '''This method runs the loop to get the state of each GPIO pin,
        analyze the state of the pins and based on the state handle a left,
        right, or button press differently

        :return: Nothing
        '''

        while True:

            # gets the state of each GPIO Pin
            stateClk, stateDt, stateSw = self._get_gpio_state()

            # checks for changes in the state of each of the GPIO pins and if there
            # were changes it updates the value in the class dictionary
            self._update_state_dictionary(stateClk, stateDt, stateSw)

            self._analyze_state()

            self._wait_for_reset()

            if self.kill_flag is True:
                break

        gpio.cleanup()

if __name__ == '__main__':

    '''This code is to give the user an example on how to integrate this driver in their code
    and allow them to have working code to run the module directly and interface with the encoder to see
    how the code is executed.
    '''

    class UsingDriver(Driver):

        '''This class inherits the RotaryEncoder driver and overwrites the "on_"
        methods to preform a task when there is an event on the rotary encoder
        '''

        def __init__(self, clk, dt, sw):
            Driver.__init__(self, clk, dt, sw)

        def on_left(self):
            print('The encoder was turned to the left 1 notch')

        def on_right(self):
            print('The encoder was turned to the right 1 notch')

        def on_press(self):
            print('The encoder was pressed down')

        def on_release(self):
            print('The encoder button was released')
    '''
    # Sets up the GPIO pins and drops into the loop
    driver = UsingDriver(13, 19, 26)
    try:
        driver.run_loop()
    except KeyboardInterrupt:
        driver.kill_flag = True
    '''
    with UsingDriver(13, 19, 26) as driver:
        try:
            driver.run_loop()
        except KeyboardInterrupt:
            driver.kill_flag = True