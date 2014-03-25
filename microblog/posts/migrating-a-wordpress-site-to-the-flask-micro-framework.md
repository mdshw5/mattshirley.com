title: Migrating a Wordpress site to the Flask micro-framework
creator: matt
post_date: 2013-07-05 08:36:00
post_name: migrating-a-wordpress-site-to-the-flask-micro-framework

# Migrating a Wordpress site to the Flask micro-framework

I've wanted to move my web server to a virtual private server like Amazon EC2 for a while now, but couldn't justify the monthly cost. After hearing positive things about the price and performance of [DigitalOcean](http://digitalocean.com)'s VPS solutions I decided to provision a small server for $5 / month and see where it took me. Since my old server was running Debian 7 I decided to stick with what I know works.

DigitalOcean's provisioning is exceptionally fast! I went from signing up to logging in to my new server in under one minute. The performance is also decent for the price: you get 512 MB RAM  and 20 GB of solid state disk space on a server connected to the internet at 1 Gb/s. The CPU isn't even that bad, although you're limited to running only one process at a time.

Since I'm making significant changes in hardware I also decided to move away from Wordpress. There's nothing wrong with Wordpress, but I wanted to start developing some web applications in Python and Wordpress is written in PHP, and is also has an exceptionally large codebase. I needed something small and flexible and written in Python. Enter [Flask](http://flask.pocoo.org). 

My new site needed only a few rules:

1. Import all of the content written previously in Wordpress with minimal fuss.
2. No databases yet. I want to start simple and then learn about my options for database backends organically as I need one.
3. As much as possible, "don't repeat myself". I should be able to reuse templates and keep most of my code and data separate. Write most of my content in Markdown and then convert to HTML on the fly.

For exporting my pages and posts from WP to markdown I used a fantastic plugin [wp2md](https://github.com/dreikanter/wp2md) developed by [Alex Musayev](https://github.com/dreikanter). Once my pages were in individual [Markdown](http://daringfireball.net/projects/markdown/) files I was ready to start writing a blog framework. For project organization I used [this guide](http://charlesleifer.com/blog/structuring-flask-apps-a-how-to-for-those-coming-from-django/) by Charles Leifer. 

The app structure looks like:

    main\
         | app
         | main
         | views
         | models
         | templates
         | static
    posts\
          | post-about-something.md
    postlisting
    upload\
           | image1.jpg
    
The `postlisting` file is created by a function routed at `/update-entries` which is polled every hour by a cURL cron job. `postlisting` is read every time a request is encountered for the index, and contains date / title pairs on each line for the contents of the `posts` directory. 
Posts are loaded as Markdown files and parsed with `markdown.markdown` before rendering in a jinja2 template. The sidebar content as well as static pages are also rendered from Markdown on disk. All of the code is available on [GitHub](https://github.com/mdshw5/microblog). 