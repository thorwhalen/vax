import os
import smtplib
from time import sleep
from functools import partial

from vax.walgreens import check_walgreens
from vax.cvs import check_cvs
from vax.riteaid import check_riteaid


def make_some_sound(beeps=3):
    beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
    beep(beeps)


if __name__ == '__main__':
    seconds_wait_between_tries = 10

    walgreens = partial(check_walgreens, latitude=37.3861, longitude=122.0839, radius=25)
    cvs = partial(check_cvs, zipcode="94043", radius=25)
    riteaid = partial(check_riteaid, zip_code="94043", radius=25)
    while True:
        for func in [walgreens, cvs, riteaid]:
            found = func()
            if found:
                break
        sleep(seconds_wait_between_tries)

    make_some_sound()
    print(found)
