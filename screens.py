from textual.screen import Screen
from textual import on, work
from textual.containers import VerticalScroll, Horizontal, Container
from textual.widgets import Placeholder, Label, ProgressBar, \
        Static, DataTable, Digits
from textual.reactive import reactive
from textual.timer import Timer
from textual.message import Message

from datetime import datetime
import math

from utils import print_datetime
from data import PSRList, PSR, get_shift

class PSRDirectory(Static):
    class Selected(Message):
        def __init__(self, psr: PSR):
            super().__init__()
            self.psr = psr

    directory: PSRList
    
    def on_mount(self):
        self.directory = PSRList()
        table = self.query_one(DataTable)
        table.add_column("#", key="id", width=14)
        table.add_column("started", key="started", width=12)
        self.refresh_rows()

    def compose(self):
        yield DataTable(
            show_header=False,
            show_row_labels=False,
            show_cursor=True,
            cursor_type="row"
        )
        yield Static("[dim]Ctrl+N чтобы добавить")

    @on(DataTable.RowHighlighted)
    def handle_psr_selected(self, message):
        row_key = message.row_key.value
        try:
            psr = next(x for x in self.directory.psrs if x.id == row_key)
            self.post_message(self.Selected(psr))
        except StopIteration:
            raise Exception(row_key, [x.id for x in self.directory.psrs])

    def refresh_rows(self):
        table = self.query_one(DataTable)
        to_remove = []
        to_add = []
        existing_numbers = [
            x.id for x in self.directory.psrs
        ]
        printed_rows = []
        for row in table.rows:
            if row.key not in existing_numbers:
                to_remove.append(row.key)
            else:
                printed_rows.append(row.key)
        for x in self.directory.psrs:
            if x not in printed_rows:
                to_add.append((x.id, print_datetime(x.started)))
        for x in to_remove:
            table.remove_row(x)
        for x in to_add:
            table.add_row(*x, key=x[0])
        table.sort("id", reverse=True)



class HomepageScreen(Screen):
    CSS_PATH = "home_screen.tcss"
    
    timer: Timer

    @staticmethod
    def print_time() -> str:
        return 
    
    def compose(self):
        with Container(id="home_screen"):
            with Container(id="left", classes="main_pane"):
                with Horizontal(id="left_header"):
                    yield Static("", id="date_time")
                    yield Static("", id="time_left")
                yield PSRDirectory()
            with VerticalScroll(id="psr_data_outer"):
                yield Digits('', id="psr_number")
                yield Static("Lorem", id="psr_data")
            yield Placeholder(variant="size")

    def on_mount(self):
        self.tick_time()
        self.timer = self.set_interval(60, self.tick_time)
        self.timer.resume()

    @on(PSRDirectory.Selected)
    async def handle_psr_selected(self, message):
        psr = message.psr
        digits = self.query_one("#psr_number")
        digits.update(str(psr.id))

    @work(exclusive=True)
    async def refresh_psr(self, psr: PSR):
        place = self.query_one("#psr_data")
    
    def tick_time(self):
        now = datetime.now()
        self.query_one("#date_time").update(print_datetime(now))
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

