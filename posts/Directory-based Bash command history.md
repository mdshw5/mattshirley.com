title: Directory-based Bash command history
post_date: 2013-07-22 11:20:52
post_name: Directory-based-Bash-command-history

# Directory-based Bash command history

Most of my work is done in Linux using the Bash shell. One of the most efficient 
constructs in Bash is the global history file `~/.bash_history`. It can be accessed 
and immediately searched in reverse order using the `Ctrl-r` keybinding, which I make 
good use of every day. The global history rolls over at `$HISTSIZE` lines (usually 
1000), so sometimes I lose older commands. Additionally, unless I used absolute file paths 
I lose the directory context for all commands. [This script](http://ecloud.org/index.php?title=Eternal_plus_per-directory_bash_history) 
writes a per-directory command history while still preserving (mostly) the global history. 
I've modified it to check for write permission before trying to create the local history file:

<script src="https://gist.github.com/mdshw5/8710121.js"></script>

Put it in your .bashrc file and you're done!