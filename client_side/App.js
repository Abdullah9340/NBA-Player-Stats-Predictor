import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View, SafeAreaView } from "react-native";
import * as Font from "expo-font";
import { Inter_500Medium } from "@expo-google-fonts/inter";
import * as SplashScreen from "expo-splash-screen";
import { useCallback, useEffect, useState } from "react";
import SearchBar from "./components/SearchBar";
import { LinearGradient } from "expo-linear-gradient";
import { NBAPlayer } from "./components/Class";
import axios from "axios";

export default function App() {
  const [appIsReady, setAppIsReady] = useState(false);
  const [NBAPlayers, setNBAPlayers] = useState([]);

  useEffect(() => {
    async function prepare() {
      try {
        await SplashScreen.preventAutoHideAsync();
        await Font.loadAsync({ Inter_500Medium });
        await new Promise((resolve) => setTimeout(resolve, 2000));
      } catch {
        // handle error
      } finally {
        setAppIsReady(true);
      }
    }
    prepare();
  }, []);

  // useEffect(() => {
  //   axios
  //     .get(`http://192.168.2.15:5000/predict_season_stats/Lebron_James`)
  //     .then((res) => {
  //       console.log(res.data);
  //     })
  //     .catch((err) => {
  //       console.log(err);
  //     });
  // }, []);

  const onLayout = useCallback(() => {
    if (appIsReady) {
      SplashScreen.hideAsync();
    }
  }, [appIsReady]);

  if (!appIsReady) {
    return null;
  }

  return (
    <LinearGradient
      // Button Linear Gradient
      colors={["#CAF2FD", "#FFFFFF"]}
    >
      <SafeAreaView>
        <View style={styles.container} onLayout={onLayout}>
          <StatusBar style="auto" />
          <Text style={styles.text}>NBA Player Stats Predictor</Text>
          <SearchBar setNBAPlayers={setNBAPlayers} />
          {NBAPlayers.map((player, index) => (
            <Text key={index}>{player}</Text>
          ))}
        </View>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 10,
    height: "100%",
  },
  text: {
    fontFamily: "Inter_500Medium",
    textAlign: "center",
    fontSize: "24px",
  },
  backgroundColor: {
    backgroundColor: "#FCEFE3",
    height: "100%",
  },
});
