# reddit\_auto\_upvote
randomly upvotes poust in new and monitors their traction

## Usage:

```usage
upvote [flag] [option] 

	-d --debug             |	enable debug mode

	l list    [file]       |	lists averige upvode/downvote/none count
	p print   [file] [n]   |	prints last n collected posts 
	c collect [sub] [file] |	starts collecting posts to file
	    controls:  q       |	save and exit
	               w       |	save
	               e       |	exit without saving (saves each minute)
	               s       |	skip one post
	               l       |	clear display
	               d       |	enable debug mode
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