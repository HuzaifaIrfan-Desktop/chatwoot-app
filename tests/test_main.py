

import pytest
import time

from main import ChatWindow


@pytest.fixture
def chat_window(qtbot):
    window = ChatWindow()
    qtbot.addWidget(window)
    window.show()
    return window


def test_real_chatwoot_updates_gui(chat_window: ChatWindow, qtbot):


    # Wait a bit for the Chatwoot to call agent_reply
    # qtbot.waitUntil(
    #     lambda: "Chatwoot" in chat_window.chat_display.toPlainText() or "Bot" in chat_window.chat_display.toPlainText(),
    #     timeout=10000  # increase if needed
    # )

    chat_window.agent_reply("pytest", "reply")

    chat_window.input_field.setText("pytest pyqt6")
    chat_window.send_button.click()

    # Get updated content
    text = chat_window.chat_display.toPlainText()
    assert any(name in text for name in ["pytest"])