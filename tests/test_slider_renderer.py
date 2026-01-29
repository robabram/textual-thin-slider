#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from src.textual_thin_slider.thinslider import ThinSliderRender, ThinSliderDisplayOptions


class RendererOptions:
    max_width: int = 20


class RendererConsole:
    width: int = 20


def test_renderer_instantiation():
    """ Test that we can instantiate a ThinSliderRenderer class """
    obj = ThinSliderRender(range_min=0, range_max=100, value=10)
    assert isinstance(obj, ThinSliderRender)


def test_renderer_simple_output():
    """ Test simple renderer output"""
    obj = ThinSliderRender(range_min=0, range_max=100, value=0)
    assert isinstance(obj, ThinSliderRender)
    assert obj.value == 0

    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[                  ]'


def test_renderer_max():
    """ Test min and max renderer output """
    obj = ThinSliderRender(range_min=0, range_max=100, value=100)
    assert isinstance(obj, ThinSliderRender)
    assert obj.value == 100

    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[██████████████████]'


def test_renderer_text_pct_offsets():
    """ Test renderer output with text offsets showing the value percentage """
    obj = ThinSliderRender(range_min=0, range_max=100, value=100, display_type=ThinSliderDisplayOptions.display_left)
    assert isinstance(obj, ThinSliderRender)
    assert obj.value == 100
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '100%[██████████████]'

    obj = ThinSliderRender(range_min=0, range_max=100, value=50,
                           display_type=ThinSliderDisplayOptions.display_left)
    assert isinstance(obj, ThinSliderRender)
    assert obj.value == 50
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == ' 50%[███████       ]'

    obj = ThinSliderRender(range_min=0, range_max=100, value=100,
                           display_type=ThinSliderDisplayOptions.display_right)
    assert isinstance(obj, ThinSliderRender)
    assert obj.value == 100
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[██████████████]100%'

    obj = ThinSliderRender(range_min=0, range_max=100, value=50,
                           display_type=ThinSliderDisplayOptions.display_right)
    assert isinstance(obj, ThinSliderRender)
    assert obj.value == 50
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[███████       ] 50%'


def test_renderer_show_value_offsets():
    """ Test renderer output with text offsets, showing position value """
    obj = ThinSliderRender(range_min=0, range_max=100, value=100,
                           display_type=ThinSliderDisplayOptions.display_left | ThinSliderDisplayOptions.show_value)
    assert isinstance(obj, ThinSliderRender)
    assert obj.value == 100
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '100[███████████████]'

    obj = ThinSliderRender(range_min=0, range_max=100, value=50,
                           display_type=ThinSliderDisplayOptions.display_left  | ThinSliderDisplayOptions.show_value)
    assert isinstance(obj, ThinSliderRender)
    assert obj.value == 50
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == ' 50[███████▌       ]'

    obj = ThinSliderRender(range_min=0, range_max=100, value=100,
                           display_type=ThinSliderDisplayOptions.display_right | ThinSliderDisplayOptions.show_value)
    assert isinstance(obj, ThinSliderRender)
    assert obj.value == 100
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[███████████████]100'

    obj = ThinSliderRender(range_min=0, range_max=100, value=50,
                           display_type=ThinSliderDisplayOptions.display_right | ThinSliderDisplayOptions.show_value)
    assert isinstance(obj, ThinSliderRender)
    assert obj.value == 50
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert isinstance(result, str)
    assert result == '[███████▌       ] 50'

def test_renderer_block_sliding():
    """ We want to test that the slider shows the correct block and slice based on values """
    # Special min and max range values, 18 blocks * 8 possible slice characters = 144. We are going to walk through
    # values and validate block slice characters. Each change in value should produce a distinct bar slice.
    max_range = 18 * 8

    obj = ThinSliderRender(range_min=0, range_max=max_range - 1, value=0)
    assert isinstance(obj, ThinSliderRender)

    obj.value = 0
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == f'[{ThinSliderRender.BLANK_GLYPH}                 ]'

    obj.value = 1
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == '[▏                 ]'

    obj.value = 2
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == '[▎                 ]'

    obj.value = 3
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == '[▍                 ]'

    obj.value = 4
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == '[▌                 ]'

    obj.value = 5
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == '[▋                 ]'

    obj.value = 6
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == '[▊                 ]'

    obj.value = 7
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == '[▉                 ]'

    # This test result should be a solid glyph with no slices
    obj.value = 8
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == f'[{ThinSliderRender.SOLID_GLYPH}                 ]'

    # This test result should be one solid glyph with smallest slice glyph
    obj.value = 9
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == f'[{ThinSliderRender.SOLID_GLYPH}▏                ]'

    obj.value = 10
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == f'[{ThinSliderRender.SOLID_GLYPH}▎                ]'

    obj.value = 11
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == f'[{ThinSliderRender.SOLID_GLYPH}▍                ]'

    obj.value = 12
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == f'[{ThinSliderRender.SOLID_GLYPH}▌                ]'

    obj.value = 13
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == f'[{ThinSliderRender.SOLID_GLYPH}▋                ]'

    obj.value = 14
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == f'[{ThinSliderRender.SOLID_GLYPH}▊                ]'

    obj.value = 15
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == f'[{ThinSliderRender.SOLID_GLYPH}▉                ]'

    # This test result should be two solid glyphs with no slices
    obj.value = 16
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == f'[{ThinSliderRender.SOLID_GLYPH}{ThinSliderRender.SOLID_GLYPH}                ]'

    # This test result should be two solid glyphs with smallest slice glyph
    obj.value = 17
    result = next(obj.__rich_console__(RendererConsole(), RendererOptions()))
    assert result == f'[{ThinSliderRender.SOLID_GLYPH}{ThinSliderRender.SOLID_GLYPH}▏               ]'
