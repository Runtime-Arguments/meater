#!/usr/bin/python3

#
# Copyright Scott Balneaves <sbalneav@beaconia.ca>
#

import aiohttp
import asyncio
import argparse
from datetime import datetime
from meater import MeaterApi
import sys

# Email and password given when registering the meater app
EMAIL = 'TheEmailYouUsed@when.u.signed.up'
PASSWORD = 'SomeSuperSecurePassword'

# Mapping between the human name of the probe (the 1, 2, 3, and 4 stamped in
# the end) and the 64 character probe id registered at the meater app.
mapping = {
 'Probe 1': 'f67db253483e0330197958121d5e656921a1d6432eccc4d8f12575560dbc6de2',
 'Probe 2': '329ac6b8c6d0c796f9c17d857f03ed807b067f5663eb54a774e1e307b6ee4c05',
 'Probe 3': 'c385603fae43855469c84b67ac69f10ffe0aef84883fd126ec0b4caefe2eab7a',
 'Probe 4': 'f0a3054bfbb441154d9f36f9caed0d04ae07ec161cc0608b7fbc5f6d6e1fbe30'
}


def c_to_f(celsius):
    """Convert celcius to fahrenheit"""
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit


# Function to get the readings.  Note the async.
async def get_readings():
    """Read the temperatures from the 4 probes"""
    # Get an async http session, and get a handle to the meater api
    session = aiohttp.ClientSession()
    api = MeaterApi(session)

    # Get the current time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # Authenticate with the meater cloud service, loop through the human names,
    # and query each of the 4 probes, and print the temps
    try:
        print(f'{current_time} ', end='')
        await api.authenticate(EMAIL, PASSWORD)
        for probe in sorted(mapping.keys()):
            device = await api.get_device(mapping[probe])
            internal = c_to_f(device.internal_temperature)
            ambient = c_to_f(device.ambient_temperature)
            print(f'{internal:5.1f} {ambient:5.1f}  ', end='')
        print()  # We've been putting all the info on one line, finish the line
    except:
        print('Meater device not connected.  Are you running the app?')

    await session.close()  # Close the http session


async def main():
    """Mainline, starts the async thread, gets the readings"""
    await asyncio.gather(get_readings())


def print_header():
    """Prints a header"""
    print('Time     Probe 1      Probe 2      Probe 3      Probe 4')
    print('======== ============ ============ ============ ============')


if __name__ == '__main__':
    # Parse our argments, either print header, or take readings.
    parser = argparse.ArgumentParser()
    parser.add_argument('--header', help='Print header', action='store_true')
    args = parser.parse_args()

    if args.header:
        print_header()
        sys.exit(0)

    asyncio.run(main())
