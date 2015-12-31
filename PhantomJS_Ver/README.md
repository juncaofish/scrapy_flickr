#Crawl flickr photo
Use PhantomJS to load flickr website and trigger the scrollbar for more photos
Anyway, there seems to be an issue that the dynamic webpage can only have a toal size of 3MB (about 2000 photos each page). So, the timestamp parameters are required to split all the searching results to a certain interval.
scrapy crawl flickr -a emotion="happy face" -a start=20151201 -a interval=30


