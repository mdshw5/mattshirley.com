title: DigitalOcean as a VPS provider
post_date: 2013-08-12 10:25:00
post_name: digitalocean-as-a-vps-provider

# Why I use DigitalOcean as a virtual private server provider

1. Price  
I could have started with performance or interface, but it's the price that initially drew me to [DigitalOcean](https://www.digitalocean.com/?refcode=42716f29b42d). 
For $5 / month (billed at $0.007 / hour) you get a fast, if somewhat resource limited virtual server as well as 1 terabyte of outgoing data transfer.

2. Interface  
While Amazon certainly has a diverse and mature array of PaaS products, DigitalOcean absolutely kills Amazon EC2 when it comes to provisioning a server. 
The provisioning process takes less than one minute in most cases. You simply assign a hostname, choose a server size, and select a Linux distribution. System backups 
are optional and completely automatic, and cost 20% above the hourly cost of the server alone. All information is clearly presented and updates are responsive.

3. Performance  
Even the smallest DigitalOcean servers are [well balanced](http://uncrunched.com/2013/08/07/digital-ocean-v-aws-10x-performance-for-13-cost/), and are 
certainly priced well below what other vendors would charge. Factor in the disk IO of hundreds of MB per second and you might get away with 
[zRam](http://en.wikipedia.org/wiki/ZRam) and a small swap image.

I'm hosting both this site, as well as a [research project](http://tripod.mattshirley.com) on DigitalOcean and cannot recommend it enough. 
[Try it out](https://www.digitalocean.com/?refcode=42716f29b42d)!