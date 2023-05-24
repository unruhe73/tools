#!/usr/bin/env python3

# you can move your mouse pointer to avoid screensaver or hibernation
# (kernel linux after version 5 is bugged and it freezes your computer
# if system tries to hibernate it)

import mouse, time

N = 1000
i = 0
while i < N:
    mouse.move(50, 50, absolute=False, duration=0.2)
    time.sleep(1)
    mouse.move(-50, -50, absolute=False, duration=0.2)
    time.sleep(1)
    mouse.move(-50, -50, absolute=False, duration=0.2)
    mouse.move(-50, -50, absolute=False, duration=0.2)
    mouse.move(50, 50, absolute=False, duration=0.2)
    mouse.move(50, 50, absolute=False, duration=0.2)
    i += 1
