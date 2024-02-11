class PlaySong(Intent):
    """
    Lets people play songs on either YouTube, Spotify or SoundCloud.
    """
    lead = ("play",)
    exclude = ("on",) # These words will be excluded in all entities.
    
    song = TextEntityField(span=5)
    artist = TextEntityField(prefixes=("by", "with"), span=10)
    shuffle_songs = BoolEntityField(message_contains=("shuffle",))
    platform = TextEntityField(as_list=True, valid_strings=(
        "Spotify", "SoundCloud", "YouTube")
    )

    def respond(self, message: Message) -> Reply | ReplyStream:
        song = message.entities["song"]
        artist = message.entities["artist"]
        shuffle_songs = message.entities["shuffle_songs"]
        platform = message.entities["platform"]
        # Play the song...        
        return Reply(f"Playing {song} by {artist} on {platform}!")