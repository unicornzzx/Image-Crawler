## Introduction & Declaration 
This repository is a record of my previous work done for Computer Networking course. It's a image crawler which can simultaneously download images from websites(**http**) and save them on user's local system. 

Skills & Knowledges I learned through this programming experience:

* use TCP socket build my own http requests and handle the replies
* use regular expression to handle the format issue for URLs
* use mutli-threading to speed up the program
* some other knowledges of computer networking

## Example
http://csse.xjtlu.edu.cn/classes/CSE205/ is an example website which can be used to demonstrate the usability of this image crawler.

There are parts of the source code of above website:

<img src="/images/sourcecode1.jpg" height="300px"> <img src="/images/sourcecode2.jpg" height="300px"> <img src="/images/sourcecode3.jpg" height="300px">

Test record:   
* the input ```url``` is the starting point of the crawl
* the ```depth``` is how many pages deep the crawler will go
<img src="/images/init.jpg"> <img src="/images/running.jpg">

**You can find the downloaded images for above test [here](/images/csse.xjtlu.edu.cn/classes/CSE205/).**
