from textual.widget import Widget
from textual.widgets import Static
from textual.app import ComposeResult

class MessageBox(Widget):
    def __init__(self, text: str, role: str) -> None:
        self.text = text
        self.role = role
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(self.text, classes=f"message {self.role}")
