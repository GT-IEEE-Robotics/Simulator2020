#!/usr/bin/env python3
"""
File:          Utilities.py
Author:        Mridul Bansal
Last Modified: Binit on 9/23
"""

from enum import Enum

DistConvertType = Enum('DistConvertType', 'inch2ft ft2inch centi2meter meter2centi inch2centi centi2inch inch2meter meter2inch ft2centi centi2ft ft2meter meter2ft')
PixelConvertType = Enum('PixelConvertType', 'p2inch inch2p p2ft ft2p p2centi centi2p p2meter meter2p')

class Utilities:
    """Utility class to convert between units of measure"""

    def __init__(self, window_width_p: int, field_width_ft: float, window_height_p: int, field_height_ft: float):
        """Setups the simulator ratios

        The field has a real width and height given in feet.
        The rendering window given by pygame changes when the
        user resizes the window. Therefore, we need to
        maintain updated width and height ratios that map real
        units of measures to a number of pixels.
        
        :param int window_width_p: window width in pixels
        :param int field_width_ft: field width in ft
        :param int window_height_p: window height in pixels
        :param int field_height_ft: field height in ft
        """
        self.window_width_p = window_width_p
        self.field_width_ft = field_width_ft
        self.window_height_p = window_height_p
        self.field_height_ft = field_height_ft

    def dist_convert(self, a: float, convert_type: DistConvertType) -> float:
        """Convert distance measurements

        Converts `a` from one unit of measure to another. This
        conversion type is given as an enum `DistConvertType`.
        
        :param float a: input value
        :param DistConvertType convert_type: the type of conversion

        :example:
        >>> dist_convert(12.0, DistConvertType.inch2ft)
        1.0
        """
        if(convert_type == DistConvertType.inch2ft):
            return a/12.0
        if(convert_type == DistConvertType.ft2inch):
            return 12.0*a;
        if(convert_type == DistConvertType.centi2meter):
            return a/100.0;
        if(convert_type == DistConvertType.meter2centi):
            return 100.0*a;
        if(convert_type == DistConvertType.inch2centi):
            return 2.54*a;
        if(convert_type == DistConvertType.centi2inch):
            return a/2.54;
        if(convert_type == DistConvertType.inch2meter):
            return 2.54/100.0 * a;
        if(convert_type == DistConvertType.meter2inch):
            return 100.0*a/2.54;
        if(convert_type == DistConvertType.ft2centi):
            return 12.0*a/2.54;
        if(convert_type == DistConvertType.centi2ft):
           return 2.54/12.0*a;
        if(convert_type == DistConvertType.ft2meter):
            return a/3.281
        if(convert_type == DistConvertType.meter2ft):
            return 3.281*a;
        return -1


    def pixel_convert(self, a: float, is_width: bool, convert_type: PixelConvertType) -> float:
        """Convert pixel measurements

        Converts `a` from a pixel/distance measure to another
        distance/pixel measure. This conversion type is given
        as an enum `PixelConvertType`. Picks one of the ratios
        established between window_p and field_ft for
        calculation, based on whether `a` is width or height.
        Note: Pixel values must be rounded to the nearest
        whole number despite `a` and the return type being
        floats.
        
        :param float a: input value
        :param bool is_width: whether input is a width or height val
        :param PixelConvertType convert_type: the type of conversion

        :example:
        >>> dist_convert(100.0, DistConvertType.p2ft)
        4.32156
        """
        if(convert_type == PixelConvertType.p2inch): 
            return field_width_ft/window_width_p*a*12.0;
        if(convert_type == PixelConvertType.inch2p):
            return window_width_p/field_width_ft/12*a;
        if(convert_type == PixelConvertType.p2ft):
            return field_width_ft/window_width_p*a;
        if(convert_type == PixelConvertType.ft2p):
            return window_width_p/field_width_ft*a;
        if(convert_type == PixelConvertType.p2centi):
            return field_width_ft/window_width_p*a*12.0*2.54;
        if(convert_type == PixelConvertType.centi2p):
            return window_width_p/field_width_ft/12*a/2.54;
        if(convert_type == PixelConvertType.p2meter):
            return field_width_ft/window_width_p*a*12.0*2.54/100.0;
        if(convert_type == PixelConvertType.meter2p):
            return 100.0*window_width_p/field_width_ft/12*a/2.54;
        return -1;

    
    def update_window_field_ratio(self, window_width_p: int, field_width_ft: float, window_height_p: int, field_height_ft: float) -> None:
        """Updates the simulator ratios

        The field has a real width and height given in feet.
        The rendering window given by pygame changes when the
        user resizes the window. Therefore, we need to
        maintain updated width and height ratios that map real
        units of measures to a number of pixels.
        
        :param int window_width_p: window width in pixels
        :param int field_width_ft: field width in ft
        :param int window_height_p: window height in pixels
        :param int field_height_ft: field height in ft
        """
        self.window_width_p = window_width_p
        self.field_width_ft = field_width_ft
        self.window_height_p = window_height_p
        self.field_height_ft = field_height_ft
