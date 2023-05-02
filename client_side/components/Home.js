import { StyleSheet, Text, View, TouchableOpacity } from "react-native";
import { useState } from "react";
import SearchBar from "./SearchBar";
import { ArrowSmallRightIcon } from "react-native-heroicons/outline";
import { getPlayerCode } from "../utils/PlayerSuffix";
import { useNavigation } from "@react-navigation/native";

export default function HomePage() {
  const [NBAPlayers, setNBAPlayers] = useState([]);
  const navigation = useNavigation();

  return (
    <View>
      <SearchBar setNBAPlayers={setNBAPlayers} />
      <View style={styles.searchResultsContainer}>
        {NBAPlayers.map((player, index) => (
          <TouchableOpacity
            onPress={async () => {
              navigation.navigate("PlayerPanel", {
                id: await getPlayerCode(player),
                name: player,
              });
              // console.log(await getPlayerCode(player));
            }}
            key={index}
          >
            <View style={styles.searchResult}>
              <Text style={styles.searchResultText}>{player}</Text>
              <ArrowSmallRightIcon />
            </View>
          </TouchableOpacity>
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
