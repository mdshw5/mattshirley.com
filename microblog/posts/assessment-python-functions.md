title: Assessment - Python functions
post_date: 2014-10-01
post_name: assessment-python-functions

# Software Carpentry concept assessment

The second assignment in the Software Carpentry instructor training involved
a concept known as "reverse instructional design". RID is analogous to test
driven software development, where you define a specification you can target  
with a test, and then make the code pass the test. In the case of RID, you might
design an assessment question that reveals the knowledge and (mis)information
a student might have, and then teach concepts that fill in the missing knowledge.
What follows below is [my assessment](http://teaching.software-carpentry.org/?p=9054):

As a followup to my [concept map](http://teaching.software-carpentry.org/?p=8567) 
exercise, here is a multiple choice assessment question about the call stack.
Please choose the correct statement.

The call stack:

1. is scoped globally
2. contains the initial values passed to the function
3. is shared between function calls
4. cannot contain other functions
5. is the set of initial values passed as arguments to the function

Please fill in the instances of `%%` to complete the function definition:

    %% mean_of_list_of_ints(%%):
      assert isinstance(%%, l)
      assert all([type(n) is %% for n in l])
      length = len(l)
      mean = sum(l) / length
      %% mean
