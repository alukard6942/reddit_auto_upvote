# reddit\_auto\_upvote
[//]: # ( ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗ )
[//]: # ( ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝ )
[//]: # ( ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗   )
[//]: # ( ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝   )
[//]: # ( ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗ ) 
[//]: # (  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝ )

randomly upvotes poust in new and monitors their traction

## fylosofy

becose of need for interactivnes, giving the user a console is the best option
genral usage:
```sh
python3 -i upvote.py
```


## Usage:

```help
upvote [flag] [option] 
	--help              -h |	prints this help
	--debug             -d |	enable debug mode
	--image             -i |	enable image mode ie. shows prewie
	--nsfw [option]        |	[enable|disenable|only] nsfw content
	--no-choise            |	disable up\\downvoting
	--no-wait              |	disenable wait time
	--collect-user         |	enable subing to users ie. u_*

	list    [file]       l |	lists averige upvode/downvote/none count
	print   [file] [n]   p |	prints last n collected posts 
	collect [sub] [file] c |	starts collecting posts to file
	
	controls:      q       |	save and exit
	               w       |	save
	               e       |	exit without saving (saves each minute)
	               s       |	skip one post
	               l       |	clear display
	               d       |	enable debug mode
	               i       |	enable image modea
	               +-      |	configure image size
	               a       |	lists averiges 
	               f       |	shows curent configuratios
	                        	! very badly named ! only a pet project
```

### primary functions:

	collect      				# starts procesess of collecting data

	list						# summary of collected data

	print						# prints top of curent Payload


## prawn Documentation
 [writing reddit bot] (https://praw.readthedocs.io/en/v3.6.0/pages/writing_a_bot.html)
