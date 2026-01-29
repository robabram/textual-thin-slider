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
    assert obj.position == 0

    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[                  ]'

def test_renderer_max():
    """ Test min and max renderer output """
    obj = ThinSliderRender(range_min = 0, range_max = 100, position = 100)
    assert isinstance(obj, ThinSliderRender)
    assert obj.position == 100

    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[██████████████████]'

def test_renderer_text_pct_offsets():
    """ Test renderer output with text offsets """
    obj = ThinSliderRender(range_min = 0, range_max = 100, position = 100, display_type= ThinSliderDisplayTypeEnum.pct_display_left)
    assert isinstance(obj, ThinSliderRender)
    assert obj.position == 100
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '100%[██████████████]'

    obj = ThinSliderRender(range_min=0, range_max=100, position=50,
                           display_type=ThinSliderDisplayTypeEnum.pct_display_left)
    assert isinstance(obj, ThinSliderRender)
    assert obj.position == 50
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == ' 50%[███████       ]'

    obj = ThinSliderRender(range_min=0, range_max=100, position=100,
                           display_type=ThinSliderDisplayTypeEnum.pct_display_right)
    assert isinstance(obj, ThinSliderRender)
    assert obj.position == 100
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[██████████████]100%'

    obj = ThinSliderRender(range_min=0, range_max=100, position=50,
                           display_type=ThinSliderDisplayTypeEnum.pct_display_right)
    assert isinstance(obj, ThinSliderRender)
    assert obj.position == 50
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[███████       ] 50%'

def test_renderer_text_value_offsets():
    """ Test renderer output with text offsets """
    obj = ThinSliderRender(range_min = 0, range_max = 100, position = 100, display_type= ThinSliderDisplayTypeEnum.position_display_left)
    assert isinstance(obj, ThinSliderRender)
    assert obj.position == 100
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '100[███████████████]'

    obj = ThinSliderRender(range_min=0, range_max=100, position=50,
                           display_type=ThinSliderDisplayTypeEnum.position_display_left)
    assert isinstance(obj, ThinSliderRender)
    assert obj.position == 50
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == ' 50[███████▌       ]'

    obj = ThinSliderRender(range_min=0, range_max=100, position=100,
                           display_type=ThinSliderDisplayTypeEnum.position_display_right)
    assert isinstance(obj, ThinSliderRender)
    assert obj.position == 100
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[███████████████]100'

    obj = ThinSliderRender(range_min=0, range_max=100, position=50,
                           display_type=ThinSliderDisplayTypeEnum.position_display_right)
    assert isinstance(obj, ThinSliderRender)
    assert obj.position == 50
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[███████▌       ] 50'
