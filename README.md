MeidoBot
========
MeidoBot is a pluggable natural language assistant written in Python.

Meido is weeaboo for Maid, aka servants in french uniforms.

This is still an alpha, so things will be buggy and change a lot. Still, feel free to try it out or write a plugin. Send a pull request with your plugin and it'll probably be added; I'll try to maintain all plugins I have whenever I change the plugin API.


Upcoming features
-----------------
* Proper UI! *(Okay, there is a TkInter UI, but it's horrible because TkInter)*
* More Plugins!
    * Twitter
    * Heello
    * Email
    * Alarm/Reminders (once we have an UI)

A sample plugin
---------------
Making plugins are easy! It does require a fair bit of boilerplate though, so here's a sample plugin you can copypaste.

Create your plugin in plugins/ and it'll be picked up automatically.

Set `brain.debug_plugins` to true in config.json to get stack traces if something goes wrong when loading the plugin, such as syntax errors.

```python
from meidobot.plugin import Plugin

# This variable is required
plugin_class = "BombPlugin"

class BombPlugin(Plugin):
	# Define a bunch of words that will trigger our plugin.
	# It's possible to act on /everything/ too, but it's harder.
	actions = ["throw", "deploy", "selfdestruct"]
	objects = ["bomb", "explosive"]
	targets = []
	
	# Define handlers. This is a simple way to handle actions on
	# keywords. If none of the handlers match, 'do_fallback' will be
	# called (weight -10), which will by default just pass on to the
	# next handler.
	handlers = {
		# Throw and Deploy are synonyms, and both map to 'do_throw'.
		# do_throw has a "weight" of 1.
		# Handlers with higher weight take priority, even between
		# different plugins.
		# Note that triggers must be lowercase.
		('throw', 'deploy'): ('do_throw', 1),
		
		# Note the trailing , - we need those for one-item tuples
		('blow up',): ('do_blow_up', 1),
	}
	
	
	
	def do_throw(self, c):
		# Only react to things that are obviously referring to our plugin!
		# Another plugin might also use the word "throw"
		if 'bomb' in c.objects or 'explosive' in c.objects:
		
			# Pick the first recognized object here, so that
			# 'throw bomb' and 'throw explosive' will both use
			# the same word that the user used.
			self.brain.ui.say("Throwing %ss! Watch out!" % (c.objects[0]))
			
			# Return True if we've handled the event...
			return True
		
		# ...or False otherwise - this'll make the next handler fire
		return False
	
	def do_blow_up(self, c):
		from time import sleep

		self.brain.ui.say("Initiating self-destruct sequence...")
		sleep(1)
		self.brain.ui.say("3...")
		sleep(1)
		self.brain.ui.say("2...")
		sleep(1)
		self.brain.ui.say("1...")
		sleep(1)
		self.brain.ui.say("BOOM!")
		
		# Terminate gracefully. Rather than just exiting, we let the
		# main loop finish and make sure to save data and such.
		self.brain.stop()
		
		# This won't actually happen, but it's good practice regardless
		return True
```
