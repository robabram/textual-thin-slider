#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from src.textual_thin_slider.thinslider import ThinSliderRender, ThinSliderDisplayTypeEnum


class RendererOptions:
    max_width: int = 20

class RendererConsole:
    width:int = 20


def test_renderer_instantiation():
    """ Test that we can instantiate a ThinSliderRenderer class """
    obj = ThinSliderRender(range_min = 0, range_max = 100, position = 10)
    assert isinstance(obj, ThinSliderRender)

def test_renderer_simple_output():
    """ Test simple renderer output"""
    obj = ThinSliderRender(range_min = 0, range_max = 100, position = 0)
    assert isinstance(obj, ThinSliderRender)

    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[                  ]'
