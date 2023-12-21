import React, { useState } from 'react';
import { Box, Button, Input, VStack } from '@chakra-ui/react';
import ReactMarkdown from 'react-markdown';

const ChatArea = () => {
  const [userInput, setUserInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSend = () => {
    if (userInput.trim() !== '') {
      // Add user input to chat history
      setChatHistory((prevChatHistory) => [
        ...prevChatHistory,
        { sender: 'user', message: userInput },
      ]);

      // Clear input field
      setUserInput('');

      // Send user input to API
      sendUserInput(userInput);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSend();
    }
  };

  const sendUserInput = (input) => {
    // Make the API call to http://127.0.0.1:5000/search using POST method
    // Don't forget to replace this placeholder code with your actual API call
    fetch('http://127.0.0.1:5000/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: input,
        top_k: 10,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        const gptResponse = data.gpt_response;
        console.log(gptResponse);
        // Add API response to chat history
        setChatHistory((prevChatHistory) => [
          ...prevChatHistory,
          { sender: 'bot', message: gptResponse },
        ]);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        overflowY: 'hidden', // Ensure that the outer container doesn't show a scrollbar
      }}
    >
      <Box width="1000px" bg="teal.50" borderRadius="lg" p={5} style={{ maxHeight: '600px', overflowY: 'auto' }}>
        <VStack spacing={2} align="stretch">
          {/* Chat history */}
          {chatHistory.map((chat, index) => (
            <Box
              mt='4px'
              key={index}
              bg={chat.sender === 'user' ? 'teal.200' : 'white'}
              color={chat.sender === 'user' ? 'black' : 'teal.800'}
              p={2}
              borderRadius="md"
              textAlign={chat.sender === 'user' ? 'right' : 'left'}
            >
              <span>{chat.sender === 'user' ? 'User:' : 'Bot:'}</span>
              <ReactMarkdown>{chat.message}</ReactMarkdown>
            </Box>
          ))}
        </VStack>

        {/* User input */}
        <Box mt={4} display="flex">
          <Input
            flex="1"
            value={userInput}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            bg="teal.50"
            color="teal.800"
          />

          <Button ml={2} onClick={handleSend} bg="teal.300" color="white">
            Send
          </Button>
        </Box>
      </Box>
    </div>
  );
};

export default ChatArea;
