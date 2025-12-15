import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';

interface Message {
  sender: 'user' | 'bot';
  text: string;
  sources?: { title: string; url: string; text: string }[];
  isTyping?: boolean;
}

// Configuration for the backend API URL
// In a real application, this would come from environment variables or a config file
// For now, assuming backend is on localhost:8000
const API_BASE_URL = process.env.NODE_ENV === 'production' ? 'https://aibook-chatbot.vercel.app' : 'http://localhost:8000';

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

  // Renamed to handleSendMessageToBot for clarity as the other sendMessage function is for UI updates
  const handleSendMessageToBot = async (question: string, selectedText: string | null = null) => {
    const userMessage: Message = { sender: 'user', text: question };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputValue('');
    setIsTyping(true);

    let botMessageIndex = -1; // To track the bot's current message being streamed

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
        // The backend sends newline-delimited JSON objects
        const jsonStrings = chunk.split('\n').filter(s => s.trim() !== '');

        for (const jsonString of jsonStrings) {
          try {
            const data = JSON.parse(jsonString);

            if (data.status === "streaming") {
              accumulatedText += data.content || '';
              if (!initialMessageAdded) {
                // Add an initial bot message to the UI
                setMessages((prevMessages) => {
                  botMessageIndex = prevMessages.length;
                  return [...prevMessages, { sender: 'bot', text: accumulatedText, isTyping: true }];
                });
                initialMessageAdded = true;
              } else {
                // Update the existing bot message
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
              // Finalize message, remove typing indicator
              setMessages((prevMessages) => {
                if (botMessageIndex >= 0 && prevMessages[botMessageIndex]) {
                  const newMsgs = [...prevMessages];
                  newMsgs[botMessageIndex] = { ...newMsgs[botMessageIndex], isTyping: false };
                  return newMsgs;
                }
                // Fallback if somehow initial message was not added
                return [...prevMessages, { sender: 'bot', text: accumulatedText }];
              });
              setIsTyping(false); // Stop global typing indicator
              return; // Stop processing further
            } else if (data.status === "error") {
              const errorMessage = data.content || 'An unknown error occurred.';
              setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: errorMessage }]);
              setIsTyping(false);
              return; // Stop processing further
            }
          } catch (jsonError) {
            console.error('Error parsing JSON chunk:', jsonError, 'Chunk:', jsonString);
            // Optionally, handle malformed JSON in stream
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

    // Remove the special /askselected command, as the backend now handles selected_text in a single /ask endpoint
    // Instead, the frontend can implement a UI for selecting text, and then call handleSendMessageToBot with selectedText
    // For now, just send the inputValue as the question
    await handleSendMessageToBot(inputValue);
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
                {/* Source references are not currently provided by the backend stream, remove for now */}
                {/* {msg.sender === 'bot' && msg.sources && msg.sources.length > 0 && (
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
                )} */}
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

