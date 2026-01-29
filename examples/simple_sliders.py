#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
from textual.app import ComposeResult, App
from textual.widgets import Header, Footer

from src.textual_thin_slider.thinslider import ThinSlider, ThinSliderDisplayOptions


class SimpleSliderApp(App):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        # Show a slider only with no value display
        yield ThinSlider(range_min=0, range_max=1500, value=600, display_type=ThinSliderDisplayOptions.none)
        # Show a slider with a percentage shown on the left side
        yield ThinSlider(range_min=0, range_max=250, display_type=ThinSliderDisplayOptions.display_left)
        # Show a slider with a percentage shown on the right side
        yield ThinSlider(range_min=0, range_max=250, display_type=ThinSliderDisplayOptions.display_right)
        # Show a slider with the selected value shown on the left side
        yield ThinSlider(range_min=72, range_max=325,
                         display_type=ThinSliderDisplayOptions.display_left | ThinSliderDisplayOptions.show_value)
        # Show a slider with the selected value shown on the right side
        yield ThinSlider(range_min=0, range_max=1500, step=3,
                         display_type=ThinSliderDisplayOptions.display_right | ThinSliderDisplayOptions.show_value)


if __name__ == "__main__":
    app = SimpleSliderApp()
    app.run()
