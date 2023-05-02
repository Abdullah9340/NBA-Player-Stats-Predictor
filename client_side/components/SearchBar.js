import { StyleSheet, View, Text, TouchableOpacity } from "react-native";
import { Input } from "galio-framework";
import player_names from "../utils/player_names.js";

export default function SearchBar(props) {
  const playerNames = player_names.split("\n");

  const getSuggestions = (value) => {
    const inputValue = value.trim();
    // Find prefixs in playerNames array that match inputValue
    const inputLength = inputValue.length;
    if (inputLength === 0) return [];
    let suggestions = playerNames;
    suggestions = suggestions
      .filter(
        (playerName) =>
          playerName.slice(0, inputLength).toLowerCase() ===
          inputValue.toLowerCase()
      )
      .splice(0, 10);
    return suggestions;
  };

  const onSearch = (value) => {
    props.setNBAPlayers(getSuggestions(value));
  };

  return (
    <View style={styles.container}>
      <Input
        placeholder="Search for a player!"
        style={styles.search}
        onChangeText={(text) => onSearch(text)}
      />
      <TouchableOpacity onPress={props.openPopup}>
        <View style={styles.button}>
          <Text style={styles.buttonText}>Search</Text>
        </View>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginTop: 20,
    width: "100%",
    display: "flex",
    flexDirection: "row",
    alignContent: "center",
    justifyContent: "center",
  },
  search: {
    minWidth: "65%",
    marginLeft: "auto",
    height: 40,
  },
  button: {
    height: 40,
    display: "flex",
    justifyContent: "center",
    marginLeft: 10,
  },
  buttonText: {
    marginTop: 10,
    color: "blue",
    fontFamily: "Inter_500Medium",
    fontSize: 16,
  },
});
