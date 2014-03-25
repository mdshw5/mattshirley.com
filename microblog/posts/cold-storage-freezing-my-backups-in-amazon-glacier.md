title: Cold storage - freezing my backups in Amazon Glacier
link: /cold-storage-freezing-my-backups-in-amazon-glacier/
creator: matt
description: 
post_id: 221
post_date: 2012-08-27 15:08:01
post_date_gmt: 2012-08-27 19:08:01
comment_status: open
post_name: cold-storage-freezing-my-backups-in-amazon-glacier
status: publish
post_type: post

# Cold storage: freezing my backups in Amazon Glacier

A couple of days ago, Amazon sent me an email about a new AWS service called "[Glacier](http://aws.amazon.com/glacier/)". What a boring name, huh? It's not caller something sexy like "FlexStore", or "FireVault", and that's by design. The idea behind Glacier is long term, low power (and therefore lower cost) offsite storage. Facebook recently announced that they are [moving to a similar solution](http://www.wired.com/wiredenterprise/2012/08/sub-zero/) for backups. You see, spinning platter hard drives take a constant amount of energy to keep running. If you write data to a HDD, and then pull the plug, you cut out the cost of operating the drive until you need to retrieve your data once again. For long-term backups which may never be accessed this is an ideal solution. Unfortunately, Glacier just exists as an API for the moment. [Peter Binkley](http://www.wallandbinkley.com/quaedam/2012/08_25_playing-with-amazon-glacier.html) wrote an excellent account of sending some data to the Glacier, and then retrieving it. I think I'll do the same, using a Java application called [glacierFreezer](http://www.glacierfreezer.com).

The first step for me is to create a public/private key pair through AWS [IAM](http://aws.amazon.com/iam/). I just created a user named "glacier" with access to all AWS functions, except IAM. This should be fairly safe, assuming I don't kick off all kinds of unwanted services and rack up a huge bill. glacierFreezer also needs an AWS SimpleDB to interact with, and seems capable of creating a SimpleDB domain for us, but I'll create one anyway with [boto](https://github.com/boto/boto).
    
    $ export AWS_ACCESS_KEY_ID=Your_AWS_Access_Key_ID
    $ export AWS_SECRET_ACCESS_KEY=Your_AWS_Secret_Access_Key
    
    $ python2
    Python 2.7.3 (default, Apr 24 2012, 00:00:54) 
    [GCC 4.7.0 20120414 (prerelease)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import boto
    >>> connection = boto.connect_sdb()
    >>> domain = sdb_connection.create_domain('glacierPhotos')
    >>> domain = connection.create_domain('glacierPhotos')
    >>> domains = connection.get_all_domains()
    >>> domains
    [Domain:glacierPhotos]
    >>>quit()

Next, after downloading the glacierFreezer jar, I need to think about what to back up. This will be "fire insurance" for our digital valuables, so let's pick something I would lose in a fire: wedding photos. In the Glacier management console, I create a "vault" named "photos". Now, let's test our new backup system with a script that will send my wedding photos to Glacier:
    
    #!/bin/sh                                                                                                                           
    dir=$1
    
    for file in `find $dir`
    do
        java -jar glacierFreezer.jar 'accessKey' 'secretAccessKey' glacierPhotos photos $file
    done

Run the script, and wait while 15 GB of jpegs are uploaded to Glacier. Theoretically, this will cost me $0.15 per month. The cost of retrieval is higher, and it seems like there is some [difficulty in predicting the exact cost](http://www.wired.com/wiredenterprise/2012/08/glacier/) at this point in time. Since this is a sort of offsite data insurance plan, the cost of retrieval will be worth it.


