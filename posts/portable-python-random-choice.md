title: Portable python random.choice() function
post_date: 2014-02-02 14:20:52
post_name: portable-python-random-choice

# Portable python random.choice() function

While writing some unit tests that utilize the Python pseudo-random number generator 
I discovered an inconsistency between Python 2.7 and 3.3. Even after setting the seed 
I would get different results using `random.choice()` under each interpreter version. 
It took a bit of Googling (the winning search query was "random.choice python2 python3") 
I found [what I was looking for in Google Groups](https://groups.google.com/forum/#!topic/comp.lang.python/KwALjKjF6Y4).

It appears that `random.choice()` in 2.7 and 3.3 looks like:

<script src="https://gist.github.com/mdshw5/8774259.js"></script>

My portable solution was to create a new function `choice()`:

<script src="https://gist.github.com/mdshw5/8774298.js"></script>

Which gives the same result as 
the Python2.X function but different than the 3.X function:

<script src="https://gist.github.com/mdshw5/8773843.js"></script>

This seems like something that [six](http://packages.python.org/six/) should handle.