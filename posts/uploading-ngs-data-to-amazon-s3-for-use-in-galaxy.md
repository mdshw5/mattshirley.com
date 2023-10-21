title: Tutorial: uploading NGS data to Amazon S3 for use in Galaxy
link: /uploading-ngs-data-to-amazon-s3-for-use-in-galaxy/
creator: matt
description: 
post_id: 492
post_date: 2013-02-14 14:18:54
post_date_gmt: 2013-02-14 18:18:54
comment_status: open
post_name: uploading-ngs-data-to-amazon-s3-for-use-in-galaxy
status: publish
post_type: post

# Tutorial: uploading NGS data to Amazon S3 for use in Galaxy

So, you've managed to launch Galaxy on Amazon Web Services EC2, and now you're trying to upload all of your RNA-seq files to run TopHat and Cufflinks. Great! But it's taking 5 (five!) days to transfer your data. That's going to cost a ton of money if you keep your Galaxy instance running on EC2 the entire time. Luckily for you there is a better way.

# Amazon S3

Amazon S3 is the service behind cloud storage giant [Dropbox](http://dropbox.com) and a number of other companies. Once your data are hosted on S3, you can quickly and cheaply import it into your Galaxy instance running on Amazon EC2. For $0.01 per gigabyte per month you can host your data on S3. Compare this to approximately $0.30 - $2.00 per _hour_ for running your Galaxy instance on the cloud, and you will quickly realize that uploading your large data to S3 before running Galaxy will save you big time.

## Uploading your data to S3

Go to the [S3 link](https://console.aws.amazon.com/s3/home?region=us-east-1#) in your [AWS dashboard](https://console.aws.amazon.com/console/home?#).

[![Screen Shot 2013-02-14 at 12.46.55 PM](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.46.55-PM.png)](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.46.55-PM.png)

You will see a management page for your S3 "buckets". Create a new bucket. You can think of a bucket like a hard drive - you can place files and folders inside a bucket.

[![Screen Shot 2013-02-14 at 12.48.05 PM](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.48.05-PM.png)](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.48.05-PM.png)

[![Screen Shot 2013-02-14 at 12.50.00 PM](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.50.00-PM.png)](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.50.00-PM.png)

Now select your new bucket. You'll drop in to a page telling you that your bucket is empty, and allowing you to select "upload" to add files to the bucket.

[![Screen Shot 2013-02-14 at 12.51.14 PM](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.51.14-PM.png)](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.51.14-PM.png)

Add some files using the file selector, and then click "start upload".

[![Screen Shot 2013-02-14 at 12.53.56 PM](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.53.56-PM.png)](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.53.56-PM.png)

You might want to use the "advanced uploader" if your files are rather large. The length of the uploading process will depend the speed of your internet connection. _Don't try this at your local Starbucks_. Once your files appear in S3, you can select a file and view its properties. You'll want to choose "actions" and "make public" so that we can import this file later into Galaxy. _Note_ this will allow anyone on the internet to see your file. I won't cover file permissions in this guide, but you may be able to keep your data private and still import them into Galaxy on AWS.

[![Screen Shot 2013-02-14 at 1.01.03 PM](/uploads/2013/02/Screen-Shot-2013-02-14-at-1.01.03-PM.png)](/uploads/2013/02/Screen-Shot-2013-02-14-at-1.01.03-PM.png)

Now that your uploads have finished, let's [initialize your Galaxy cluster on AWS](/uploads/2013/02/Galaxy-for-NGS-Analysis.pdf) and import your files into your history. You can simply select your file and copy its S3 URL (in blue) to your clipboard.

[![Screen Shot 2013-02-14 at 12.58.38 PM](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.58.38-PM.png)](/uploads/2013/02/Screen-Shot-2013-02-14-at-12.58.38-PM.png)

Then in Galaxy, select the "upload file" tool under "get data" and paste the S3 URL of your file into the text box and click "execute".

[![Screen Shot 2013-02-14 at 1.14.51 PM](/uploads/2013/02/Screen-Shot-2013-02-14-at-1.14.51-PM.png)](/uploads/2013/02/Screen-Shot-2013-02-14-at-1.14.51-PM.png)

That's it! The file should almost immediately appear in your Galaxy history and you can start working with your data.