import requests
from bs4 import BeautifulSoup
import sys
import time

# Banner
banner = """

________  ____  ___  _________                         
\_____  \ \   \/  / /   _____/     ____ _____    ____  
 /   |   \ \     /  \_____  \    _/ ___\\__  \  /    \ 
/    |    \/     \  /        \   \  \___ / __ \|   |  \
\_______  /___/\  \/_______  / /\ \___  >____  /___|  /
        \/      \_/        \/  \/     \/     \/     \/ 

"""

# List of websites to search
websites = {
    "Facebook": "https://www.facebook.com/",
    "Instagram": "https://www.instagram.com/",
    "Snapchat": "https://www.snapchat.com/add/",
    "LinkedIn": "https://www.linkedin.com/in/",
    "Twitter": "https://twitter.com/",
    "GitHub": "https://github.com/",
    "Pinterest": "https://www.pinterest.com/",
    "Reddit": "https://www.reddit.com/user/",
    "Tumblr": "https://www.tumblr.com/blog/",
    "YouTube": "https://www.youtube.com/user/",
    "Twitch": "https://www.twitch.tv/",
    "WhatsApp": "https://api.whatsapp.com/send?phone=",
    "Quora": "https://www.quora.com/profile/",
    "Vimeo": "https://vimeo.com/",
    "Medium": "https://medium.com/@",
    "WordPress": "https://wordpress.com/me/",
    "Flickr": "https://www.flickr.com/people/",
    "SoundCloud": "https://soundcloud.com/",
    "Dribbble": "https://dribbble.com/",
    "Behance": "https://www.behance.net/",
    "DeviantArt": "https://www.deviantart.com/",
    "AngelList": "https://angel.co/",
    "AboutMe": "https://about.me/",
    "Bitbucket": "https://bitbucket.org/",
    "CodePen": "https://codepen.io/",
    "Goodreads": "https://www.goodreads.com/",
    "HackerRank": "https://www.hackerrank.com/",
    "Imgur": "https://imgur.com/user/",
    "Kickstarter": "https://www.kickstarter.com/profile/",
    "Meetup": "https://www.meetup.com/members/",
    "ProductHunt": "https://www.producthunt.com/@",
    "StackOverflow": "https://stackoverflow.com/users/",
    "Steemit": "https://steemit.com/@",
    "WeHeartIt": "https://weheartit.com/",
    "Myspace": "https://myspace.com/",
    "VK": "https://vk.com/",
    "TikTok": "https://www.tiktok.com/@",
    "Blogger": "https://www.blogger.com/profile/",
    "LiveJournal": "https://www.livejournal.com/profile?userid=",
    "OK.ru": "https://ok.ru/profile/",
    "Disqus": "https://disqus.com/by/",
    "HubPages": "https://hubpages.com/@",
    "Ello": "https://ello.co/",
    "AngelFire": "http://www.angelfire.com/",
    "Last.fm": "https://www.last.fm/user/",
    "Mix": "https://mix.com/",
    "Smule": "https://www.smule.com/",
    "Vero": "https://www.vero.co/",
    "Periscope": "https://www.pscp.tv/",
    "Taringa": "https://www.taringa.net/u/",
    "500px": "https://500px.com/",
    "Houzz": "https://www.houzz.com/user/",
    "Fotolog": "http://www.fotolog.com/",
    "Canva": "https://www.canva.com/@",
    "Slideshare": "https://www.slideshare.net/",
    "Dailymotion": "https://www.dailymotion.com/",
    "Patreon": "https://www.patreon.com/",
    "ReverbNation": "https://www.reverbnation.com/",
    "Mixcloud": "https://www.mixcloud.com/",
    "Wattpad": "https://www.wattpad.com/user/",
    "Archive.org": "https://archive.org/details/@",
    "Bandcamp": "https://bandcamp.com/",
    "Ning": "https://www.ning.com/",
    "Gab": "https://gab.com/",
    "Badoo": "https://badoo.com/profile/",
    "Foursquare": "https://foursquare.com/",
    "Plurk": "https://www.plurk.com/",
    "Ravelry": "https://www.ravelry.com/people/",
    "Zomato": "https://www.zomato.com/",
    "GaiaOnline": "https://www.gaiaonline.com/profiles/",
    "BuzzFeed": "https://www.buzzfeed.com/",
}

# Function to search username on a specific website
def search_username(username, website):
    url = websites[website] + username
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status codes
        if response.status_code == 200:
            # Depending on the website, you may need to parse the HTML
            if website in ["Facebook", "Instagram", "LinkedIn", "Twitter"]:
                soup = BeautifulSoup(response.content, "html.parser")
                if soup.find("title").get_text().lower() == "page not found":
                    return False, None
                else:
                    return True, url
            elif website == "Snapchat":
                # Check if response contains the username
                if username.lower() in response.text.lower():
                    return True, url
                else:
                    return False, None
            elif website == "GitHub":
                # Check if response contains the username
                if username.lower() in response.text.lower():
                    return True, url
                else:
                    return False, None
            # Add more parsing logic for other websites if needed
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return False, None

# Function to save results to a text file
def save_results(results):
    with open("resultfind.txt", "w") as file:
        for website, (found, url) in results.items():
            if found:
                file.write(f"{website}: Found - {url}\n")
            else:
                file.write(f"{website}: Not found\n")

# Function to search username across all websites
def search_all_websites(username):
    results = {}
    total_websites = len(websites)
    for index, website in enumerate(websites):
        sys.stdout.write("\r" + f"Searching on {website}... [{(index+1)/total_websites*100:.2f}%]")
        sys.stdout.flush()
        results[website] = search_username(username, website)
        time.sleep(0.1)  # Simulate some processing time
    print()  # New line after loading completes
    return results

# Main function
def main():
    # Display banner
    print(banner)
    
    # Get target username from the user
    target_username = input("Enter the username to search: ")
    
    # Search username across all websites
    results = search_all_websites(target_username)
    
    # Save results to text file
    save_results(results)
    
    print("Search completed. Results saved to resultfind.txt")

if __name__ == "__main__":
    main()


