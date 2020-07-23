# reddit\_auto\_upvote


#### ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
#### ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
#### ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
#### ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
#### ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
####  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝

randomly upvotes poust in new and monitors their traction

## Usage:

```usage
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



## prawn Documentation
 [writing reddit bot] (https://praw.readthedocs.io/en/v3.6.0/pages/writing_a_bot.html)




## Reddit.py
	

### primary functions:
	read (file = default file)  # reads payloade form file and sets default file

	write (file = default file) # writes payloade to file

	collect ()					# starts procesess of collecting data

	list()						# summary of collected data

	print()						# prints top of curent Payload


### set funtions:
	
	set_debug_flag()
	set_choise(choses = ["[up]","[dw]","[no]"] )
	set_bot(bot = "bot1")
	set_sub(subreddit = "all")

### \*.bin files
+ pickled list of tracked posts 

		[ 	choise 	# "[up]" upvoted / "[dw]" downvoted / "[no]" no action
			postId 	# id of a post
			time  ]	# time when choise was made
