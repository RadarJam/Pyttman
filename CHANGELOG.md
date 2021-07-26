# Pyttman Changelog

### v 1.1.4



# Native client support for community plattforms		

> **This feature is one of the flagship-features of this release.**  


A new interface class, `BaseClient` dictates how Pyttman expects a minimally developed client to behave. 

This allows us to subclass platform clients from SDK's and libraries from plattforms, and using the `BaseClient` as a mixin, creating the powerful combination of a native client to be used with Pyttman.

The native and community Client support in Pyttman enables you to launch your app to the [Discord](https://discordpy.readthedocs.io/en/stable/api.html) plattform **without a single line of code.** 

By simply providing which clients you want to use in the `settings.py` file ( using Pyttman-included Clients, or a client you wrote yourself )  - your app will be running on all clients in parallel by starting your app with `pyttman-cli runclients`.  

The Pyttman `MessageRouter` will keep your clients separate, so there's no risk of a `Reply` ending up in the wrong plattform. 

Many more clients are on the way, so stay tuned for more plattform clients to be supported natively.



> **Note**
>
> Some platforms offer different methods than others; if you mix plattform clients in your app, it's a good idea to check which client is associated with your message, if you're accessing members of that client. 



*Example*

```py
# The following CLIENTS list will start your app using the Discord client 
# making your bot go online, with your Pyttman app powering it's backend.
# To use more clients, simply append more config dict's like this one, and 
# have your app hosted on these platforms in parallel.

CLIENTS = [
	{
		"module": "pyttman.clients.community.discord.DiscordClient",
		"token": "foo-token-from-discord-developer-portal",
		"guild": "bar-guild-id-from-your-discord-server"		
	}
]
```



* **Parallel runtime for all clients**

  Develop your app **once** - and have it online on multiple platforms in an instant. Add the clients you want to use to the `CLIENTS` list in `settings.py`. That's it! 

  The next time you run `pyttman-cli runclients` , the clients start up in parallell and inside your app, you will see which client is sending the message by the Message property `client`. 

  

  *Example*

  ```py
  # inside a Command.respond method:
  
  if isinstance(message.client, DiscordClient):
  	print(message.client.users)
  elif isinstance(message.client.CliClient):
  	message.client.publish("I can publish this directly to my CliClient for testing!")
  ```

  

> **Hint!**
>
> If you're a power user and want to use the hooks defined in `discord.Client`, simply subclass `DiscordClient ` to have the Pyttman-defined  '`on_message`'  hook method already taken care of (this is where the integration takes place between your Pyttman app and Discord) and define any behavior in the other hooks as you please. Use your custom class instead of the included one, in the example above. 





# EntityParser API

> **This feature is one of the flagship-features of this release.**  

The EntityParser is a powerful tool for developers looking to extract information from natural language. 

Odds are you're developing a chatbot using Pyttman. Chatbots usually have a job to do, and more than often, we as devs, are looking for data in the message from a user. 

A message from a user may look something like this:



>  `Can you play Rocket Man by Elton John on Spotify please?`



In this example, you may have a Command which job it is to play songs for users on their Spotify accounts. 

Now, your app may host support for more platforms than just one. Say you also support SoundCloud, or YouTube Music. You'd want to identify which platform the user wanted to use. 

You're also looking for `artist` and/or `song` in this message. 

The **EntityParser** class defined *inside* your Command will take care of this for you. It enables you to quickly and without a single iteration or if-statement, find the values you're looking for by defining a set of rules to wich degree is entirely up to you - loosely or constricted.



*Example*

```py
class PlayMusic(Command):
    lead = ("play",)

    """
    Define the EntityParser inside the Command class and 
    create fields, named as you want them to be named when
    accessing them through self.entities.get(). 
    """

    class EntityParser(Command.EntityParser):
        song = ValueParser(identifier=CapitalizedIdentifier, prefixes=("play",), span=10)
        artist = ValueParser(identifier=CapitalizedIdentifier, prefixes=("by",), span=2)
        platform = ChoiceParser(choices=("Spotify", "SoundCloud", "YouTubeMusic"))

    def respond(self, message: MessageMixin) -> Reply:
        print("My entities:", self.entities)
        return Reply(self.entities)


class MusicFeature(Feature):
    commands = (PlayMusic,)


```

Writing the message to the following example command returns:

```py
{'artist': 'Elton John', 'platform': 'spotify', 'song': 'Rocket Man'}
```



This is a short example of how powerful the EntityApi is, and what you can do with it. 

In short - it enables you to develop Commands and Features which extract information from messages, without looping manually, looking for data. 





# Storage API

* Feature-level implicit encapsulation, dict-like storage in all `Command` classes. 

  The Storage API offers a `Storage` object accessible in all `Command` subclasses by accessing  the `self.feature.storage` property.  Your other Commands which are defined in the same `Feature` will access the same storage object which allows for an easy and safe way to store and share data between commands. 

  

  *Example*

  ```py
  # Put data
  class FooCommand(Command):		
  	def respond(self, Message):
  		# self.feature.storage["foo"] = "bar" works as well
  		self.feature.storage.put("foo", "bar") 
  
  # Get data 
  class BarCommand(Command):
  	def respond(self, Message):
  	foo = self.feature.storage.get("foo")
  	print(foo)
  	
  class FooBarFeature(Feature):
  	commands = (FooCommand, BarCommand)
  
  ```

  **Outputs:**

  `>>> "bar"`

  

  The Storage object is encapsulated by the scope of a `Feature` in which the command is listed in. This means that `Command` classes operate on the same `Storage` object as the other `Command` classes in the same `Feature`, but commands outside of the Feature cannot interfere with the data in that storage object. 

  

  > **Note**
  >
  > If you don't use the Storage API but try to use instance variables in your commands, you will eventually learn that they don't stick. This is because of how Pyttman preserves memory in deleting Command instances once the Reply is generated. 

  

  

# Improved settings module

* Improved versatility with configuration for default replies vastly improved and other similar settings

* AutoHelp, creating automatically generated help snippets for your Commands by their configuration
* Improved error handling
* If exceptions occur in the application, the user will in 99% of the times receive a mesage letting them know something went wrong instead of the app going silent. The app is much less likely to crash, and a UUID is stored in the log file along with a stderr print out of the error. The user also gets to see thsi UUID for relaying to a developer if needed.



# Routing

MessageRouters improved, now instantiating Command classes each time to prevent memory leaks in local preferences in Command objects outside of the Storage API.



# Licenses

This release includes discord.py, and it's license is mentioned in the README.MD and LICENSE of the Pyttman project, [here](https://github.com/dotchetter/pyttman)