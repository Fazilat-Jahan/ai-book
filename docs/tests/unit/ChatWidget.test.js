import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatWidget from '../src/components/ChatWidget';

// Mock the fetch API
global.fetch = jest.fn();

describe('ChatWidget', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders chat button', () => {
    render(<ChatWidget />);
    expect(screen.getByRole('button', { name: /chat/i })).toBeInTheDocument();
  });

  test('opens chat window when button is clicked', () => {
    render(<ChatWidget />);
    fireEvent.click(screen.getByRole('button', { name: /chat/i }));
    expect(screen.getByPlaceholderText(/ask a question/i)).toBeInTheDocument();
  });

  test('sends message and displays bot response', async () => {
    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ answer: 'Bot response' }),
      })
    );

    render(<ChatWidget />);
    fireEvent.click(screen.getByRole('button', { name: /chat/i }));

    fireEvent.change(screen.getByPlaceholderText(/ask a question/i), {
      target: { value: 'Hello bot' },
    });
    fireEvent.click(screen.getByRole('button', { name: /send/i }));

    expect(screen.getByText('Hello bot')).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText('Bot response')).toBeInTheDocument());
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith('/api/v1/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'Hello bot' }),
    });
  });

  test('displays error message on fetch failure', async () => {
    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: false,
      })
    );

    render(<ChatWidget />);
    fireEvent.click(screen.getByRole('button', { name: /chat/i }));

    fireEvent.change(screen.getByPlaceholderText(/ask a question/i), {
      target: { value: 'Hello bot' },
    });
    fireEvent.click(screen.getByRole('button', { name: /send/i }));

    expect(screen.getByText('Hello bot')).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText('Sorry, something went wrong.')).toBeInTheDocument());
  });
});
