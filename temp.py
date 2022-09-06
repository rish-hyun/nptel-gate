from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=SuQTqjqCATM')
stream = yt.streams.get_highest_resolution()
print(stream.title)