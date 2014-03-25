title: Automating Apple time machine backups to Amazon Glacier using python, tar, and zfs
link: /automating-apple-time-machine-backups-to-amazon-glacier-using-python-tar-and-zfs/
creator: matt
description: 
post_id: 456
post_date: 2013-01-23 17:14:51
post_date_gmt: 2013-01-23 21:14:51
comment_status: open
post_name: automating-apple-time-machine-backups-to-amazon-glacier-using-python-tar-and-zfs
status: publish
post_type: post

# Automating Apple time machine backups to Amazon Glacier using python, tar, and zfs

In a [previous post](/cold-storage-freezing-my-backups-in-amazon-glacier/) I played around with Amazon Glacier, using a tool called [glacierFreezer](http://www.glacierfreezer.com). Since then, I've wanted to automate backups of my Time Machine archives, as well as my photos and home directories. Looking around for more current Glacier interfaces I noticed a project called [glacier-cmd](https://github.com/uskudnik/amazon-glacier-cmd-interface) which looks promising. The core utilities are written in Python, and provide means to upload, download, and query Glacier vaults.
    
    git clone https://github.com/uskudnik/amazon-glacier-cmd-interface.git 
    cd amazon-glacier-cmd-interface 
    sudo python setup.py install  
    

After we install _glacier-cmd_, let's start creating our backup script to upload files located in a certain directory, as well as check that we don't have too many copies of those files stored already on Glacier. We should keep the last three months of Glacier archives, since deletion prior to three months results in a pro-rated charge. First we need to create a SimpleDB domain to store the glacier-cmd cache:
    
    python
    >>> import boto
    >>> sdb = boto.connect_sdb('your_access_key', 'your_secret_key')
    >>> sdb.create_domain('glacier-cmd')
    >>> quit()
    

Now let's start our script. We want a wrapper script that passes all of our AWS information, as well as some information about logging and AWS region. We'll set SimpleDB domain we created so we can have a cached inventory of our vaults and their contents. We'll want a function that creates a new vault (based on the date and name of the backup set) and uploads some data to it. I've written two methods: (1) Using _tar_ and (2) using _zfs send_. Both methods compress the backup using _bzip2_, although the zfs method uses a more advanced "snapshot" of the filesystem which will accurately reflect the state of the backup set even if data are added or removed during our upload. We will also want a function that cleans up backup sets. I've hard-coded this to a value of 3 months old backup sets, since Glacier expects that data will reside for this minimum period.
    
    #!/bin/bash
    # Usage:
    # glacier_backup.sh backup-job-name action folder-to-backup
    # action=(backup,cleanup,zfsbackup)
    
    # AWS access keys
    access_key='your_access_key'
    secret_key='your_secret_key'
    
    # glacier-cmd configuration
    region='us-east-1'
    bookkeeping_domain='glacier-cmd'
    logfile=/var/log/glacier.log
    loglevel=INFO
    output=print
    
    # Command line invocation of glacier-cmd with variables passed
    glacier_cmd="
    /usr/local/bin/glacier-cmd\
     --aws-access-key $access_key\
     --aws-secret-key $secret_key\
     --region $region\
     --bookkeeping\
     --bookkeeping-domain-name $bookkeeping_domain\
     --logfile $logfile\
     --loglevel $loglevel\
     --output $output
    "
    
    # Debugging options
    if [ "$1" == "debug" ]; then
        $glacier_cmd $2
        exit 0
    fi
    
    # The name of the backup job
    backup_job=$1
    path_folder=$3
    
    if [ "$2" == "backup" ]; then
        hello=`date --date='now' +%b%g`
        vault="$backup_job$hello" # A unique vault name created from today's date plus job name
        $glacier_cmd 'mkvault' $vault # Create this vault
    # Tar and compress directory, then upload from stdin
        tar cjf - $path_folder | $glacier_cmd 'upload' $vault --stdin --name ${path_folder#/}.tar.bz2
    fi 
    
    if [ "$2" == "zfsbackup" ]; then
        hello=`date --date='now' +%b%g`
        vault="$backup_job$hello" # A unique vault name created from today's date plus job name
        $glacier_cmd 'mkvault' $vault # Create this vault
    # Use ZFS send, then upload from stdin
    # If using ZFS send, $path_folder must be "pool/filesystem" with no preceding "/"
        pool_filesystem=${path_folder#/}
        /sbin/zfs snapshot "$pool_filesystem@$vault"
        /sbin/zfs send "$pool_filesystem@$vault" | bzip2 | $glacier_cmd 'upload' $vault --stdin --name ${pool_filesystem}.zfs.bz2
        /sbin/zfs destroy "$pool_filesystem@$vault"
    fi 
    
    if [ "$2" == "cleanup" ]; then
        goodbye=`date --date='3 months ago' +%b%g`
        vault="$backup_job$goodbye" # The vault from three months ago - may not exist!
        $glacier_cmd 'rmvault' $vault
    fi
    

We can set up two _cron_ jobs for the beginning of every month to upload and cleanup a set of ZFS filesystem backups:
    
    00 02 01 * * /home/matt/scripts/glacier_backup.sh timemachine zfsbackup socrates/TimeMachine
    00 01 01 * * /home/matt/scripts/glacier_backup.sh timemachine cleanup
    

That's it.