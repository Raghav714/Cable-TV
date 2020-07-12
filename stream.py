import urllib.request
import subprocess
import argparse

class PlaylistParser():
    def __init__(self):
        self.filename = None
        self.channels = []

    def is_m3u(self, filename=None):
        fname = filename or self.filename
        try:
            with open(fname, "r") as fhand:
                while True:
                    line = fhand.readline()
                    line = line.strip()
                    if line:
                        if line.startswith("#EXTM3U"):
                            return True
                    else:
                        return False
        except FileNotFoundError:
            return False
    
    # Parse the m3u file
    def parse_m3u(self, filename=None):
        if filename:
            self.filename = filename
        is_m3u = self.is_m3u(filename)
        if is_m3u:
            print("Is m3u file")
            with open(self.filename, "r") as fhand:
                playlist=[]
                channel = {}
                for line in fhand:
                    line=line.strip()
                    if line.startswith('#EXTINF:'):
                        # pull length and title from #EXTINF line
                        meta_data = line.split(",")
                        channel_name = meta_data[-1]
                        channel["name"] = channel_name
                    elif (len(line) != 0):
                        # pull channel link from all other, non-blank lines
                        link=line
                        channel["link"] = link
                        self.channels.append(channel)
                        # make the channel dict empty for the new channel
                        channel = {}
        else:
            print("Not an m4u file")
    
    # Display list to the user
    def list_channels(self):
        print("List of channels available are: ")
        for i, channel in enumerate(self.channels, 1):
            if i % 3 == 0:
                print("{0}: {1}".format(i, channel.get("name")).ljust(26))
            else:
                print("{0}: {1}".format(i, channel.get("name")).ljust(26), end=" ")
        print()
    
    # Returns the list of channels with {name, link}
    def get_channels(self):
        return self.channels

file_name = "India.m3u"
playlist = PlaylistParser()
playlist.parse_m3u(file_name)
playlist.list_channels()
channels = playlist.get_channels()

choice = "n"
error = False
while choice not in ["y", "yes", "q", "quit"]:
    try:
        channel_no = int(input("Enter the channel number: "))
        if channel_no < 1:
            raise ValueError
        channel = channels[channel_no - 1]
        subprocess.run(["vlc", channel["link"]])
    except ValueError:
        print("INVALID CHANNEL NUMBER")
        error = True
        quit()
    except Exception as e:
        print(e)
    finally:
        if not error:
            choice = input("Press q or quit to EXIT or Enter to continue: ").lower()
print("Exiting...\n")
