import random
from datetime import datetime, timedelta

# Sample data for generating random news
TECH_COMPANIES = ["Apple", "Google", "Microsoft", "Amazon", "Meta", "Tesla", "SpaceX", "Netflix", "IBM", "Intel"]
TECH_PRODUCTS = ["smartphone", "laptop", "AI assistant", "smart home device", "VR headset", "electric vehicle", "robot", "drone", "wearable device"]
TECH_ACTIONS = ["launches", "announces", "unveils", "releases", "develops", "patents", "acquires", "partners with", "invests in"]

SPORTS = ["Football", "Basketball", "Tennis", "Golf", "Soccer", "Baseball", "Hockey", "Cricket", "Rugby", "Swimming"]
SPORTS_TEAMS = ["Lakers", "Warriors", "Yankees", "Red Sox", "Chiefs", "Eagles", "Real Madrid", "Barcelona", "Manchester United", "Liverpool"]
SPORTS_ACTIONS = ["wins against", "defeats", "dominates", "struggles against", "ties with", "prepares for match with", "signs star player from"]

ENTERTAINMENT_CELEBS = ["Taylor Swift", "Tom Cruise", "Beyoncé", "Leonardo DiCaprio", "Jennifer Lawrence", "Brad Pitt", "Rihanna", "Ryan Reynolds", "Meryl Streep"]
ENTERTAINMENT_ACTIONS = ["stars in new film", "releases new album", "announces world tour", "wins award for", "spotted with", "launches new business", "signs deal with"]

BUSINESS_COMPANIES = ["Amazon", "Apple", "Microsoft", "Google", "Tesla", "Walmart", "JPMorgan", "Goldman Sachs", "Berkshire Hathaway"]
BUSINESS_ACTIONS = ["reports record profits", "announces layoffs", "acquires startup", "expands into new market", "faces regulatory scrutiny", "names new CEO", "launches IPO"]

HEALTH_TOPICS = ["nutrition", "exercise", "mental health", "sleep", "vaccines", "medical research", "healthcare technology", "wellness"]
HEALTH_ACTIONS = ["study reveals benefits of", "doctors recommend new approach to", "breakthrough in", "experts warn about", "new guidelines for", "research shows promise for"]

# Generate random dates for news articles (within the last week)
def random_date():
    days_ago = random.randint(0, 6)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    date = datetime.now() - timedelta(days=days_ago, hours=random_hour, minutes=random_minute)
    return date.strftime("%B %d, %Y at %I:%M %p")

# Generate random author names
def random_author():
    first_names = ["John", "Sarah", "Michael", "Emma", "David", "Olivia", "James", "Sophia", "Robert", "Emily"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Generate detailed news content
def generate_detailed_content(headline, section, basic_content):
    """Generate more detailed content for news articles"""
    
    # Create a more detailed version of the basic content
    paragraphs = []
    
    # First paragraph - expanded version of the basic content
    paragraphs.append(basic_content)
    
    # Second paragraph - add more context based on the section
    if section == "Technology":
        paragraphs.append(f"Industry analysts have been closely monitoring these developments, with many suggesting this could represent a significant shift in the tech landscape. \"This is exactly the kind of innovation we've been expecting,\" said Dr. Alex Chen, technology researcher at Digital Futures Institute. \"The implications for consumers and the broader market could be substantial.\"")
    
    elif section == "Sports":
        paragraphs.append(f"Sports commentators were quick to analyze the match, with many highlighting the exceptional performance from key players. \"We witnessed something special today,\" remarked veteran sports analyst James Wilson. \"The level of play and strategic execution was remarkable, and fans will be talking about this for weeks to come.\"")
    
    elif section == "Entertainment":
        paragraphs.append(f"The entertainment industry has been buzzing with speculation about this development. \"This represents a significant career move,\" entertainment correspondent Lisa Rodriguez told us. \"It's the kind of strategic decision that could define their trajectory in the industry for years to come.\"")
    
    elif section == "Business":
        paragraphs.append(f"Market watchers have been analyzing the potential impact on shareholders and the broader industry. \"This move signals a clear strategic direction,\" noted financial analyst Sarah Thompson of Global Investments. \"We're seeing significant trading volume as investors digest this news and recalibrate their expectations.\"")
    
    elif section == "Health":
        paragraphs.append(f"Medical professionals are cautiously optimistic about these findings. \"While more research is certainly needed, these initial results are promising,\" explained Dr. Michael Roberts, who specializes in this field. \"The potential implications for patient care and public health guidelines could be substantial.\"")
    
    # Third paragraph - future implications
    paragraphs.append(f"Looking ahead, experts predict this development could have far-reaching implications. Various stakeholders are already preparing for potential changes, while consumers and industry observers are watching closely for follow-up announcements. As this story develops, we'll continue to provide updates with the latest information and expert analysis.")
    
    # Join paragraphs with line breaks
    return "\n\n".join(paragraphs)

# Generate random news content based on section
def generate_news_for_section(section, count=5):
    # Always generate exactly 5 news items per section
    news_items = []
    
    for _ in range(count):
        if section == "Technology":
            company = random.choice(TECH_COMPANIES)
            action = random.choice(TECH_ACTIONS)
            product = random.choice(TECH_PRODUCTS)
            headline = f"{company} {action} new {product}"
            basic_content = f"{company} has {action.lower()} a revolutionary new {product} that promises to change the industry. The new offering features cutting-edge technology and innovative design that competitors will struggle to match."
        
        elif section == "Sports":
            sport = random.choice(SPORTS)
            team1 = random.choice(SPORTS_TEAMS)
            team2 = random.choice(SPORTS_TEAMS)
            while team1 == team2:  # Ensure different teams
                team2 = random.choice(SPORTS_TEAMS)
            action = random.choice(SPORTS_ACTIONS)
            headline = f"{team1} {action} {team2} in thrilling {sport} match"
            basic_content = f"In an exciting {sport} showdown, {team1} {action.lower()} {team2} in what analysts are calling one of the most memorable games of the season. Fans were on the edge of their seats as the competition reached its climax."
        
        elif section == "Entertainment":
            celeb = random.choice(ENTERTAINMENT_CELEBS)
            action = random.choice(ENTERTAINMENT_ACTIONS)
            headline = f"{celeb} {action}"
            basic_content = f"Entertainment icon {celeb} has made headlines again as they {action.lower()}. Fans and critics alike are buzzing about this latest development in the star's career."
        
        elif section == "Business":
            company = random.choice(BUSINESS_COMPANIES)
            action = random.choice(BUSINESS_ACTIONS)
            headline = f"{company} {action}"
            basic_content = f"In a significant business development, {company} {action.lower()}. Market analysts are closely watching how this will impact the company's stock price and industry position."
        
        elif section == "Health":
            topic = random.choice(HEALTH_TOPICS)
            action = random.choice(HEALTH_ACTIONS)
            headline = f"New {action} {topic}"
            basic_content = f"Health professionals are excited about a new {action.lower()} {topic}. This development could have significant implications for public health and wellness practices."
        
        else:
            headline = "Breaking News"
            basic_content = "More details to follow."
        
        # Generate detailed content
        detailed_content = generate_detailed_content(headline, section, basic_content)
        
        news_items.append({
            "headline": headline,
            "content": detailed_content,
            "author": random_author(),
            "date": random_date()
        })
    
    # Sort by date (newest first)
    news_items.sort(key=lambda x: datetime.strptime(x["date"], "%B %d, %Y at %I:%M %p"), reverse=True)
    
    return news_items