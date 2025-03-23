from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.tools import BaseTool, tool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field
from typing import Optional
import requests
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=os.getenv('GEMINI_API_KEY'))

# TOOL 1: Tavily Search

search_tool = TavilySearch(
    max_results=5,
    topic="general"
)

# TOOL 2: Weather API

class Place(BaseModel):
    place: str = Field(description="place")

class WeatherTool(BaseTool):
    name: str = "weather_tool"
    description: str = "A tool to fetch current weather details given a place."
    args_schema: Optional[ArgsSchema] = Place

    def _run(self, place: str):
        """Use the tool to hit weather endpoint and fetch current weather details given a place"""
        api_key = os.getenv('WEATHERBIT_API_KEY')
        url = f"https://api.weatherbit.io/v2.0/current?city={place}&key={api_key}"
        response = requests.get(url)
        return response.json()
    
getweather_tool = WeatherTool()
    
# @tool
# def weather_tool(place: str):
#     """A tool to fetch weather details given a place."""
#     api_key = os.getenv('GPLACES_API_KEY')
#     url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={api_key}"
#     response = requests.post(url)
#     return response.json()


# TOOL 3: News API

class NewsTool(BaseTool):
    name: str = "news_tool"
    description: str = "A tool to perform news search about a given place."
    args_schema: Optional[ArgsSchema] = Place

    def _run(self, place: str):
        """Use the tool to hit news endpoint and fetch any related news about a given place"""
        api_key = os.getenv('GNEWS_API_KEY')
        url = f"https://gnews.io/api/v4/search?q={place}&apikey={api_key}"
        response = requests.get(url)
        return response.json()
    
getnews_tool = NewsTool()
    
# TOOL 4: Places API

class PlaceTool(BaseTool):
    name: str = "places_tool"
    description: str = "A tool to hit Google Places API. Useful for when you need place details from a query."
    args_schema: Optional[ArgsSchema] = Place

    def _run(self, place: str):
        """Use the tool to hit google places endpoint and fetch details given a place"""
        api_key = os.getenv('GPLACES_API_KEY')
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={api_key}"
        response = requests.get(url)
        return response.json()
    
getplaces_tool = PlaceTool()

tools = [getnews_tool, getplaces_tool, search_tool, getweather_tool] 

agent = create_react_agent(
    llm,
    tools,
    state_modifier=(
        "You are a travel planner, Cassandra, that collates all the current information about a given place such as address details, current news, weather information and any related online result about the place."
        "Your response MUST have positive and negative points regarding travelling to the place along with your recommendation to travel or not."
        "Include top things to do or visit."
        "You MUST only respond precisely in 100 words."
    )
)

def invoke_agent(user_input):
    response = agent.invoke({"messages": [("human", user_input)]})
    return response["messages"][-1].content



