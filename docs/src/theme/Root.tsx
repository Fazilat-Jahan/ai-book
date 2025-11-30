import React, { useState, useEffect } from 'react';
import Root from '@theme-original/Root';

export default function RootWrapper(props) {
  const [selectedText, setSelectedText] = useState('');
  const [position, setPosition] = useState({ top: 0, left: 0 });

  const handleMouseUp = () => {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    if (text) {
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      setSelectedText(text);
      setPosition({ top: rect.bottom + window.scrollY, left: rect.left + window.scrollX });
    } else {
      setSelectedText('');
    }
  };

  const handleAskChatbot = async () => {
    if (!selectedText) return;

    try {
      const response = await fetch('/api/v1/ask-selected', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selected_text: selectedText }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('Chatbot response:', data.answer);
      setSelectedText(''); // Hide the button after asking
    } catch (error) {
      console.error('Error asking chatbot:', error);
    }
  };

  useEffect(() => {
    document.addEventListener('mouseup', handleMouseUp);
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  return (
    <>
      <Root {...props} />
      {selectedText && (
        <div
          style={{
            position: 'absolute',
            top: `${position.top}px`,
            left: `${position.left}px`,
            zIndex: 1000,
          }}
        >
          <button
            onClick={handleAskChatbot}
            style={{
              padding: '5px 10px',
              fontSize: '12px',
              cursor: 'pointer',
              backgroundColor: '#1a73e8',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
            }}
          >
            Ask Chatbot
          </button>
        </div>
      )}
    </>
  );
}
