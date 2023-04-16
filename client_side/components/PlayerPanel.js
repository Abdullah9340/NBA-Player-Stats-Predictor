import { View, Text, Image } from "react-native";

export function PlayerPanel({ route }) {
  const { id, name } = route.params;
  const imagePart = id.split("/")[1];
  console.log(imagePart);
  return (
    <View>
      <Image
        style={{ width: 100, height: 100 }}
        source={{
          uri: `https://www.basketball-reference.com/req/202106291/images/players/${imagePart}.jpg`,
        }}
      />
      <Text>{name}</Text>
    </View>
  );
}
