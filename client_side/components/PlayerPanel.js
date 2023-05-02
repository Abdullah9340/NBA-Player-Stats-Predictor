import React, { useState, useEffect } from "react";
import { View, Text, Image, TouchableOpacity } from "react-native";

export function PlayerCard({ route }) {
  const { id, name } = route.params;
  const headshot = `https://www.basketball-reference.com/req/202106291/images/players/${
    id.split("/")[1]
  }.jpg`;

  const [showPrediction, setShowPrediction] = useState(false);
  const [careerStats, setCareerStats] = useState({
    points: 0,
    rebounds: 0,
    assists: 0,
  });

  const [gamePrediction, setGamePrediction] = useState({
    points: 0,
    rebounds: 0,
    assists: 0,
  });

  const [seasonPrediction, setSeasonPrediction] = useState({
    points: 0,
    rebounds: 0,
    assists: 0,
  });

  useEffect(() => {
    fetch(process.env.API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name.trim(),
        action: "career_stats",
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        const dataArray = JSON.parse(data["data"]);
        setCareerStats({
          points: dataArray[dataArray.length - 1]["PTS"],
          rebounds: dataArray[dataArray.length - 1]["TRB"],
          assists: dataArray[dataArray.length - 1]["AST"],
        });
        // Do something with the response data here
      })
      .catch((error) => {
        console.error("There was a problem with the network request:", error);
      });
  }, []);

  const handlePredictionClick = async () => {
    setShowPrediction(true);

    fetch(process.env.API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        action: "predict",
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Round each value to 1 decimal place
        let dataNew = JSON.parse(data["data"]);
        setGamePrediction({
          points: dataNew["Game Predict"]["Points"].toFixed(1),
          rebounds: dataNew["Game Predict"]["Rebounds"].toFixed(1),
          assists: dataNew["Game Predict"]["Assists"].toFixed(1),
        });

        setSeasonPrediction({
          points: dataNew["Season Predict"]["Points"].toFixed(1),
          rebounds: dataNew["Season Predict"]["Rebounds"].toFixed(1),
          assists: dataNew["Season Predict"]["Assists"].toFixed(1),
        });
      })
      .catch((error) => {
        console.error("There was a problem with the network request:", error);
      });
  };

  return (
    <View
      style={{
        padding: 20,
        backgroundColor: "#fff",
        borderRadius: 10,
        margin: 10,
      }}
    >
      <View style={{ flexDirection: "row", alignItems: "center" }}>
        <Image
          source={{ uri: headshot }}
          style={{ width: 80, height: 80, borderRadius: 40, marginRight: 10 }}
        />
        <View>
          <Text style={{ fontSize: 24, fontWeight: "bold" }}>{name}</Text>
          <Text
            style={{ fontSize: 16 }}
          >{`${careerStats.points} PPG / ${careerStats.rebounds} RPG / ${careerStats.assists} APG`}</Text>
        </View>
      </View>
      <TouchableOpacity
        style={{ marginTop: 20 }}
        onPress={handlePredictionClick}
      >
        <Text style={{ fontSize: 18, fontWeight: "bold", color: "#007AFF" }}>
          Predict Next Game
        </Text>
      </TouchableOpacity>
      {showPrediction && (
        <View>
          <View style={{ marginTop: 20 }}>
            <Text style={{ fontSize: 18, fontWeight: "bold" }}>
              Predicted Stats For Season
            </Text>
            <View style={{ marginTop: 10 }}>
              <Text
                style={{ fontSize: 16 }}
              >{`${seasonPrediction.points} PPG / ${seasonPrediction.rebounds} RPG / ${seasonPrediction.assists} APG`}</Text>
            </View>
          </View>
          <View style={{ marginTop: 20 }}>
            <Text style={{ fontSize: 18, fontWeight: "bold" }}>
              Predicted Stats For Next Game
            </Text>
            <View style={{ marginTop: 10 }}>
              <Text
                style={{ fontSize: 16 }}
              >{`${gamePrediction.points} Points / ${gamePrediction.rebounds} Rebounds / ${gamePrediction.assists} Assists`}</Text>
            </View>
          </View>
        </View>
      )}
    </View>
  );
}
