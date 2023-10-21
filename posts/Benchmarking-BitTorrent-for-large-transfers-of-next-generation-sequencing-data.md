title: Benchmarking BitTorrent for large transfers of next-generation sequencing data
creator: matt
post_date: 2013-07-15 08:36:00
post_name: Benchmarking-BitTorrent-for-large-transfers-of-next-generation-sequencing-data

# Benchmarking BitTorrent for large transfers of next-generation sequencing data

Intrigued by this [post at Biostars](http://www.biostars.org/p/76628/), which asks for a wide-area network transfer utility that has:

> - Multiple TCP streams or UDP for very fast transfer of bulk data
> - Similarly sensible re disk writes, threads, poll/select and copying to get stuff onto disk quickly
> - Checking of ownership and permissions as well as checksumming at both ends
> - Handles multiple small files as efficiently as very large files
> - Can run "rsync-style", only transferring diffs when appropriate
> - Has good security integrity and authenticity guarantees (secrecy not required)
> - good quality linux server and client with robust error detection and reporting.

I proposed that the BitTorrent protocol might allow for efficient internet transfer of sequencing data between (at least) two computers. After searching the internet for comparisons between BitTorrent and Aspera and rsync I realized that no one is taking the BitTorrent protocol seriously for transfer of research data. Therefore I set out to benchmark an `rtorrent` transfer of a 29 GB fastq file between two compute nodes on a gigabit local network. This should simulate an extremely low-latency, high bandwidth scenario where protocol overhead could become an issue.

First we need to create the `.torrent` metainfo file that describes the announce URL (-a localhost) as well as block size for hashing (2^n; 2^18 = 256 kb blocks) and number of threads to use for calculating hashes. Note the we're specifying a single file, but this utility can run on multiple files or an entire directory.

    mktorrent -a localhost -l 18 -t 4 testData.fastq

Runs in 18 seconds on our hardware. Next we need to transfer our 2 kb "torrent" file to the receiving node:

    scp testData.fastq.torrent testnode1:/scratch/matt

Now we start `rtorrent` on testnode0:

    mkdir session
    rtorrent testData.fastq.torrent

Runs in 400 seconds, checking each 256 kb block of the file `testData.fastq` for consistency against the values precomputed in our "torrent" file. This step is most likely single-threaded in rtorrent. Not the configuration values supporting encryption and peer discovery at the end of this post.

Now we ssh to testnode1 and run:

    mkdir session
    rtorrent testData.fastq.torrent

We need to add the peer directly to our new client since we aren't using a tracker: `^x add_peer=testnode0:6881` where 6881 is the port the first client is bound to. The download should start immediately.

# Results

## BitTorrent
26000 megabytes / 460 seconds * 8 bits / byte = 452 megabit/s

## scp
26000 megabytes / 738 seconds * 8 bits / byte = 281 megabit/s

An encrypted BitTorrent transfer over a gigabit network with low latency leads to a 1.6X increase in throughput compared to `scp`. Since the BitTorrent protocol was created for high latency transfers, I think this shows that the protocol can utilize a high bandwidth link to reliably transfer research data quickly via the internet.

## .rtorrent.rc configuration file:

    # Default session directory. Make sure you don't run multiple instance
    # of rtorrent using the same session directory. Perhaps using a
    # relative path?
    session = ./session

    # Encryption options, set to none (default) or any combination of the following:
    # allow_incoming, try_outgoing, require, require_RC4, enable_retry, prefer_plaintext
    #
    # The example value allows incoming encrypted connections, starts unencrypted
    # outgoing connections but retries with encryption if they fail, preferring
    # plaintext to RC4 encryption after the encrypted handshake
    #
    encryption = require

    # Enable DHT support for trackerless torrents or when all trackers are down.
    # May be set to "disable" (completely disable DHT), "off" (do not start DHT),
    # "auto" (start and stop DHT as needed), or "on" (start DHT immediately).
    # The default is "off". For DHT to work, a session directory must be defined.
    # 
    dht = auto

    # UDP port to use for DHT. 
    # 
    dht_port = 6881

    # Enable peer exchange (for torrents not marked private)
    #
    peer_exchange = yes


