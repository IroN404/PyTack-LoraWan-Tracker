function decodeUplink(input) {
  // Extraire les données pertinentes du payload JSON
  const latitude = input.data.uplink_message.locations["frm-payload"].latitude;
  const longitude = input.data.uplink_message.locations["frm-payload"].longitude;
  const frmPayload = input.data.uplink_message.frm_payload;

  // Créer la structure de données pour la fonction decodeUplink
  const decodedData = {
    bytes: [latitude, longitude, frmPayload], // Placer les données dans un tableau d'octets
  };

  return {
    data: decodedData,
    warnings: [],
    errors: []
  };
}
