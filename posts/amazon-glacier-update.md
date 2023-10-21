title: Amazon Glacier update
link: /amazon-glacier-update/
creator: matt
description: 
post_id: 261
post_date: 2012-08-29 09:17:07
post_date_gmt: 2012-08-29 13:17:07
comment_status: open
post_name: amazon-glacier-update
status: publish
post_type: post

# Amazon Glacier update

It looks like after 24 hours, my data are all there:

[![](/uploads/2012/08/Screen-Shot-2012-10-22-at-11.07.22-AM.png)](/uploads/2012/08/Screen-Shot-2012-10-22-at-11.07.22-AM.png)

And my bill will be $0.15 this month.

Overall, this was a smooth process. Now, I think we'll start freezing monthly versions of my Time Machine backups in Glacier. There is one small catch that I managed to miss in my original post. Glacier charges a [minimum of three months of data storage](http://aws.amazon.com/glacier/faqs/#How_am_I_charged_for_deleting_data_that_is_less_than_3_months_old), and prorates that amount if you delete your archives earlier. That really just means I'll be keeping three of the most recent versions of my monthly backups, and deleting anything older than three months.
