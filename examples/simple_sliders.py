#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
from textual.app import ComposeResult, App
from textual.widgets import Header, Footer

from src.textual_thin_slider.thinslider import ThinSlider, ThinSliderDisplayTypeEnum


class SimpleSliderApp(App):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ThinSlider(range_min=0, range_max=1500, value=600, display_type=ThinSliderDisplayTypeEnum.no_value_display)
        yield ThinSlider(range_min=0, range_max=250, display_type=ThinSliderDisplayTypeEnum.pct_display_left)
        yield ThinSlider(range_min=0, range_max=250, display_type=ThinSliderDisplayTypeEnum.pct_display_right)
        yield ThinSlider(range_min=72, range_max=325, display_type=ThinSliderDisplayTypeEnum.position_display_left)
        yield ThinSlider(range_min=0, range_max=1500, step=3,
                         display_type=ThinSliderDisplayTypeEnum.position_display_right)


if __name__ == "__main__":
    app = SimpleSliderApp()
    app.run()