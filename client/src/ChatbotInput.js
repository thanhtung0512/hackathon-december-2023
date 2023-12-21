// ChatbotInput.js
import React, { useState } from 'react';
import { Input, Button, Flex, Text } from '@chakra-ui/react';

const ChatbotInput = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSendQuery = async () => {
    try {
        console.log(query);
      const apiEndpoint = 'http://127.0.0.1:5000/search';
      const requestBody = {
        query,
        top_k: 3,
      };
      
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });
  
      console.log(response); // Log the entire response
      
      if (!response.ok) {
        throw new Error(`Error sending query: ${response.statusText}`);
      }
  
      const data = await response.json();
  
      // Update the response state
      setResponse(data);
  
      // Corrected line to set gpt_response
      console.log("gpt_response:", data.gpt_response);
    } catch (error) {
      console.error('Error sending query:', error);
    }
  };
  
  

  return (
    <Flex direction="column" align="center">
      <Input
        placeholder="Type your query here..."
        value={query}
        onChange={handleQueryChange}
        mb={4}
      />
      <Button colorScheme="blue" onClick={handleSendQuery}>
        Send
      </Button>

      {/* Display user input */}
      {query && <Text mt={4}>You: {query}</Text>}

      {/* Display GPT response */}
      {response && (
        <Text mt={4}>
          GPT Response: {response.gpt_response}
        </Text>
      )}

      {/* Display relevant results */}
      {response && response.results && response.results.length > 0 && (
        <Flex direction="column" mt={4}>
          <Text fontWeight="bold">Relevant Products:</Text>
          {response.results.map((product, index) => (
            <Text key={index}>
              {index + 1}. {product["Tên sản phẩm"]}
            </Text>
          ))}
        </Flex>
      )}
    </Flex>
  );
};

export default ChatbotInput;
