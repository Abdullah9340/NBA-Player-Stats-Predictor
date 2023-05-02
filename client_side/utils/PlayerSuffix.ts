import axios from "axios";
import { load } from "cheerio";

const LOOK_UP_URL: string = "https://basketball-reference.com/players/{0}.html";
const cache = {};

export async function getPlayerCode(
  player_name: string
): Promise<string | null> {
  try {
    if (cache[player_name]) {
      console.log("using cache")
      return cache[player_name];
    }
    const [first_name, last_name] = player_name.split(" ");
    const prefix = last_name.slice(0, 5).toLowerCase();
    const suffix = first_name.slice(0, 2).toLowerCase();
    const option1 = `${prefix[0]}/${prefix}${suffix}01`;
    const option2 = `${prefix[0]}/${prefix}${suffix}02`;

    // Try Option 1
    const response1 = await axios.get(LOOK_UP_URL.replace("{0}", option1));
    const $1 = load(response1.data);
    const found_name1 = $1("h1 span").text();
    if (found_name1.toLowerCase() === player_name.toLowerCase()) {
      cache[player_name] = option1;
      return option1;
    }

    // Try Option 2
    const response2 = await axios.get(LOOK_UP_URL.replace("{0}", option2));
    const $2 = load(response2.data);
    const found_name2 = $2("h1 span").text();
    if (found_name2.toLowerCase() === player_name.toLowerCase()) {
      cache[player_name] = option2;
      return option2;
    }

    // Player not found
    cache[player_name] = null;
    return null;
  } catch (e) {
    return null;
  }
}
