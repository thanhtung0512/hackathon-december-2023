import React from 'react';
import { ChakraProvider, CSSReset, Box, Text } from '@chakra-ui/react';
import ChatArea from './ChatArea';

function App() {
  return (
    <ChakraProvider>
      <CSSReset />
      <Box bg="teal.500" p={4}>
        <Text color="white" fontSize="xl" fontWeight="bold" textAlign="center">
          Chat'Innov Hackathon Chatbot
        </Text>
      </Box>
      <ChatArea />
    </ChakraProvider>
  );
}

export default App;