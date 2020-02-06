# How an audiophile chump adds a little thump

I've been listening to music in our living room (which is indisputably the nicest room in the house) using only a pair of 
[Cornered Audio Ci4-V](https://www.cornered.dk/shop/c3-a65yy-nmw4a) speakers. 

![](http://mattshirley.com/uploads/2019/01/IMG_2758.jpg)

Relative to their small cabinet and 4" speaker 
cone size, these are very capable speakers, with relatively flat response between 80-20,000hz, and noticeable extension down 
to 70hz. These are the first speakers that I've listened to that use a 
[passive radiator design](https://en.wikipedia.org/wiki/Passive_radiator_(speaker)), which improves their bass reproduction and 
also increases their power handling, with a descreased overall sensitivity. I really like the idea of designing the smallest 
possible speaker cabinet that can perform well in a relatively small space, and so I decided that my system needed more 
bass.

<div style="width:100%;height:0;padding-bottom:100%;position:relative;"><iframe src="https://giphy.com/embed/1gO2qJJs29aw0" width="100%" height="100%" style="position:absolute" frameBorder="0" class="giphy-embed" allowFullScreen></iframe></div><p><a href="https://giphy.com/gifs/daft-punk-bass-1gO2qJJs29aw0">via GIPHY</a></p>

Most small commercial subwoofers for home audio are [extremely pricey](http://www.sunfire.com/product/atmos-dual-65-1400w-tracking-down-converter-powered-sub-auto-eq-brushed-aluminum-cab-XTATM265) and 
capable, or [still expensive](http://velodyneacoustics.com/subwoofers/microvee-6-5-black-207.html) and less capable than other larger 
subwoofers on offer. Also, forget about finding an affordable, good performing option with a white cabinet (critical for the 
all-important *Wife Approval Factor*).

## DIY passive radiator microsub
> What's a guy to do when he can't find the right toys to buy?

After failing to find a commercially available subwoofer in my budget (<$400), and with the right aesthetics and performance, 
I decided to look at parts for building my own "microsub". Parts Express has a fantastic line of DIY speakers and speaker building 
supplies, and so I began my search for a suitable driver for my small sub. Chinese manufacturer Tang Band makes all kinds of 
neat small form factor drivers, and I settled on a 5-1/4" Tang Band [W5-1138SMF](https://www.parts-express.com/tang-band-w5-1138smf-5-1-4-paper-cone-subwoofer-speaker--264-917). 
This relatively tiny speaker has crazy specifications for its size. The most important to me being a 9mm Xmax and 45hz FS, with a 
compliance that allows vented box designs to reach close to 35hz at -3dB. That's pretty low extension for a 5" driver! At $43 I decided 
this was a great speaker to design my subwoofer around, and so I set about figuring out how to design a vented enclosure that minimizes total 
volume. This design turned out to be difficult to achieve with a typical ported box. For a box of <1cu foot I'd need ports that are much, 
much longer than 12", and so I turned to passive radiators.

Passive radiators allow you to design a vented enclosure by substituting the volume of air contained in the port tube with 
the volume of air that the passive radiator cone moves, which is the cone area (Sd) times the maximum excursion (Xmax). I chose 
the Dayton Audio [DS175-PR 6-1/2"](https://amzn.to/31rcVjI) passive radiator 
for its ability to move about as much air as the W5-1138 driver: `94cm2 * 9.25mm = 86,950mm3` vs. `128.7cm2 * 8mm = 102,960mm3`. 
To avoid over-excursion, passive radiators are usually chosen to move twice as much air as the active driver, so I used two.

For an amplifier board I chose an [AOSHIKE TPA3116 DC 12-24v 100W Subwoofer Amplifier Board](https://amzn.to/2TiZVry) which, at $15, 
provides a volume control, adjustable low pass filter, and clean 100W output at 4ohm. As good as the amp sounds I would have paid 
twice as much. It requires a high current DC power supply [such as this one](https://amzn.to/2RWMIqm). 
Wiring the amplifier board required a [voltage divider](http://www.epanorama.net/circuits/speaker_to_line.html/) circuit with a [few resistors](https://electronics.stackexchange.com/a/100309) to step down the 50wpc speaker level to ~2V line level. 

For the speaker cabinet, I chose to use existing 3/4" particleboard, thinking that I would rebuild the project using better quality 
MDF in the future. I'm actually fine with the finished product, and the particleboard is nice and heavy. The active speaker is down 
firing, and I placed the passive radiators on opposing sides. This allows me to hide most of the speakers without flush mounting or using speaker cloth, 
and keeps the overall external dimensions of the box as small as possible. 

![](http://mattshirley.com/uploads/2019/01/IMG_2272.jpg)

The box design is a simple 9"x8"x8" cube, which is just large enough to accommodate the huge magnet on the driver, the two PRs, 
and the amplifier board.

![](http://mattshirley.com/uploads/2019/01/IMG_2273.jpg)

After a few coats of Bondo and some light sanding it doesn't look too bad - although I plan to fix up the corners and paint 
the enclosure a matte white.

![](http://mattshirley.com/uploads/2019/01/IMG_2755.jpg)

The cutout for the amplifer board required some work with a jigsaw, and I fabricated a plexiglass plate to seal off the back (with some 
putty to cover the 3.5mm input). Speaker level inputs come through [binding posts](https://amzn.to/372ZRlL). 

I added [some feet](https://amzn.to/2v3uZo3) to give the 
down-firing speaker enough clearance, and mounted the speakers using [these nice machine screws with backing nuts](https://amzn.to/2RZxosR).

WinISD modeling of my 0.19ft3 cabinet helped me determine that I needed to add at least 25 grams of weight to the passive radiators 
to avoid a huge peak at 80hz, so I used two 1-1/2" steel fender washers along with a neoprene washer to protect the spider from damage.

![](http://mattshirley.com/uploads/2019/01/IMG_2754.jpg)

I initially designed the cabinet so it would fit inside of my record cabinet:

![](http://mattshirley.com/uploads/2019/01/IMG_2283.jpg)

But after listening to the speaker (and deciding that I couldn't part with half of my record collection) I found that 
placing it beside the cabinet sounded best.

![](http://mattshirley.com/uploads/2019/01/IMG_2756.jpg) 

The end result sounds pretty good. At 25% gain the output is more than sufficient to add enough bass, and by playing tones 
through the system I can hear reproduction down to 29hz. During listening I hear useful extension to about 40hz, which is backed up 
by my measurements with and without the subwoofer:

![](http://mattshirley.com/uploads/2019/01/microsub_spl_nosmooth.png) 

These measurements were made from a listening position about 2 meters from the subwoofer, and 8 meters from the primary speakers. 
How does it sound? It's not going to wake up the neighbors, or even bother everyone living in your house (which for me is a good thing), 
but the bass reproduction is smooth and tight, with good transient response evident on tracks such as [Jaco Pastorius' Portrait of Tracy](https://www.youtube.com/watch?v=nsZ_1mPOuyk). 
For less than $150 I can't find any other designs that come close to producing so much good sound in such a small package. 

![](http://mattshirley.com/uploads/2019/01/IMG_2757.jpg)
