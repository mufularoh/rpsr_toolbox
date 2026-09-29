import termux

from textual import on
from textual.reactive import reactive, var
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Footer, Header, Static, Input

from screens import HomepageScreen

class RPSRToolBox(App):
    search_term = var("")

    SCREENS = {
        "home": HomepageScreen
    }

    def on_mount(self) -> None:
        self.push_screen("home")

    # def compose(self) -> ComposeResult:
    #     yield Header() 
    #     with Container():
    #         yield Input(
    #             placeholder="PSR #",
    #             id="search"
    #         )
    #         with VerticalScroll():
    #             yield Static(id="main", expand=True)
    #     yield Footer()
    #
    # def on_mount(self) -> None:
    #     st = self.query_one("#main", Static)
    #     call_log = termux.API.generic(["termux-call-log"])[1]
    #     result = []
    #     for rec in call_log:
    #         result.append(f"From: {rec.get('name', rec.get('phone_number'))} at: {rec['date']} {rec['type']}")
    #     st.update("\n".join(result))
    # @on(Input.Changed, "#search")
    # def on_search_change(self, message: Input.Changed):
    #     self.search_term = message.value
    #     st = self.query_one("#main", Static)
    #     st.update(f"Searching for: f{self.search_term}")

if __name__ == "__main__":
    RPSRToolBox().run()
