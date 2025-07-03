

from chatwoot import Chatwoot

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton
)

from PyQt6.QtCore import QThread, QObject, QSettings

# Worker object to handle WebSocket logic
class ChatWootWorker(QObject):
    def __init__(self, chatwoot:Chatwoot):
        super().__init__()
        self.chatwoot:Chatwoot = chatwoot

    def run(self):
        self.chatwoot.run_websocket()

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Interface")
        self.setGeometry(100, 100, 400, 500)
        self.init_ui()

        self._settings = QSettings("HuzaifaIrfan", "ChatwootApp")
        self.load_settings()


        # Create chatwoot instance with agent_reply
        self.chatwoot = Chatwoot(self.agent_reply, self.contact_identifier, self.conversation_id)

        # Start WebSocket in a thread
        self.start_websocket_thread()


        self.contact_identifier=self.chatwoot.contact_identifier
        self.conversation_id=self.chatwoot.conversation_id
        self.save_settings()

    def load_settings(self):     
        self.contact_identifier: str = self._settings.value("contact_identifier", "")
        self.conversation_id: str = self._settings.value("conversation_id", "")

    def save_settings(self):
        self._settings.setValue("contact_identifier", self.contact_identifier)
        self._settings.setValue("conversation_id", self.conversation_id)

    def clear_settings(self):
        self.contact_identifier = ""
        self.conversation_id = ""
        self.save_settings()


    def start_websocket_thread(self):
        self.thread = QThread()
        self.worker = ChatWootWorker(self.chatwoot)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def init_ui(self):
        layout = QVBoxLayout()

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        # Input field and send button
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.returnPressed.connect(self.send_message)

        

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)


        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

        # Add widgets to layout
        layout.addWidget(self.chat_display)
        layout.addLayout(input_layout)

        self.setLayout(layout)

    def send_message(self):
        message = self.input_field.text().strip()
        if message:
            self.chat_display.append(f"<b>You:</b> {message}")
            self.input_field.clear()
            self.chatwoot.send_message(message)

    def agent_reply(self, sender_name, content):
        self.chat_display.append(f"<b>{sender_name}:</b> {content}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
