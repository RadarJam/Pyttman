class MusicPlayer(Ability):
    """
    This Ability class holds Intent classes which serve users
    ways to play music through the chatbot.
    """
    
    # Intent classes are added to this tuple for them to be available 
    # to users when the application starts.
    intents = (PlaySong,
               RepeatSong,
               FindSongByLyrics)