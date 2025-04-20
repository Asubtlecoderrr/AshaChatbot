SERPAPI_KEY = "3237d985f10df42f6e578b99a5966ff84131358dae814931afd18373384e28a9"

class SerpApiCommunitySearcher:
    def search_communities(self, topic, count=5):
        """
        Search for online communities related to a specific topic and return direct links.

        Args:
            topic (str): Topic to search for communities about.
            count (int): Number of results to fetch.

        Returns:
            list: Communities related to the topic with links and brief descriptions.
        """
        try:
            url = "https://serpapi.com/search"

            # Search query to find online communities (forums, groups, etc.)
            search_query = f"{topic} community OR forum OR group"

            params = {
                "engine": "google",
                "q": search_query,
                "api_key": SERPAPI_KEY,
                "num": count,
            }

            response = requests.get(url, params=params, verify=False)
            data = response.json()

            # Define community platforms to filter
            community_platforms = ['linkedin.com', 'facebook.com', 'slack.com', 'telegram.org', 'discord.com', 'reddit.com']

            results = []
            for item in data.get("organic_results", [])[:count]:
                # Filter results that match community platforms
                link = item.get("link", "")
                if any(platform in link for platform in community_platforms):
                    community = {
                        "title": item.get("title", "No title"),
                        "description": item.get("snippet", ""),
                        "link": link,
                        "platform": item.get("displayed_link", ""),
                        "is_community_search_result": True
                    }
                    results.append(community)

            return results

        except Exception as e:
            print(f"SerpAPI community search error: {e}")
            return []

class CommunitySearchAgent:
    def _init_(self):
        self.searcher = SerpApiCommunitySearcher()

    def find_communities(self, topic, count=5):
        return self.searcher.search_communities(topic, count)

# =========================
# 🎯 Example Runner
# =========================
if _name_ == "_main_":
    agent = CommunitySearchAgent()

    # Get user input for the topic to search communities
    topic = input("Enter the topic (e.g., women in tech, data engineering): ").strip()

    # Fetch communities for the given topic
    print(f"\n==== Communities for '{topic}' ====")
    results = agent.find_communities(topic=topic, count=5)

    # Display the results in the clean format
    communities = []
    for result in results:
        communities.append({
            "title": result['title'],
            "description": result['description'],
            "link": result['link'],
            "platform": result['platform'],
        })

    # Print out the clean result in JSON format for better visibility
    print(json.dumps(communities, indent=4))