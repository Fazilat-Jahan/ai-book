import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';

interface Message {
  sender: 'user' | 'bot';
  text: string;
  sources?: { title: string; url: string; text: string }[];
  isTyping?: boolean;
}

// Configuration for the backend API URL
const API_BASE_URL = process.env.NODE_ENV === 'production' ? 'https://aibook-chatbot.vercel.app' : 'http://localhost:8000';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [greetingVisible, setGreetingVisible] = useState(true); // New state for greeting

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const toggleChat = () => setIsOpen(!isOpen);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => setInputValue(e.target.value);

  const handleSendMessageToBot = async (question: string, selectedText: string | null = null) => {
    const userMessage: Message = { sender: 'user', text: question };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputValue('');
    setIsTyping(true);

    let botMessageIndex = -1;

    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, selected_text: selectedText }),
      });

      if (!response.ok || !response.body) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedText = '';
      let initialMessageAdded = false;

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const jsonStrings = chunk.split('\n').filter(s => s.trim() !== '');

        for (const jsonString of jsonStrings) {
          try {
            const data = JSON.parse(jsonString);
            if (data.status === "streaming") {
              accumulatedText += data.content || '';
              if (!initialMessageAdded) {
                setMessages((prevMessages) => {
                  botMessageIndex = prevMessages.length;
                  return [...prevMessages, { sender: 'bot', text: accumulatedText, isTyping: true }];
                });
                initialMessageAdded = true;
              } else {
                setMessages((prevMessages) => {
                  if (botMessageIndex >= 0 && prevMessages[botMessageIndex]) {
                    const newMsgs = [...prevMessages];
                    newMsgs[botMessageIndex] = { ...newMsgs[botMessageIndex], text: accumulatedText };
                    return newMsgs;
                  }
                  return prevMessages;
                });
              }
            } else if (data.status === "complete") {
              setMessages((prevMessages) => {
                if (botMessageIndex >= 0 && prevMessages[botMessageIndex]) {
                  const newMsgs = [...prevMessages];
                  newMsgs[botMessageIndex] = { ...newMsgs[botMessageIndex], isTyping: false };
                  return newMsgs;
                }
                return [...prevMessages, { sender: 'bot', text: accumulatedText }];
              });
              setIsTyping(false);
              return;
            } else if (data.status === "error") {
              const errorMessage = data.content || 'An unknown error occurred.';
              setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: errorMessage }]);
              setIsTyping(false);
              return;
            }
          } catch (jsonError) {
            console.error('Error parsing JSON chunk:', jsonError, 'Chunk:', jsonString);
          }
        }
      }
    } catch (error) {
      console.error('Error sending message to bot:', error);
      setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: 'Sorry, something went wrong with the connection.' }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;
    await handleSendMessageToBot(inputValue);
  };

  return (
    <div className={styles.chatWidgetContainer}>
      {/* Conditionally render chat window above the toggle button */}
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.messagesContainer}>
            {messages.map((msg, index) => (
              <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                <div dangerouslySetInnerHTML={{ __html: msg.text.replace(/\n/g, '<br />') }} />
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

      {/* New UI for the toggle button */}
      <div className={styles.toggleUIContainer}>
        {greetingVisible && !isOpen && (
          <div className={styles.greetingBubble}>
            Hi! Need help with the book?
            <button
              className={styles.closeButton}
              onClick={(e) => {
                e.stopPropagation(); // Prevent opening chat
                setGreetingVisible(false);
              }}
              aria-label="Close greeting"
            >
              &times;
            </button>
          </div>
        )}
        <img
          src="/img/chatbot.png"
          alt="Toggle Chat"
          className={styles.chatbotImageToggle}
          onClick={toggleChat}
        />
      </div>
    </div>
  );
};

export default ChatWidget;