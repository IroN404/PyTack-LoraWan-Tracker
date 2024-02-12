function decodeDownlink(input) {
  // Extraire les octets du message
  const bytes = input.data.bytes;

  // Convertir les octets en une chaîne ASCII
  const asciiMessage = Buffer.from(bytes).toString('ascii');

  return {
    data: {
      message: asciiMessage
    },
    warnings: [],
    errors: []
  };
}
