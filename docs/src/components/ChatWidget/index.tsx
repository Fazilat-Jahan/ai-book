import React, { useState } from 'react';
import styles from './styles.module.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const toggleChat = () => setIsOpen(!isOpen);

  const handleInputChange = (e) => setInputValue(e.target.value);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const newMessages = [...messages, { sender: 'user', text: inputValue }];
    setMessages(newMessages);
    setInputValue('');

    try {
      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: inputValue }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setMessages([...newMessages, { sender: 'bot', text: data.answer }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages([...newMessages, { sender: 'bot', text: 'Sorry, something went wrong.' }]);
    }
  };

  return (
    <div className={styles.chatWidgetContainer}>
      <button className={styles.chatToggleButton} onClick={toggleChat}>
        {isOpen ? 'X' : 'Chat'}
      </button>
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.messagesContainer}>
            {messages.map((msg, index) => (
              <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                {msg.text}
              </div>
            ))}
          </div>
          <div className={styles.inputContainer}>
            <input
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask a question..."
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
