#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
import pytest
from textual.app import ComposeResult, App

from src.textual_thin_slider.thinslider import ThinSlider, ThinSliderDisplayOptions


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
        yield TestThinSlider(id="slider-1", range_min=0, range_max=79, value=0, display_type=ThinSliderDisplayOptions.none)
        yield TestThinSlider(id="slider-2", range_min=0, range_max=79, value=0,
                             display_type=ThinSliderDisplayOptions.display_left)
        yield TestThinSlider(id="slider-3", range_min=0, range_max=79, value=0,
                             display_type=ThinSliderDisplayOptions.display_right)

    def on_thin_slider_changed(self, event: ThinSlider.Changed):
        self.event = event


def test_slider_instantiation():
    """ Test that we can instantiate a ThinSliderRenderer class """
    # No value/percent display
    obj = ThinSlider(range_min = 0, range_max = 100, value = 0)
    assert isinstance(obj, ThinSlider)

    # Show value as a percentage
    obj = ThinSlider(range_min=0, range_max=100, value=0, display_type=ThinSliderDisplayOptions.display_left)
    assert isinstance(obj, ThinSlider)

    # Show value
    obj = ThinSlider(range_min=0, range_max=100, value=0, display_type=ThinSliderDisplayOptions.show_value)
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

@pytest.mark.asyncio
async def test_slider_message_events():
    """ Test slider value changed event message handling """
    app = TestSliderApp()
    async with app.run_test() as pilot:
        obj = app.get_child_by_type(TestThinSlider)
        # Mouse click on slider to trigger event message
        await pilot.click(widget=obj, offset=(5, 0))  # offset=(x, y)

        assert app.event is not None
        control = app.event.control
        assert control is not None