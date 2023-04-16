import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View, SafeAreaView } from "react-native";
import * as Font from "expo-font";
import { Inter_500Medium } from "@expo-google-fonts/inter";
import * as SplashScreen from "expo-splash-screen";
import { useCallback, useEffect, useState } from "react";
import { LinearGradient } from "expo-linear-gradient";
import { NavigationContainer, DefaultTheme } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { NativeRouter, Route, Routes } from "react-router-native";
import Home from "./components/Home";
import { PlayerPanel } from "./components/PlayerPanel";

const Stack = createNativeStackNavigator();
const navTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: "transparent",
  },
};

export default function App() {
  const [appIsReady, setAppIsReady] = useState(false);

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
      colors={["#CAF2FD", "#b2d3db"]}
    >
      <SafeAreaView>
        <View style={styles.container} onLayout={onLayout}>
          <StatusBar style="auto" />
          <Text style={styles.text}>NBA Player Stats Predictor</Text>
          <NavigationContainer theme={navTheme}>
            <Stack.Navigator
              options={{
                headerShown: false,
                animation: "none",
              }}
            >
              <Stack.Screen
                name="Home"
                component={Home}
                options={{
                  animation: "none",
                  headerShown: false,
                }}
              />
              <Stack.Screen
                name="PlayerPanel"
                component={PlayerPanel}
                options={{
                  headerShown: false,
                  animation: "none",
                }}
              />
            </Stack.Navigator>
          </NavigationContainer>
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
