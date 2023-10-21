title: Estimating costs associated with Cloudman Galaxy clusters on Amazon Web Services
post_date: 2013-07-17 11:20:52
post_name: Estimating-costs-associated-with-Cloudman-Galaxy-clusters-on-Amazon-Web-Services

# Estimating costs associated with Cloudman Galaxy clusters on Amazon Web Services

The following is a response to a question about costs associated with [Galaxy Cloudman](http://wiki.galaxyproject.org/CloudMan) from 
the Biotrac 45 workshop email list:

> Hi <s>redacted</s>. I would direct you to [this page](http://wiki.galaxyproject.org/CloudMan/AWS/CapacityPlanning) which details capacity planning for AWS under "scenario 2" for medium/heavy usage. You'll have to plan on using data sets for each type of analysis of an appropriate size so that you can complete the lab within 3 hours. For planning and testing I recommend just bringing up a cluster and trying to complete the lab. If it takes too long, maybe remove data for a few chromosomes.

> Regarding price, using the [calculator Amazon provides](http://calculator.s3.amazonaws.com/calc5.html) I can come up with two billing scenarios for a Galaxy cluster (see attached screenshots). Since Cloudman automatically scales the cluster to a maximum of 19 worker nodes and terminates idle nodes after one hour calculating cost is tricky. I can come up with a "best" and "worst" case scenario. Both scenarios are cost for running the cluster 24 hours and then shutting it down:

> Scenario 1: a 19-node cluster maintained at maximum utilization  
> $252 / 24 hours = $10.50 per hour

> Scenario 2: a 1-node cluster maintained at minimum utilization  
> $42 / 24 hours = $1.74 per hour

> This is for a cluster with 1 terabyte of data storage for job history datasets. It's worth remembering that everything is billed hourly, so these prices will scale perfectly out to an entire month (calculated 24 hours in a day, 30 days in a  month).

> Regarding your own hardware, let's configure comparable Dell clusters:

> Scenario 1: a 19-node cluster of 1x R510 (head node) and 19x R210 (worker node)  
> $2012 + 19($1053) = $28,667

> Scenario 2: a 1-node cluster of 1x R510 (head node) and 1x R210 (worker node)  
> $2012 + $1053 = $3063

> In addition you have to have someone configure the cluster, periodically fix issues with the configuration, and service failed hardware (which will happen) and pay for power usage, network switches, and a rack to place it all in. The upshot comes over the course of a few years for your fixed cost:

> AWS 19 node cluster over 1 year:  
> $252 * 365 days = $91,980 per year

> AWS 1 node cluster over 1 year:  
> $42 * 365 days = $15,330

> If you are planning to use the cluster even 50% of the time over the first year you're better off buying your own. In my lab, we have an 8 node cluster sitting at ~20% utilization for what it's worth. Most people severely overestimate their ability to efficiently use compute resources long-term, so it ends up being cheaper / easier to rent it from Amazon or another cloud provider.