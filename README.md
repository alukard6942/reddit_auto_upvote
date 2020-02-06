# reddit_auto_upvote
randomly upvotes poust in new and monitors their traction

## prawn Documentation
[https://praw.readthedocs.io/en/v3.6.0/pages/writing_a_bot.html ] writing reddit bot


## PayLode.bin
+ binary file containg PayLode of all upvoted from new
+ TODO for subreddit new *.bin 
+

## main 
+ main


## Reddit
	PayLoad 		List of up dw posts
	read():			reads form PayLoad.bin
	write():		writes to PayLoad.bin
	print():		prints contents of PayLode


## PayLoader (Reddit)
	__init__():		reads paylode on init
	vote():			colects votes forever
	update():		updates PayLoad

## PayChecker (Reddit)
	__init__():		void
	list():			collects results form PayLoad
	