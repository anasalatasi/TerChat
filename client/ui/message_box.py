from textual.widget import Widget
from textual.widgets import Static
from textual.app import ComposeResult

class MessageBox(Widget):
    def __init__(self, text: str, role: str, color: str) -> None:
        self.text = text
        self.role = role
        self.color = color
        super().__init__()

    def compose(self) -> ComposeResult:
        message = Static(self.text, classes=f"message {self.role}")
        message.styles.background = self.color
        yield message