# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of 'IMPROVER' and is released under the BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
"""
Unit tests for the function "cube_manipulation.compare_coords".
"""

import unittest

import iris
import numpy as np
import pytest
from iris.coords import AuxCoord, DimCoord

from improver.synthetic_data.set_up_test_cubes import set_up_variable_cube
from improver.utilities.cube_manipulation import compare_coords


class Test_compare_coords(unittest.TestCase):
    """Test the compare_coords utility."""

    def setUp(self):
        """Use temperature cube to test with."""
        data = 275 * np.ones((3, 3, 3), dtype=np.float32)
        self.cube = set_up_variable_cube(data)
        self.extra_dim_coord = DimCoord(
            np.array([5.0], dtype=np.float32), standard_name="height", units="m"
        )
        self.extra_aux_coord = AuxCoord(
            ["uk_det", "uk_ens", "gl_ens"], long_name="model", units="no_unit"
        )

    def test_basic(self):
        """Test that the utility returns a list."""
        cube1 = self.cube.copy()
        cube2 = self.cube.copy()
        cubelist = iris.cube.CubeList([cube1, cube2])
        result = compare_coords(cubelist)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [{}, {}])

    def test_catch_warning(self):
        """Test warning is raised if the input is cubelist of length 1."""
        cube = self.cube.copy()
        warning_msg = "Only a single cube so no differences will be found "

        with pytest.warns(UserWarning, match=warning_msg):
            result = compare_coords(iris.cube.CubeList([cube]))

        self.assertEqual(result, [])

    def test_first_cube_has_extra_dimension_coordinates(self):
        """Test for comparing coordinate between cubes, where the first
        cube in the list has extra dimension coordinates."""
        cube1 = self.cube.copy()
        cube2 = self.cube.copy()
        cube1.add_aux_coord(self.extra_dim_coord)
        cube1 = iris.util.new_axis(cube1, "height")
        cubelist = iris.cube.CubeList([cube1, cube2])
        result = compare_coords(cubelist)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(len(result[1]), 0)
        self.assertEqual(result[0]["height"]["coord"], self.extra_dim_coord)
        self.assertEqual(result[0]["height"]["data_dims"], 0)
        self.assertEqual(result[0]["height"]["aux_dims"], None)

    def test_second_cube_has_extra_dimension_coordinates(self):
        """Test for comparing coordinate between cubes, where the second
        cube in the list has extra dimension coordinates."""
        cube1 = self.cube.copy()
        cube2 = self.cube.copy()
        cube2.add_aux_coord(self.extra_dim_coord)
        cube2 = iris.util.new_axis(cube2, "height")
        cubelist = iris.cube.CubeList([cube1, cube2])
        result = compare_coords(cubelist)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result[0]), 0)
        self.assertEqual(len(result[1]), 1)
        self.assertEqual(result[1]["height"]["coord"], self.extra_dim_coord)
        self.assertEqual(result[1]["height"]["data_dims"], 0)
        self.assertEqual(result[1]["height"]["aux_dims"], None)

    def test_first_cube_has_extra_auxiliary_coordinates(self):
        """Test for comparing coordinate between cubes, where the first
        cube in the list has extra auxiliary coordinates."""
        cube1 = self.cube.copy()
        cube2 = self.cube.copy()
        cube1.add_aux_coord(self.extra_aux_coord, data_dims=0)
        cubelist = iris.cube.CubeList([cube1, cube2])
        result = compare_coords(cubelist)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(len(result[1]), 0)
        self.assertEqual(result[0]["model"]["coord"], self.extra_aux_coord)
        self.assertEqual(result[0]["model"]["data_dims"], None)
        self.assertEqual(result[0]["model"]["aux_dims"], 0)

    def test_second_cube_has_extra_auxiliary_coordinates(self):
        """Test for comparing coordinate between cubes, where the second
        cube in the list has extra auxiliary coordinates."""
        cube1 = self.cube.copy()
        cube2 = self.cube.copy()
        cube2.add_aux_coord(self.extra_aux_coord, data_dims=0)
        cubelist = iris.cube.CubeList([cube1, cube2])
        result = compare_coords(cubelist)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result[0]), 0)
        self.assertEqual(len(result[1]), 1)
        self.assertEqual(result[1]["model"]["coord"], self.extra_aux_coord)
        self.assertEqual(result[1]["model"]["data_dims"], None)
        self.assertEqual(result[1]["model"]["aux_dims"], 0)

    def test_second_cube_has_extra_ignored_coordinate(self):
        """Test for comparing coordinate between cubes, where the second
        cube in the list has an extra dimension coordinate which is
        explicitly ignored in the comparison."""
        cube1 = self.cube.copy()
        cube2 = self.cube.copy()
        cube2.add_aux_coord(self.extra_dim_coord)
        cube2 = iris.util.new_axis(cube2, "height")
        cubelist = iris.cube.CubeList([cube1, cube2])
        result = compare_coords(cubelist, ignored_coords=["height"])
        self.assertIsInstance(result, list)
        self.assertEqual(result, [{}, {}])


if __name__ == "__main__":
    unittest.main()
