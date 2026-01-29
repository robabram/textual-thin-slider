#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
import pytest
from textual.app import ComposeResult, App

from src.textual_thin_slider.thinslider import ThinSlider, ThinSliderDisplayTypeEnum


class TestThinSlider(ThinSlider):

    # 8 Slices per character * 10 characters = 80

    DEFAULT_CSS = """
        TestThinSlider {
            width: 10;
            height: 1;
        }
        """


class TestSliderApp(App):

    CSS = """        
        Horizontal {
            width: 10;
            height: 1;
        }
        """

    event = None

    def compose(self) -> ComposeResult:
        yield TestThinSlider(range_min=0, range_max=79, value=0, display_type=ThinSliderDisplayTypeEnum.no_value_display)
        yield TestThinSlider(range_min=0, range_max=79, value=0,
                             display_type=ThinSliderDisplayTypeEnum.pct_display_left)
        yield TestThinSlider(range_min=0, range_max=79, value=0,
                             display_type=ThinSliderDisplayTypeEnum.position_display_right)

    # TODO: Test event messaging is working...
    def on_slider_changed(self, event: ThinSlider.Changed):
        self.event = event


def test_slider_instantiation():
    """ Test that we can instantiate a ThinSliderRenderer class """
    obj = ThinSlider(range_min = 0, range_max = 100, value = 0)
    assert isinstance(obj, ThinSlider)


@pytest.mark.asyncio
async def test_slider_keyboard_movement():
    app = TestSliderApp()
    async with app.run_test() as pilot:
        obj = app.get_child_by_type(TestThinSlider)
        await pilot.press("right")
        assert obj.value == 1

        await pilot.press("left")
        assert obj.value == 0


@pytest.mark.asyncio
async def test_slider_mouse_events():
    """ Test mouse events changes the slider value """
    app = TestSliderApp()
    async with app.run_test() as pilot:
        obj = app.get_child_by_type(TestThinSlider)
        # Mouse down event
        await pilot.mouse_down(widget=obj, offset=(1, 0))  # offset=(x, y)
        assert obj.value == 10

        # Mouse up event
        await pilot.mouse_up(widget=obj, offset=(4, 0))
        assert obj.value == 40

        # Mouse click event
        await pilot.click(widget=obj, offset=(2, 0))
        assert obj.value == 20


@pytest.mark.asyncio
async def test_slider_mouse_text_events():
    """ Test mouse events over the text portion of the slider """
    app = TestSliderApp()
    async with app.run_test() as pilot:
        obj = app.get_child_by_type(TestThinSlider)
        # Mouse down event over the text portion of the slider should not change the value
        await pilot.mouse_down(widget=obj, offset=(1, 1))  # offset=(x, y)
        assert obj.value == 0

        obj = app.get_child_by_type(TestThinSlider)
        # Mouse down event over the text portion of the slider should not change the value
        await pilot.mouse_down(widget=obj, offset=(10, 2))  # offset=(x, y)
        assert obj.value == 0