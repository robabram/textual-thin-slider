#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
from textual import on
from textual.app import ComposeResult, App
from src.textual_thin_slider.thinslider import ThinSlider, ThinSliderDisplayOptions


class SimpleSliderApp(App):
    slider_value: int = 0
    slider_percentage: float = 0.0

    def compose(self) -> ComposeResult:
        yield ThinSlider(
            id="test-slider",
            range_min=0,
            range_max=250,
            display_type=ThinSliderDisplayOptions.display_right | ThinSliderDisplayOptions.show_value
        )

    @on(ThinSlider.Changed, "#test-slider")
    def on_thin_slider_changed(self, event: ThinSlider.Changed) -> None:
        self.slider_value = event.value
        self.slider_percentage = event.control.percent

if __name__ == "__main__":
    app = SimpleSliderApp()
    app.run()