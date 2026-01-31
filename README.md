![Tests Completion Status](https://github.com/robabram/textual-thin-slider/actions/workflows/tests.yaml/badge.svg)
![Coverage Status](https://raw.githubusercontent.com/robabram/textual-thin-slider/refs/heads/coverage-badge/coverage.svg?raw=true)
![Supported Python Versions](https://img.shields.io/badge/Python-v3.8%20|%20v3.9%20|%20v3.10%20|%20v3.11%20|%20v3.12%20|%20v3.13%20|%20v3.14-blue)
![is support](https://img.shields.io/badge/OS-Linux%20|%20MacOS%20|%20Windows-red)
![AI Code Pct](https://img.shields.io/badge/AI-0%25-purple)

# Textual Thin Slider
A thin slider widget for the [Textual](https://github.com/Textualize/textual) UI platform. The thin slider widget is only 1 character tall and allows 
fine control to choose a value within a range.  Options include, no value display, percentage or value. Value may displayed
on left or right of slider bar.


![Slider w/Percent](https://raw.githubusercontent.com/robabram/textual-thin-slider/refs/heads/main/examples/images/slider-percent.png?raw=true)

## Installation

```
pip install thin-textual-slider
```
```
uv add thin-textual-slider
```

## Usage

Display Option Enum and Widget Control Arguments
```python
class ThinSliderDisplayOptions(IntEnum):
    """ How should we show values with the slider bar, use bitwise and/or to set/read values. """
    none = 0  # Do not display the percentage or value (default)
    display_left = 1  # Display percentage/value to the left of the slider bar
    display_right = 2  # Display percentage/value to the right of the slider bar 
    show_value = 4  # Show current slider value instead of percentage

class ThinSlider(
    range_min: int,
    range_max: int,
    value: int,
    step: int,
    display_type: ThinSliderDisplayOptions
)

# Programmatically change slider value
slider.value = {new integer value}

```

Example: Textual App Usage With Event Message
```python
from textual import on
from textual.app import ComposeResult, App
from textual_thin_slider import ThinSlider, ThinSliderDisplayOptions

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
```