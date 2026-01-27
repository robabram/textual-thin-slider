#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
# A Textual thin slider control widget
#
from __future__ import annotations

from enum import IntEnum
from math import ceil
from typing import Optional, ClassVar, Type

from rich.console import RenderableType, Console, ConsoleOptions, RenderResult
from textual import events
from textual.binding import Binding
from textual.geometry import Offset, clamp
from textual.message import Message
from textual.reactive import reactive, var
from textual.widget import Widget


class ThinSliderDisplayTypeEnum(IntEnum):
    """ How should we show values with the slider bar """
    no_value_display = 0
    pct_display_left = 1
    pct_display_right = 2
    position_display_left = 3
    position_display_right = 4


class ThinSliderRender:
    PARTIAL_GLYPHS: ClassVar[list[str]] = ["▉", "▊", "▋", "▌", "▍", "▎", "▏", " "]
    SOLID_GLYPH: ClassVar[str] = "█"
    BLANK_GLYPH: ClassVar[str] = " "

    def __init__(self, range_min: int = 0, range_max: int = 100, position: int = 0,
                 display_type: ThinSliderDisplayTypeEnum = ThinSliderDisplayTypeEnum.no_value_display) -> None:
        self.range_min = range_min
        self.range_max = range_max
        self.position = position
        self.display_type = display_type

    @classmethod
    def render_bar(cls, range_min: int, range_max: int, size: int, position: int,
                   display_type: ThinSliderDisplayTypeEnum) -> str:
        """
        Draw the Thin Slider bar
        :param range_min: Minimum range value of the bar
        :param range_max: Maximum range value of the bar
        :param size: The widget window horizontal size
        :param position: The current slider position, between min and max
        :param display_type: ThinSliderValueDisplayEnum value
        :return:
        """
        _, display_left = divmod(display_type, 2)
        position = min(max(range_min, position), range_max)
        display_value = ''
        if display_type in (ThinSliderDisplayTypeEnum.pct_display_left,
                            ThinSliderDisplayTypeEnum.pct_display_right):
            if (position - range_min) == range_max:
                display_value = '100%'
            else:
                display_value = f'{round((position - range_min) / (range_max - range_min) * 100):3}%'
        elif display_type in (ThinSliderDisplayTypeEnum.position_display_left,
                              ThinSliderDisplayTypeEnum.position_display_right):
            display_value = str(position).rjust(len(str(range_max)), cls.BLANK_GLYPH)

        bar_size = (size - len(display_value)) - 2
        glyph_len = len(cls.PARTIAL_GLYPHS)

        step_size = (range_max - range_min) / bar_size
        sel_len = max(0, int((position - range_min) / step_size))

        # Build an empty bar array and then fill as needed, arrays are mutable and fast.
        bar = [cls.BLANK_GLYPH] * bar_size
        for i in range(bar_size):
            if i < sel_len:
                bar[i] = cls.SOLID_GLYPH
            elif i == sel_len:
                glyph_fill_pct = (float(((position - range_min) - (i * step_size)) / step_size))
                glyph_bar_idx = min(max(0, round(glyph_len * glyph_fill_pct)), glyph_len - 1)
                bar[i] = cls.PARTIAL_GLYPHS[(glyph_len - 1) - glyph_bar_idx]
            else:
                break
        return f'{display_value}[{"".join(bar)}]' if display_left else f'[{"".join(bar)}]{display_value}'

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        size = (options.max_width or console.width)
        bar = self.render_bar(
            range_min=self.range_min,
            range_max=self.range_max,
            size=size,
            position=self.position,
            display_type=self.display_type
        )
        yield bar


