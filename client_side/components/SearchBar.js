import { StyleSheet, View, TextInput, Button } from "react-native";
import { Input, Block } from "galio-framework";

export default function SearchBar() {
  return (
    <View style={styles.container}>
      <Input placeholder="Search for a player!" style={styles.search} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: "100%",
  },
  search: {
    width: "80%",
    marginLeft: "auto",
    marginRight: "auto",
  },
});
