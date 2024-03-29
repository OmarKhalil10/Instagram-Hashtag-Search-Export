import instaloader
from datetime import datetime
import csv

def download_posts_to_csv(username, since_date, until_date, csv_filename):
    L = instaloader.Instaloader()

    # Get posts for the specified user
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        posts = profile.get_posts()
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile @{username} not found or not accessible.")
        return

    # Set the date range
    SINCE = since_date
    UNTIL = until_date

    # Open CSV file for writing
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Caption', 'URL', 'Date', 'Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Download posts within the specified date range
        for post in posts:
            post_date = post.date

            if post_date > UNTIL:
                continue
            elif post_date < SINCE:
                break
            else:
                # Download post and write details to CSV
                L.download_post(post, target=username)
                writer.writerow({
                    'Caption': post.caption,
                    'URL': f'https://www.instagram.com/p/{post.shortcode}/',
                    'Date': post_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'Likes': post.likes,
                    'Comments': post.comments
                })

# Example usage
# Replace with your own Instagram username
username_to_download = 'IG_USERNAME'
start_date = datetime(2021, 1, 1)  # Replace with your desired start date
end_date = datetime(2023, 1, 31)   # Replace with your desired end date
output_csv_filename = 'downloaded_posts.csv'

download_posts_to_csv(username_to_download, start_date, end_date, output_csv_filename)
