from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Input, Button, Footer, Header
from textual.widget import Widget
from services.message_service import send_message_to_server, get_messages_from_server, get_message_count_from_server
from ui.message_box import MessageBox

class ChatApp(App):
    TITLE = "TerChat"
    SUB_TITLE = "Chat directly in your terminal"
    CSS_PATH = "../../static/styles.css"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_message_timestamp = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(id="conversation_box")
        with Horizontal(id="input_box"):
            yield Button(label="Message Count", variant="warning", id="count_button")
            yield Input(placeholder="Enter your message", id="message_input")
            yield Button(label="Send", variant="success", id="send_button")
        yield Footer()

    async def on_mount(self) -> None:
        self.message_polling_task = self.set_interval(2, self.poll_messages)

    async def poll_messages(self) -> None:
        new_messages = get_messages_from_server()
        if new_messages:
            if self.last_message_timestamp:
                new_messages_to_add = [msg for msg in new_messages if msg['timestamp'] > self.last_message_timestamp and msg['text'].strip()]
            else:
                new_messages_to_add = [msg for msg in new_messages if msg['text'].strip()]

            if new_messages_to_add:
                self.update_messages(new_messages_to_add)
                self.last_message_timestamp = new_messages_to_add[-1]['timestamp']

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send_button":
            self.handle_send_message()
        elif event.button.id == "count_button":
            self.handle_message_count()

    def handle_send_message(self) -> None:
        message_input = self.query_one("#message_input", Input)
        message = message_input.value
        if not message:
            return

        self.toggle_widgets(message_input, self.query_one("#send_button"))
        send_message_to_server(message)
        message_input.value = ""
        
        conversation_box = self.query_one("#conversation_box")
        conversation_box.mount(MessageBox(message, "my_message"))
        conversation_box.scroll_end(animate=False)
        self.toggle_widgets(message_input, self.query_one("#send_button"))

    def handle_message_count(self) -> None:
        message_count = get_message_count_from_server()
        if message_count is not None:
            count_button = self.query_one("#count_button", Button)
            count_button.label = f"Messages: {message_count}"

    def toggle_widgets(self, *widgets: Widget) -> None:
        for widget in widgets:
            widget.disabled = not widget.disabled

    def update_messages(self, new_messages):
        conversation_box = self.query_one("#conversation_box")
        for msg in new_messages:
            conversation_box.mount(MessageBox(msg['text'], "others_message"))
        conversation_box.scroll_end(animate=True)
