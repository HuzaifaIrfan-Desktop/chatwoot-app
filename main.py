

from chatwoot import Chatwoot

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)

from PyQt6.QtCore import QThread, QObject, QSettings, pyqtSignal

from colorama import init as colorama_init
from colorama import Fore, Style
colorama_init()

# Worker object to handle WebSocket logic
class ChatWootWorker(QObject):
    def __init__(self, chatwoot:Chatwoot):
        super().__init__()
        self.chatwoot:Chatwoot = chatwoot

    def run(self):
        self.chatwoot.run_websocket()

class ChatWindow(QWidget):
    def __init__(self, email, name):
        super().__init__()
        self.setWindowTitle("Chat Interface")
        self.setGeometry(100, 100, 400, 500)
        self.init_ui()

        self.email=email
        self.name=name

        self._settings = QSettings("HuzaifaIrfan", "ChatwootApp")
        self.load_settings()


        # Create chatwoot instance with agent_reply
        self.chatwoot = Chatwoot(self.agent_reply, self.email, self.name, "", self.contact_identifier, self.conversation_id)

        # Start WebSocket in a thread
        self.start_websocket_thread()


        self.contact_identifier=self.chatwoot.contact_identifier
        self.conversation_id=self.chatwoot.conversation_id
        self.email=self.chatwoot.email
        self.name=self.chatwoot.name
        self.phone_number=self.chatwoot.phone_number

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
        message_content = self.input_field.text().strip()
        if message_content:
            message=f"<b>{self.name} (You):</b> {message_content}"
            print(Fore.BLUE + message + Style.RESET_ALL)
            self.chat_display.append(message)
            self.input_field.clear()
            self.chatwoot.send_message(message_content)

    def agent_reply(self, sender_name, message_content):
        message=f"<b>{sender_name} (Agent):</b> {message_content}"
        print(Fore.BLUE + message + Style.RESET_ALL)
        self.chat_display.append(message)



class LoginWindow(QWidget):
    login_successful = pyqtSignal(str, str)  # email, name

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        # QSettings for persistent config
        self.settings = QSettings("HuzaifaIrfan", "ChatwootApp")

        # UI Elements
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.status_label = QLabel()

        self.load_settings()

        # Layout
        layout = QVBoxLayout()
        form = QFormLayout()
        form.addRow("Name:", self.name_input)
        form.addRow("Email:", self.email_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.save_settings)

        layout.addLayout(form)
        layout.addWidget(login_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)


    def load_settings(self):
        """Load saved name and email if available."""
        self.name=self.settings.value("name", "")
        self.email=self.settings.value("email", "")
        self.name_input.setText(self.name)
        self.email_input.setText(self.email)

    def save_settings(self):
        """Save name and email to persistent QSettings."""
        self.name = self.name_input.text().strip()
        self.email = self.email_input.text().strip()

        if self.name and self.email:
            self.settings.setValue("name", self.name)
            self.settings.setValue("email", self.email)
            self.status_label.setText("Saved!")
            self.login_successful.emit(self.email, self.name)  # emit signal
            self.close()
        else:
            self.status_label.setText("Please enter both name and email.")


def start_chat(email, name):
    chat_window = ChatWindow(email, name)
    chat_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    if login_window.email and login_window.name:
        start_chat(login_window.email, login_window.name)
    else:
        login_window.login_successful.connect(start_chat)
        login_window.show()

    sys.exit(app.exec())