# {'messages': [
#     HumanMessage(content='I want to travel to Dubai in the month of July 2025.', additional_kwargs={}, response_metadata={}, id='e67d7446-4e1a-49ad-aafe-773c9debdff0'), 
#     AIMessage(content='', additional_kwargs={'function_call': {'name': 'tavily_search', 'arguments': '{"query": "tourism in Dubai"}'}}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'safety_ratings': []}, id='run-b7b0eb71-0756-42b8-b49b-87ef0ba1a80d-0', tool_calls=[{'name': 'places_tool', 'args': {'place': 'Dubai'}, 'id': '26c31ec4-8ecf-4dae-b8f5-2d8e59d0ab28', 'type': 'tool_call'}, {'name': 'news_tool', 'args': {'place': 'Dubai'}, 'id': 'd3519a55-9612-481c-9330-ae9d6e6b09b1', 'type': 'tool_call'}, {'name': 'weather_tool', 'args': {'place': 'Dubai'}, 'id': '8aa0b78c-c26e-48bb-a032-0aabd2864155', 'type': 'tool_call'}, {'name': 'tavily_search', 'args': {'query': 'tourism in Dubai'}, 'id': 'fb28defe-ea8f-42ce-b6c2-28ac3e8acd75', 'type': 'tool_call'}], usage_metadata={'input_tokens': 615, 'output_tokens': 23, 'total_tokens': 638, 'input_token_details': {'cache_read': 0}}), 
#     ToolMessage(content='{"results": [{"address_components": [{"long_name": "Dubai", "short_name": "Dubai", "types": ["locality", "political"]}, {"long_name": "Dubai", "short_name": "Dubai", "types": ["administrative_area_level_1", "political"]}, {"long_name": "United Arab Emirates", "short_name": "AE", "types": ["country", "political"]}], "formatted_address": "Dubai - United Arab Emirates", "geometry": {"bounds": {"northeast": {"lat": 25.3585607, "lng": 55.5645216}, "southwest": {"lat": 24.7934842, "lng": 54.89045429999999}}, "location": {"lat": 25.2048493, "lng": 55.2707828}, "location_type": "APPROXIMATE", "viewport": {"northeast": {"lat": 25.3585607, "lng": 55.5645216}, "southwest": {"lat": 24.7934842, "lng": 54.89045429999999}}}, "place_id": "ChIJRcbZaklDXz4RYlEphFBu5r0", "types": ["locality", "political"]}], "status": "OK"}', name='places_tool', id='da9ba212-f09d-4a5b-a173-f4995515d9a4', tool_call_id='26c31ec4-8ecf-4dae-b8f5-2d8e59d0ab28'), 
#     ToolMessage(content='{"totalArticles": 39378, "articles": [{"title": "Facteur Cheval and Ghostwriter camps excited to take on hot favourite Romantic Warrior in Dubai Turf", "description": "Romantic Warrior will head into the $5 million Dubai Turf a week on Saturday as an overwhelming favourite, but the presence of Hong Kong\'s global... Read More", "content": "Romantic Warrior will head into the $5 million Dubai Turf a week on Saturday as an overwhelming favourite, but the presence of Hong Kong\'s global star has done little to dissuade connections of several top-class international rivals from taking their... [441 chars]", "url": "https://www.racingpost.com/news/international/uae/facteur-cheval-and-ghostwriter-camps-excited-to-take-on-hot-favourite-romantic-warrior-in-dubai-turf-adQ1E1y0NEqa/", "image": "https://media.racingpost.gcpp.io/prod/images/gm_preview/b62aedd89303-facteur-cheval.jpeg", "publishedAt": "2025-03-22T17:00:00Z", "source": {"name": "Racing Post", "url": "https://www.racingpost.com"}}, {"title": "Wathnan and Tom Clover opt for US target over Dubai World Cup night invite for talented sprinter", "description": "Classy sprinter Rogue Lightning is set for a first US assignment in the wake of his overseas success in the Wathnan colours in Qatar last month. The... Read More", "content": "Classy sprinter Rogue Lightning is set for a first US assignment in the wake of his overseas success in the Wathnan colours in Qatar last month.\\nThe five-year-old was a breakthrough first winner for the Qatari operation in the international races at ... [2184 chars]", "url": "https://www.racingpost.com/news/international/us/wathnan-and-tom-clover-opt-for-us-target-over-dubai-world-cup-night-invite-for-talented-sprinter-abZSG0U5MUNM/", "image": "https://media.racingpost.gcpp.io/prod/images/gm_preview/0f0594c35c50-rogue-lightning.jpg", "publishedAt": "2025-03-22T16:07:25Z", "source": {"name": "Racing Post", "url": "https://www.racingpost.com"}}, {"title": "Tommy Fury and Molly-Mae Hague fuel reunion rumours after \'returning from Dubai trip together\'", "description": "The former Love Island stars were seen together at Manchester Airport", "content": "Tommy Fury and Molly-Mae Hague fuel reunion rumours after \'returning from Dubai trip together\'\\nThe former Love Island stars were seen together at Manchester Airport\\nMolly-Mae Hague and Tommy Fury (Image: Instagram )\\nTommy Fury and Molly-Mae Hague hav... [2657 chars]", "url": "https://www.birminghammail.co.uk/news/showbiz-tv/tommy-fury-molly-mae-hague-31259638", "image": "https://i2-prod.birminghammail.co.uk/article31204589.ece/ALTERNATES/s1200/0_Tommy-Fury-says-daughter-Bambi-has-been-keeping-him-going-as-he-opens-up-about-tough-year-follow.jpg", "publishedAt": "2025-03-22T14:30:24Z", "source": {"name": "Birmingham Live", "url": "https://www.birminghammail.co.uk"}}, {"title": "Diebstahlschutz: Darum steckt Pistaziencreme in Plastikbox", "description": "Pistaziencreme ist der Renner, seit sie in der viralen Dubai-Schoggi verwendet wird. Doch der Hype hat auch seine Schattenseiten: In Deutschland greifen Läden zu drastischen Massnahmen.", "content": "Pistaziencreme braucht es zur Herstellung der Dubai-Schoggi. Ein Glas kostet weniger als fünf Franken. Trotzdem steckt es in manchen Läden in einer Plastikkassette.\\nHype-Produkt : «Wo sind wir hier?» DM schützt Pistaziencreme mit Warensicherung\\nPista... [2953 chars]", "url": "https://www.20min.ch/story/hype-produkt-wo-sind-wir-hier-dm-schuetzt-pistaziencreme-mit-warensicherung-103307570", "image": "https://image.20min.ch/2025/03/22/3a04c16d-8f10-4a17-b280-ac76d38b5c07.jpeg?auto=format%2Ccompress%2Cenhance&fit=crop&w=1200&h=675&rect=0%2C0%2C827%2C572&crop=faces&s=b0ca4697b95319112c4cee0f44a6c16b", "publishedAt": "2025-03-22T14:28:48Z", "source": {"name": "20 Minuten", "url": "https://www.20min.ch"}}, {"title": "Lindt\'s viral chocolate bar that sold out in December coming to these high street supermarkets", "description": "Lindt’s Dubai-style chocolates are returning with some new variations", "content": "Lindt\'s viral chocolate bar that sold out in December coming to these high street supermarkets\\nLindt’s Dubai-style chocolates are returning with some new variations\\nThe chocolate pistachio nuts and milk chocolate topped with a crunchy Kadayif pastry ... [2390 chars]", "url": "https://www.liverpoolecho.co.uk/whats-on/food-drink-news/lindts-viral-chocolate-bar-sold-31259396", "image": "https://i2-prod.liverpoolecho.co.uk/article31259322.ece/ALTERNATES/s1200/0_Dubai-style-chocolate-bar.jpg", "publishedAt": "2025-03-22T13:40:50Z", "source": {"name": "Liverpool Echo", "url": "https://www.liverpoolecho.co.uk"}}, {"title": "OnlyFans model, 20, \'found in Dubai with broken spine and limbs\'", "description": "Her mother has issued an update on her health", "content": "OnlyFans model, 20, \'found in Dubai with broken spine and limbs\'\\nHer mother has issued an update on her health\\nAn OnlyFans model has been left injured in Dubai\\nAn OnlyFans model reportedly suffered serious injuries in Dubai after attending a fetish p... [2682 chars]", "url": "https://www.birminghammail.co.uk/news/world-news/onlyfans-model-20-found-dubai-31259417", "image": "https://i2-prod.birminghammail.co.uk/article30246324.ece/ALTERNATES/s1200/0_dubai.jpg", "publishedAt": "2025-03-22T13:16:01Z", "source": {"name": "Birmingham Live", "url": "https://www.birminghammail.co.uk"}}, {"title": "I tried Lidl Ireland\'s viral Dubai chocolate bar that has shoppers rushing to tills to try it - and it costs just €5", "description": "LIDL Ireland has sent chocolate lovers into a frenzy with a new Dubai-style chocolate bar.And with shoppers scrambling to get their hands on the dupe", "content": "LIDL Ireland has sent chocolate lovers into a frenzy with a new Dubai-style chocolate bar.\\nAnd with shoppers scrambling to get their hands on the dupe bar, we decided to put it to the test.\\n5 The supermarket chocolate did not disappoint Credit: COLLE... [2906 chars]", "url": "https://www.thesun.ie/fabulous/14921153/lidl-ireland-viral-dubai-chocolate-dupe-rushing-tills-euro/", "image": "https://www.thesun.ie/wp-content/uploads/sites/3/2025/03/MixCollage-22-Mar-2025-09-59-AM-9163.jpg?strip=all&quality=100&w=1920&h=1080&crop=1", "publishedAt": "2025-03-22T09:57:34Z", "source": {"name": "The Irish Sun", "url": "https://www.thesun.ie"}}, {"title": "Vermisstes ukrainisches Model in Dubai nach Party brutal zugerichtet aufgefunden", "description": "Schock-Fund in Dubai: Ein vermisstes ukrainisches Model (20) wurde nach einer Hotelparty brutal zugerichtet und mit gebrochenen Knochen am Straßenrand entdeckt. | TAG24", "content": "Dubai - Schock-Fund in Dubai : Ein vermisstes ukrainisches Model (20) wurde nach einer Hotelparty brutal zugerichtet und mit gebrochenen Knochen am Straßenrand entdeckt.\\nMaria Kovalchuk (20) wollte eigentlich weiter nach Thailand fliegen, doch dazu k... [590 chars]", "url": "https://www.tag24.de/thema/aus-aller-welt/vermisstes-ukrainisches-model-in-dubai-nach-party-brutal-zugerichtet-aufgefunden-3370066", "image": "https://media.tag24.de/1200x800/s/n/sn11ye9u7voqkly3dmwr5t4n6zxy8n30.jpg", "publishedAt": "2025-03-22T08:15:02Z", "source": {"name": "TAG24", "url": "https://www.tag24.de"}}, {"title": "Wie Dubai-Schokolade, nur besser - Kinder Country selbst gemacht", "description": "Mit diesem Rezept zaubern Sie die beliebte Kinder-Country-Schokolade schnell und einfach selbst. Perfekt für Geburtstage oder als süßer Snack für zwischendurch.", "content": "Wie Dubai-Schokolade, nur besser – Kinder Country selbst gemacht\\nVon: Cosima Baumann\\nDrucken Teilen\\nMit diesem Rezept zaubern Sie die beliebte Kinder-Country-Schokolade schnell und einfach selbst. Perfekt für Geburtstage oder als süßer Snack für zwis... [3884 chars]", "url": "https://www.tz.de/leben/einfach-tasty/wie-dubai-schokolade-nur-besser-kinder-country-selbst-gemacht-zr-93639431.html", "image": "https://www.tz.de/assets/images/37/504/37504482-wie-dubai-schokolade-nur-besser-kinder-country-schokolade-selbst-gemacht-3y0XjLFYhWfe.jpg", "publishedAt": "2025-03-22T06:00:00Z", "source": {"name": "tz.de", "url": "https://www.tz.de"}}, {"title": "Wie Dubai-Schokolade, nur besser - Kinder Country selbst gemacht", "description": "Mit diesem Rezept zaubern Sie die beliebte Kinder-Country-Schokolade schnell und einfach selbst. Perfekt für Geburtstage oder als süßer Snack für zwischendurch.", "content": "Wie Dubai-Schokolade, nur besser – Kinder Country selbst gemacht\\nVon: Cosima Baumann\\nDrucken Teilen\\nMit diesem Rezept zaubern Sie die beliebte Kinder-Country-Schokolade schnell und einfach selbst. Perfekt für Geburtstage oder als süßer Snack für zwis... [3884 chars]", "url": "https://www.fr.de/ratgeber/einfach-tasty/wie-dubai-schokolade-nur-besser-kinder-country-selbst-gemacht-zr-93639431.html", "image": "https://www.fr.de/assets/images/37/504/37504482-wie-dubai-schokolade-nur-besser-kinder-country-schokolade-selbst-gemacht-3y0XjLFYhWfe.jpg", "publishedAt": "2025-03-22T06:00:00Z", "source": {"name": "fr.de", "url": "https://www.fr.de"}}]}', name='news_tool', id='ecca721d-9ed4-45ef-811a-43a69492f309', tool_call_id='d3519a55-9612-481c-9330-ae9d6e6b09b1'), 
#     ToolMessage(content='{"count": 1, "data": [{"app_temp": 27.5, "aqi": 67, "city_name": "Dubai", "clouds": 72, "country_code": "AE", "datetime": "2025-03-23:05", "dewpt": 4.5, "dhi": 114, "dni": 893, "elev_angle": 47.59, "ghi": 766, "gust": null, "h_angle": -45, "lat": 25.0657, "lon": 55.17128, "ob_time": "2025-03-23 05:42", "pod": "d", "precip": 0, "pres": 1014.8, "rh": 21, "slp": 1017, "snow": 0, "solar_rad": 565.4, "sources": ["OMDW", "radar", "satellite"], "state_code": "03", "station": "OMDW", "sunrise": "02:18", "sunset": "14:32", "temp": 29, "timezone": "Asia/Dubai", "ts": 1742708561, "uv": 3, "vis": 16, "weather": {"description": "Broken clouds", "code": 803, "icon": "c03d"}, "wind_cdir": "SSW", "wind_cdir_full": "south-southwest", "wind_dir": 210, "wind_spd": 2.6}]}', name='weather_tool', id='f4b5a174-7f6f-4ffb-b891-40ffee995ee2', tool_call_id='8aa0b78c-c26e-48bb-a032-0aabd2864155'), 
#     ToolMessage(content='{"query": "tourism in Dubai", "follow_up_questions": null, "answer": null, "images": [], "results": [{"title": "Tourism in Dubai - Wikipedia", "url": "https://en.wikipedia.org/wiki/Tourism_in_Dubai", "content": "The Al Fahidi Historical Neighbourhood, also called Al Bastakiya, is Dubai\'s historic district and major tourist destination.. Tourism in Dubai is a major part of the economy of Dubai.Dubai was the third most visited city in the world in 2023 with 17 million international visitors according to Euromonitor International. [1] [2] Dubai hosts more than 800 hotels with more than 150,000 rooms.", "score": 0.93206495, "raw_content": null}, {"title": "Visit Dubai - Official Tourism Board in Dubai", "url": "https://www.visitdubai.com/", "content": "Planning a trip to Dubai? Explore Dubai Dubai Interactive MapDiscover nearby events, top attractions, restaurants and more Deals in Dubai Wellness in DubaiPlan an active holiday with wellness experiences in Dubai 99 things to do in Dubai Restaurants in DubaiDiscover Dubai\'s top dining experiences with our restaurant guide FlightsUse our tool to book flight tickets to Dubai and plan your trip to the city Dubai attractions passesUnlock huge savings with pre-paid access to top spots Discover Dubai\'s best new hotels and upcoming hotel launches in 2025 Attraction dealsSave big with great offers on Dubai\'s top sights and activities Dubai Calendar ### Save up to 60% with the Dubai Pass Experience all that\'s possible with the Dubai Pass.", "score": 0.4526091, "raw_content": null}, {"title": "Top Things to Do in Dubai - Visit Dubai", "url": "https://www.visitdubai.com/en/things-to-do", "content": "Dubai is particularly famous for its eye-catching landmarks, including Burj Khalifa (the world\'s tallest building), Dubai Mall, The Dubai Fountain, Burj Al Arab, Palm Jumeirah (a man-made island in the shape of a palm tree) and more.The latest addition to the skyline is the stunning Museum of the Future.Dubai is also known for its picturesque beaches and desert landscapes, as well as its", "score": 0.42749292, "raw_content": null}, {"title": "THE 15 BEST Things to Do in Dubai (2025) - Must-See Attractions", "url": "https://www.tripadvisor.com/Attractions-g295424-Activities-Dubai_Emirate_of_Dubai.html", "content": "LIKELY TO SELL OUT* Dubai Full Day Tour with Entry Ticket to Burj Khalifa at the Top 306 Likely To Sell Out from $143 per adult Burj Khalifa At the Top Observation Deck Admission Ticket Dubai 23 Ports of Call Tours from $53 per adult (price varies by group size) SPECIAL OFFER Abu Dhabi City Tour Including Ferrari World Tickets from Dubai 439 Private and Luxury from ~$224~ $180 per adult SPECIAL OFFER Abu Dhabi City Tour Including Ferrari World Tickets from Dubai 439 Private and Luxury from ~$224~ $180 per adult SPECIAL OFFER Abu Dhabi City Tour Including Ferrari World Tickets from Dubai 439 Private and Luxury from ~$224~ $180 per adult", "score": 0.36303747, "raw_content": null}, {"title": "19 Best Things to Do in Dubai | U.S. News Travel", "url": "https://travel.usnews.com/Dubai_United_Arab_Emirates/Things_To_Do/", "content": "19 Best Things to Do in Dubai | U.S. News Travel Dubai Full Day Tour with Entry Ticket to Burj Khalifa at the Top (863 reviews) from $143.00 Read More U.S. News Insider Tip: Two of the best ways to get a look at Palm Jumeirah are from beyond: a jump with Skydive Dubai offers unparalleled views of the \\"tree\\" while an afternoon yacht excursion can take you around the perimeter in style. U.S. News Insider Tip: Two of the best ways to get a look at Palm Jumeirah are from beyond: a jump with Skydive Dubai offers unparalleled views of the \\"tree\\" while an afternoon yacht excursion can take you around the perimeter in style.", "score": 0.2651513, "raw_content": null}], "response_time": 1.51}', name='tavily_search', id='d0b997b3-4154-4892-900e-a5ac9deacf01', tool_call_id='fb28defe-ea8f-42ce-b6c2-28ac3e8acd75'), 
#     AIMessage(content='Dubai in July 2025 promises dazzling attractions and luxurious experiences. The city boasts world-class landmarks like the Burj Khalifa and vibrant cultural districts. However, be prepared for intense heat, with average temperatures around 42°C (108°F) and high humidity, which can make outdoor activities uncomfortable. Recent news highlights ongoing tourism developments and events.\n\nRecommendation: If you can tolerate extreme heat and plan to spend most of your time indoors, Dubai can be an exciting destination. Otherwise, consider visiting during the cooler months for a more enjoyable experience.', additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'safety_ratings': []}, id='run-79393411-2d0a-4eb2-8aa7-ad61de16699b-0', usage_metadata={'input_tokens': 4353, 'output_tokens': 117, 'total_tokens': 4470, 'input_token_details': {'cache_read': 0}})
# ]}