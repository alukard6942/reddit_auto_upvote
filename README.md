# reddit_auto_upvote
randomly upvotes poust in new and monitors their traction

## prawn Documentation
 [writing reddit bot] (https://praw.readthedocs.io/en/v3.6.0/pages/writing_a_bot.html)


## \*.bin 
+ pickled list of tracked posts 
+ [ choise 	# "[up]" upvoted / "[dw]" downvoted / "[no]" no action
	postId 	# id of a post
	time  ]	# time when choise was made	

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
	