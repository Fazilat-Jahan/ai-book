import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';

interface Message {
  sender: 'user' | 'bot';
  text: string;
  sources?: { title: string; url: string; text: string }[];
  isTyping?: boolean;
}

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const toggleChat = () => setIsOpen(!isOpen);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => setInputValue(e.target.value);

  const sendMessageToBot = async (messageText: string, endpoint: string = '/api/v1/ask', body: object = { message: messageText }) => {
    const newMessages = [...messages, { sender: 'user', text: messageText }];
    setMessages(newMessages);
    setInputValue('');
    setIsTyping(true);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: data.answer, sources: data.source_references }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: 'Sorry, something went wrong.' }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    // Handle special commands
    if (inputValue.startsWith('/askselected ')) {
      const selectedText = inputValue.substring('/askselected '.length);
      await sendMessageToBot(inputValue, '/api/v1/ask-selected', { selected_text: selectedText });
    } else {
      await sendMessageToBot(inputValue);
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
                <div dangerouslySetInnerHTML={{ __html: msg.text.replace(/\n/g, '<br />') }} />
                {msg.sender === 'bot' && msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sourceReferences}>
                    <p>Sources:</p>
                    <ul>
                      {msg.sources.map((source, i) => (
                        <li key={i}>
                          <a href={source.url} target="_blank" rel="noopener noreferrer">{source.title}</a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
            {isTyping && (
              <div className={`${styles.message} ${styles.bot}`}>
                <div className={styles.typingIndicator}>
                  <span>.</span><span>.</span><span>.</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className={styles.inputContainer}>
            <input
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask a question..."
              disabled={isTyping}
            />
            <button onClick={handleSendMessage} disabled={isTyping}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
