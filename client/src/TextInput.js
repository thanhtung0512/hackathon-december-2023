import React from "react";
import { TextInput } from "@chakra-ui/react";

const TextInput = ({ placeholder, value, onChange }) => {
  return (
    <TextInput
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      // Set the width to 100%
      width="100%"
    />
  );
};

export default TextInput;