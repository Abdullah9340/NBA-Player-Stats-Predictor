# NBA-Player-Stats-Predictor

Checkout the application on Expo Go here (Download the Expo Go App First): <br />
https://expo.dev/@abdullah9430/nba_predictor?serviceType=classic&distribution=expo-go

# Info

- React Native application to search for NBA players, view their current season stats, and generate predictions for future stats
- Uses a Baysian regreesion model from SciKit learn to make predictions
- Backend functions hosted using GCP cloud functions combined with a PostgreSQL database to cache results
- Accounted for a players "hot streak" by using a weighted average of their last 10 games as a part of the prediction algorithim
- Built a web scraper in Python using Beautiful Soup to scrape NBA player info and pictures from basketball reference

# Images

Loading Screen: <br />
<img src="https://user-images.githubusercontent.com/72326930/235766929-5e2372d3-65d5-44bc-b98c-82d71e8584b5.png" width="100" /> 

Search Bar: <br />
<img src="https://user-images.githubusercontent.com/72326930/235767244-b9480a25-b31a-4815-a3f3-d70ee34f6f8f.png" width="100" /> 

Player Card: <br />
<img src="https://user-images.githubusercontent.com/72326930/235767375-d13648c6-fe17-4e39-943b-8f9885ef36ad.png" width="100" /> 

Player Prediction: <br />
<img src="https://user-images.githubusercontent.com/72326930/235767451-6d9ab061-83f1-4e17-bd68-971400fdf823.png" width="100" /> 