class ThinSlider(Widget, can_focus=True):
    """
    A Textual thin slider control widget.
    """
    renderer: ClassVar[Type[ThinSliderRender]] = ThinSliderRender
    # Prevent user from selecting text within the widget
    ALLOW_SELECT = False

    BINDINGS = [
        Binding("right", "slide_right", "Slide Right", show=False),
        Binding("left", "slide_left", "Slide Left", show=False),
    ]

    DEFAULT_CSS = """
    ThinSlider {
        width: 100%;
        height: 1;
        background: $surface;
        padding: 0 0;

        color: $foreground 90%;

        &:focus {
            # border: tall $border;
            background-tint: $foreground 5%;
            color: $foreground 100%;
        }
    }
    """
    # The current position value between self.min and self.max.
    value: reactive[int] = reactive(0, init=False)
    # The percent the value is between the min and max range values
    percent: float = 0.0
    # The position of the slider in a virtual range of 0.0 to 100.0
    _virtual_pos: reactive[float] = reactive(0.0)
    # Mouse capture and movement values
    _grabbed: var[Offset | None] = var[Optional[Offset]](None)
    _grabbed_pos: var[float] = var(0.0)

    class Changed(Message):
        """
        Event message is created when the value of the slider changes.
        Define a `on_slider_changed()` method to catch the event.
        """
        def __init__(self, slider: ThinSlider, value: int) -> None:
            super().__init__()
            self.value: int = value
            self.slider: ThinSlider = slider

        @property
        def control(self) -> ThinSlider:
            return self.slider

    def __init__(self, range_min: int, range_max: int,
                 display_type: ThinSliderDisplayTypeEnum = ThinSliderDisplayTypeEnum.no_value_display, step: int = 1,
                 value: int | None = None, name: str | None = None, id: str | None = None, classes: str | None = None,
                 disabled: bool = False) -> None:
        """
        :param range_min: The minimum range value of the slider
        :param range_max: The maximum range value of the slider
        :param display_type: Show a value or do not display any value
        :param step: The step size for each movement of the slider
        :param value: The initial value of the slider
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled, markup=False)
        self.min = range_min
        self.max = range_max
        self.step = step
        self.value = value if value is not None else range_min
        self.display_type = display_type

        if display_type in (ThinSliderDisplayTypeEnum.pct_display_left, ThinSliderDisplayTypeEnum.pct_display_right):
            self.display_value_len = 4
        elif display_type in (ThinSliderDisplayTypeEnum.position_display_left, ThinSliderDisplayTypeEnum.position_display_right):
            self.display_value_len = len(str(range_max))
        else:
            self.display_value_len = 0

        self._virtual_pos = ((self.value - self.min) / (self.total_steps / 100)) / self.step

    @property
    def total_steps(self) -> int:
        return int((self.max - self.min) / self.step) + 1

    def validate_value(self, value: int) -> int:
        return clamp(value, self.min, self.max)

    def validate__slider_position(self, slider_position: float) -> float:
        max_pos = ((self.max - self.min) / (self.total_steps / 100) ) / self.step
        return clamp(slider_position, 0, max_pos)

    def watch_value(self) -> None:
        if not self._grabbed:
            self._virtual_pos = ((self.value - self.min) / (self.total_steps / 100)) / self.step
        pct = (self.value / (self.max - self.min)) * 100
        self.percent = clamp(pct, 0.0, 100.0)
        self.post_message(self.Changed(self, self.value))

    def render(self) -> RenderableType:
        """ Render the slider bar """
        return self.renderer(
            range_min=self.min,
            range_max=self.max,
            position=self.value,
            display_type=self.display_type
        )

    def _calc_bar_min_max_positions(self, display_left: int, width: int) -> tuple[int, int]:
        """
        Calculate the minimum and maximum position of the slider.
        :param display_left: 1 if there is a value being displayed to the left or 0 if right of the slider.
        :param width: Width of the slider widget
        :return: Min and max positions of the slider bar
        """
        # Remember to account for display value and bracket characters
        min_x = (0 if not display_left else self.display_value_len) + 1
        max_x = (self.content_size.width if display_left else self.content_size.width - self.display_value_len) - 1
        return min_x, max_x

    def action_slide_right(self) -> None:
        self.value = self.value + self.step

    def action_slide_left(self) -> None:
        self.value = self.value - self.step

    async def _on_mouse_down(self, event: events.MouseDown) -> None:
        event.stop()

        _, display_left = divmod(self.display_type, 2)
        bar_min_x, bar_max_x = self._calc_bar_min_max_positions(display_left, self.content_size.width)
        mouse_x = (event.x - self.styles.gutter.left)
        # If we are not clicking on the bar area, just return
        if not (bar_min_x <= mouse_x < bar_max_x):
            return

        step_ratio = ceil(100 / self.total_steps)
        thumb_size = max(1.0, step_ratio / (100 / (bar_max_x - bar_min_x)))
        mouse_x_offset = max(0, (mouse_x - (bar_min_x - 1)))
        self._virtual_pos = ((mouse_x_offset - (thumb_size // 2)) / (bar_max_x - bar_min_x)) * 100

        self._grabbed = event.screen_offset
        self.action_grab()

        self.value = (self.step * round(self._virtual_pos * (self.total_steps / 100)) + self.min)

    def action_grab(self) -> None:
        self.capture_mouse()

    async def _on_mouse_up(self, event: events.MouseUp) -> None:
        event.stop()
        if self._grabbed:
            self.release_mouse()
            self._grabbed = None

    def _on_mouse_capture(self, event: events.MouseCapture) -> None:
        self._grabbed = event.mouse_position
        self._grabbed_pos = self._virtual_pos

    def _on_mouse_release(self, event: events.MouseRelease) -> None:
        event.stop()
        self._grabbed = None

    async def _on_mouse_move(self, event: events.MouseMove) -> None:
        event.stop()
        if self._grabbed:
            _, display_left = divmod(self.display_type, 2)
            bar_min_x, bar_max_x = self._calc_bar_min_max_positions(display_left, self.content_size.width)

            mouse_move = event.screen_x - self._grabbed.x
            self._virtual_pos = self._grabbed_pos + (mouse_move * (100 / (bar_max_x - bar_min_x)))
            self.value = (self.step * round(self._virtual_pos * (self.total_steps / 100)) + self.min)

    async def _on_click(self, event: events.Click) -> None:
        event.stop()
