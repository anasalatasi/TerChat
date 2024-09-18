from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Input, Button, Footer, Header, ListView, ListItem
from textual.widget import Widget
from services.message_service import client_id, send_message_to_server, get_messages_from_server, get_message_count_from_server
from ui.message_box import MessageBox
import logging
from datetime import datetime
import socketio

# Set up logging
logging.basicConfig(filename=f'chat_app-{datetime.now()}.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ChatApp(App):
    TITLE = "TerChat"
    SUB_TITLE = "Chat directly in your terminal"
    CSS_PATH = "../static/styles.css"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_message_timestamp = None
        self.sio = socketio.AsyncClient()
        logging.info("ChatApp initialized")

    def compose(self) -> ComposeResult:
        yield Header()
        self.message_list = ListView(id="conversation_box")
        yield self.message_list
        with Horizontal(id="input_box"):
            yield Button(label="Message Count", variant="warning", id="count_button")
            yield Input(placeholder="Enter your message", id="message_input")
            yield Button(label="Send", variant="success", id="send_button")
        yield Footer()
        logging.info("UI components composed")

    def on_key(self, event):
        if event.key == "enter":
            self.handle_send_message()
        elif event.key == "ctrl+c":
            self.exit()
    
    async def on_mount(self) -> None:
        await self.load_initial_messages()
        await self.setup_socketio()
        logging.info("App mounted, initial messages loaded, and SocketIO setup complete")

    async def load_initial_messages(self) -> None:
        messages = get_messages_from_server()
        for msg in messages:
            self.message_list.append(ListItem(MessageBox(msg['text'], "my_message" if msg['sender'] == client_id else "others_message")))
        self.message_list.scroll_end(animate=True)
        logging.info(f"Loaded {len(messages)} initial messages")
        
    async def setup_socketio(self):
        logging.info("Setting up SocketIO")
        
        @self.sio.event
        async def connect():
            logging.info("Connected to SocketIO server")

        @self.sio.event
        async def disconnect():
            logging.info("Disconnected from SocketIO server")

        @self.sio.on('new_message')
        async def on_new_message(data):
            logging.info(f"Received new message: {data}")
            if data['sender'] != client_id:
                await self.update_messages([data])

        try:
            await self.sio.connect('http://localhost:5005')
        except Exception as e:
            logging.error(f"Failed to connect to SocketIO server: {str(e)}")

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
        
        self.message_list.append(ListItem(MessageBox(message, "my_message")))
        self.toggle_widgets(message_input, self.query_one("#send_button"))
        
        self.message_list.scroll_end(animate=True)
        logging.info(f"Message sent: {message}")

    def handle_message_count(self) -> None:
        message_count = get_message_count_from_server()
        if message_count is not None:
            count_button = self.query_one("#count_button", Button)
            count_button.label = f"Messages: {message_count}"
            logging.info(f"Message count updated: {message_count}")

    def toggle_widgets(self, *widgets: Widget) -> None:
        for widget in widgets:
            widget.disabled = not widget.disabled
        logging.debug(f"Toggled widgets: {[w.__class__.__name__ for w in widgets]}")

    async def update_messages(self, new_messages):
        for msg in new_messages:
            self.message_list.append(ListItem(MessageBox(msg['text'], "others_message")))
        self.message_list.scroll_end(animate=True)
        logging.info(f"Updated messages with {len(new_messages)} new messages")
