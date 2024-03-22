from User import User
import os
import csv
import shutil

SCRAPER_DIRECTORY = "scrapedYoutubeData"

if os.path.exists(SCRAPER_DIRECTORY):
    # remove old files alongside directory
    shutil.rmtree(SCRAPER_DIRECTORY)

# make new directory for new files
os.mkdir(SCRAPER_DIRECTORY)

def export_playlists_lists(playlists_lists):
    #csv storage location
    csvName = "Playlists.csv"
    csvFilePath = SCRAPER_DIRECTORY + "/" + csvName

    # create a csv file and add the playlist data
    with open(csvFilePath, 'a') as csv_file:
        # create the writer object
        writer = csv.writer(csv_file)

        # write the first row header
        writer.writerow(["Playlist ID", "Playlist Title", "Media Count"])

        # For each list of the playlists_lists
        for playlist_list in playlists_lists:
            # get videos from each playlist
            for playlist in playlist_list:
                # playlist details
                playlist_id = playlist["id"]
                playlist_media_count = playlist["contentDetails"]["itemCount"]
                playlist_title = playlist["snippet"]["title"]

                # write the playlist details to a new row in the csv file
                writer.writerow([playlist_id, playlist_title, playlist_media_count])

def export_videos_list(playlists_lists, user):
    csvName = "VideoList" + '.csv'
    csvFilePath = SCRAPER_DIRECTORY + "/" + csvName

    # create a csv file and add the playlist data
    with open(csvFilePath, 'a') as csv_file:
        # create the writer object
        writer = csv.writer(csv_file)

        # write the first row header
        writer.writerow(["Playlist Title", "Video Title", "Default Thumbnail URL", "Playlist ID", "Video ID"])

        # For each list of the playlists_lists
        for playlist_list in playlists_lists:
            # get videos from each playlist
            for playlist in playlist_list:
                # playlist details
                playlist_id = playlist["id"]
                playlist_title = playlist["snippet"]["title"]

                user.request_playlist_videos(playlist_id, playlist_title)

        # get all the videos in videos list
        videos_lists = user.get_videos_lists()
                
        for videos_list in videos_lists:
            try:
                playlist_title = videos_list[0]["playlistTitle"]
            except (IndexError, KeyError) as e:
                # Handle the exception as you see fit, like printing an error message or setting a default value for playlist_title
                print(f"Error occurred: {e}")

                # error: playlist title is empty
                playlist_title = ""

            for video in videos_list:
                try:
                    video_id = video["id"]
                    video_title = video["snippet"]["title"]
                    playlist_id = video['snippet']['playlistId']
                    video_default_thumbnail = video["snippet"]["thumbnails"]["default"]["url"]

                except KeyError as key_error:
                    # Handling KeyError if 'playlistID' or 'playlistTitle' keys are missing in the video dictionary
                    # Perform actions for missing keys (e.g., provide default values, logging, handling the error)
                    print(f"KeyError: Missing key - {key_error}")

                    # key_error: "default" thumbnail is missing
                    if "default" in str(key_error):
                        video_default_thumbnail = ""

                except Exception as e:
                    # Handling any other potential exceptions that might occur
                    # Perform actions based on the specific exception (e.g., logging, handling the error)
                    print(f"An error occurred: {e}")


                # write the video details to a new row in the csv file
                writer.writerow([playlist_title, video_title, video_default_thumbnail,  playlist_id, video_id])

def main():
    user = User()
    user.authenticate("client_secret.json", "youtubeAPI")

    user.request_playlists_lists()
    playlists_lists = user.get_playlists_lists()

    export_playlists_lists(playlists_lists)
    export_videos_list(playlists_lists, user)
main()