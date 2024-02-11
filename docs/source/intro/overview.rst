===============
Overview
===============

How many times have you had to iterate over the message contents to route the message to the correct part of your code?
Or even worse; How many hours have you spent on trying to decipher a message and its contents to find words of interest?
Maybe the name of a song, or a phone number? Or a username?

I had enough of that - so I wrote this framework.
The Pyttman Framework aims to provide a similar experience as Django and Flask does for web, but for chatbots and digital assistants.
It's large and full of features yet easy to use.

-----------------------
Ability, Intent, Entity
-----------------------
*Ability* - 
Chatbots can have many areas of capabilities; Anything from answering questions, searching the web, playing songs to playing games. I call these Abilities, which encapsulate responses to queries in the same domain. The Ability class has Intent classes, and acts like a hub for the Intent classes which correspond to the same domain of the application. The ability to store expenses may contain many components - saving new expenses, visualizing existing ones, searching for records, etcetera.

Ability classes also facilitate a session storage object accessible in the Ability as self.storage and in intent classes as self.ability.storage. This allows efficient and safe memory storage for intents to manipulate data in their respective domain, without global variables and risking exposing data to intents of another domain.


.. literalinclude:: activity.py
   :language: python
   :linenos:

*Intent* -
The Intent class is the heart of the Pyttman development experience. They are classes, 1:1 to a message and a response. If you're a web developer, you see the similarity to a controller. Here, we tell which messages it should match and also how to respond with implementing the respond method.

Consider a message like Play Last Train Home by John Mayer on Spotify.

.. literalinclude:: intent.py
   :language: python
   :linenos:


*Entity* - What are those EntityField classes in the example above?
In Pyttman, the Entity is a word, or several words sought in a message.
When writing chatbots it's very common to have to parse the message from humans to try and find words of interest.
Maybe your chatbot registers purchases in a database. You'll need to parse the name of the purchased item as well as the price.
But how do you know where to stop the name of the item? It could be one word, or several.
The price could be mentioned first - or last - or in the middle of the message.
Positioning won't help. Regex? This repetitive and complex process also won't scale.
When you've invented the parser for one answer, you'll need to do it again for the next thing your chatbot can do.

Let's take a closer look at the example code above.

.. code-block:: python
    
   song = TextEntityField(span=5)

This EntityField declared in the Intent class above tells Pyttman that you're looking for a text value in the message.
The span argument defaults to 1, but in this case is set to 5.
That means the value parsed here can be 5 words long, at the longest - after which Pyttman will stop adding words to the entity, should it be any longer than that.

.. code-block:: python

   shuffle_songs = BoolEntityField(message_contains=("shuffle",))


For situations where a set of known valid choices are available, the valid_strings argument can be provided, rendering all other words ignored. 
In the example below, message.entities["platform"] can only ever be Spotify, SoundCloud, YouTube or its default which defaults to None.

.. code-block:: python

    platform = TextEntityField(as_list=True, valid_strings=(
        "Spotify", "SoundCloud", "YouTube"))


When the message has entered the respond method of the matching Intent, the entities are available on the entities property on the Message object.
Given the Intent above and the message Play Last Train Home by John Mayer on Spotify, the dictionary message.entities look like this:

.. code-block:: python

    {
        'song': 'Last Train Home', 
        'artist': 'John Mayer', 
        'shuffle_songs': False, 
        'platform': 'Spotify'
    }

The next chapter is :doc:`Installing Pyttman </intro/install>`.