#!/usr/bin/env python
# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of 'IMPROVER' and is released under the BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
"""CLI to calculate the virtual temperature from temperature and specific humidity."""

from improver import cli


@cli.clizefy
@cli.with_output
def process(cubeList: cli.inputcube) -> cli.outputcube:
    """Calculate the virtual temperature from temperature and specific humidity.

    Args:
        cubeList:
            2 cubes, the first is temperature and the second is specific humidity

    Returns:
        Cube of virtual temperature
    """
    from improver.temperature.virtual_temperature import VirtualTemperature

    return VirtualTemperature.get_virtual_temperature(cubeList[0], cubeList[1])
