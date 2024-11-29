# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of 'IMPROVER' and is released under the BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
"""Calculate the gradient between two vertical levels."""

from iris.cube import Cube

from improver import BasePlugin


class VirtualTemperature(BasePlugin):
    """Calculates the virtual temperature from temperature and specific humidity."""

    @staticmethod
    def get_virtual_temperature(temperature: Cube, specific_humidity: Cube) -> Cube:
        """
        Calculate the virtual temperature from temperature and specific humidity.

        Args:
            temperature:
                Cube of temperature
            specific_humidity:
                Cube of specific humidity

        Returns:
            Cube of virtual temperature
        """
        # Calculate the virtual temperature
        virtual_temperature = temperature.copy(
            data=temperature.data * (1 + 0.61 * specific_humidity.data)
        )
        virtual_temperature.rename("air_temperature")
        return virtual_temperature
