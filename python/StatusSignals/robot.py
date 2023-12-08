#!/usr/bin/env python3
"""
    This is a demo program for StatusSignal usage in Phoenix 6
"""
import wpilib
from wpilib import Timer, XboxController
from phoenix6 import *

class MyRobot(wpilib.TimedRobot):
    motor: TalonFX
    request: DutyCycleOut
    pos: StatusSignal[rotation]
    vel: StatusSignal[rotations_per_second]
    timer: Timer
    joystick: XboxController

    def robotInit(self):
        """Robot initialization function"""

        # Keep a reference to all the motor controllers used
        self.motor = TalonFX(1, "Fred")
        self.request = DutyCycleOut(0)

        self.pos = self.motor.get_position()
        self.vel = self.motor.get_velocity()

        self.timer = Timer()
        self.timer.start()

        self.joystick = XboxController(0)

        self.motor.set_position(6)

    def robotPeriodic(self) -> None:
        self.motor.set_control(self.request.with_output(self.joystick.getLeftY()))

    def teleopInit(self) -> None:
        """Start signal logger for logging purposes"""
        SignalLogger.start()

    def teleopPeriodic(self):
        """Every 100ms, print the status of the StatusSignal"""

        if self.timer.hasElapsed(0.1):
            BaseStatusSignal.refresh_all(self.pos, self.vel)
            print(f"Position is {self.pos} and velocity is {self.vel} at timestamp {self.pos.all_timestamps.get_device_timestamp().time}")

if __name__ == "__main__":
    wpilib.run(MyRobot)
