from textual.screen import Screen
from textual.containers import VerticalScroll, Horizontal, Container
from textual.widgets import Placeholder, Label, ProgressBar, Static
from textual.reactive import reactive
from textual.timer import Timer

from datetime import datetime
import math

from data import get_shift

class HomepageScreen(Screen):
    CSS_PATH = "home_screen.tcss"
    
    timer: Timer

    @staticmethod
    def print_time() -> str:
        return 
    
    def on_mount(self):
        self.tick_time()
        self.timer = self.set_interval(60, self.tick_time)
        self.timer.resume()
    
    def tick_time(self):
        now = datetime.now()
        self.query_one("#date_time").update(now.strftime("%d/%m %H:%M"))
        shift_start, shift_end = get_shift()
        if shift_start > now:
            percent = 0
            left = ""
        elif shift_end < now:
            percent = 100
            left = ""
        else:
            total = shift_end - shift_start
            passed = now - shift_start
            left = (shift_end - now).seconds
            percent = math.floor((passed / total) * 100)
            left = f" {left / (60 * 60):.1f} left"
        self.query_one("#time_left").update(f"{percent}%{left}")

    def compose(self):
        with Container(id="home_screen"):
            with Container(id="left", classes="main_pane"):
                with Horizontal(id="left_header"):
                    yield Static("", id="date_time")
                    yield Static("", id="time_left")
            yield Placeholder(variant="size")
            yield Placeholder(variant="size")
