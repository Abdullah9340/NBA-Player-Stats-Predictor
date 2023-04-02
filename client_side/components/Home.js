import { StyleSheet, Text, View } from "react-native";
import { useState } from "react";
import SearchBar from "./SearchBar";
import { ArrowSmallRightIcon } from "react-native-heroicons/outline";

export default function HomePage() {
  const [NBAPlayers, setNBAPlayers] = useState([]);

  return (
    <View>
      <SearchBar setNBAPlayers={setNBAPlayers} />
      <View style={styles.searchResultsContainer}>
        {NBAPlayers.map((player, index) => (
          <View style={styles.searchResult} key={index}>
            <Text style={styles.searchResultText}>{player}</Text>
            <ArrowSmallRightIcon />
          </View>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  searchResultsContainer: {
    display: "flex",
    flexDirection: "column",
    width: "100%",
    marginLeft: "auto",
  },
  searchResultText: {
    fontSize: "18px",
    color: "gray",
  },
  searchResult: {
    borderBottomColor: "black",
    borderBottomWidth: 1,
    padding: 10,
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
  },
});
