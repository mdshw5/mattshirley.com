title: WL v911 helicopter battery charger fix
link: /wl911-helicopter-battery-charger-fix/
creator: matt
description: 
post_id: 397
post_date: 2013-01-06 13:35:33
post_date_gmt: 2013-01-06 17:35:33
comment_status: open
post_name: wl911-helicopter-battery-charger-fix
status: publish
post_type: post

# WL v911 helicopter battery charger fix

I recently bought a really fun [mini RC helicopter](http://www.amazon.com/gp/product/B00762BMOI/ref=oh_details_o00_s00_i00). It's made in China by WL Toys, and it packs lots of technology into a ready to fly kit. Flying it has been a blast, but the manufacturing quality control leaves something to be desired. The remote control has a small piece of something rattling around in it, which doesn't affect the function at all. The battery charger is supposed to charge two of the Li-polymer batteries simultaneously, but it seems like mine only has one working port:

[![We need more red LEDs please.](/uploads/2013/01/IMG_0161-300x300.jpg)](/uploads/2013/01/IMG_0161.jpg)

Let's see what we can do about that. The bottom has four tiny screws and a small vent.

![Thank god it has screws.](/uploads/2013/01/IMG_0163-300x300.jpg)](/uploads/2013/01/IMG_0163.jpg) 

Inside there is a small, roughly finished board with some SMD components. It looks like a few resistors and maybe voltage regulators.

[![The top of the board looks fine. Reads "Hong Li".](/uploads/2013/01/IMG_0167-300x300.jpg)](/uploads/2013/01/IMG_0167.jpg) 

[![Underneath the lid.](/uploads/2013/01/IMG_0164-300x300.jpg)](/uploads/2013/01/IMG_0164.jpg) 

 

Looking at the bottom of the tiny board reveals a potential issue with one of the charging leads. It appears that the leads on the left channel are both soldered, but the right channel only has solder on one lead! Let's fix that right up with some lead-free solder.

 

 

 

 

[![Something missing](/uploads/2013/01/IMG_0166-300x300.png)](/uploads/2013/01/IMG_0166.png) 

 

[![Something added](/uploads/2013/01/IMG_0165-300x300.png)](/uploads/2013/01/IMG_0165.png) 

 

 

 

 

 

 

After adding a blob of solder to the pin and re-assembling the whole thing, it works! I was thinking about asking the seller to replace this part, but the entire fix took under 5 minutes with a small amount of work. My friend has this same helicopter kit, and he also had this issue with the first charger he received. It seems like someone was asleep on the assembly line.

[![It works!](/uploads/2013/01/IMG_0162-300x300.jpg)](/uploads/2013/01/IMG_0162.jpg) 

