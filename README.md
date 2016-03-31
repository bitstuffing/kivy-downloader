This project is based on GNU v2 and shared on github.com to the community to learn, make improves and promote the use of Kivi, because it's the best library for python.

Kivy-downloader is a simple app to test the powerful Kivy library and the possibilities which brings to developers.

It's just an instance of how the people can build multi-platform interfaces and recycle code, very important issue in this world.
 
You're the unique responsible of the use of this app. If you do an wrong use of this app or you see something that it's illegal in your country, please go to the people/entities which have published the content. 
The developer of this app is not responsible of nothing, and less by third people.
This app have not any content, so if you change params to see illegal content or browse to page which offers illegal content you are the unique responsible.

It's hoped be clear enough. Ok, great, let's work. 

First time you'll need checkout the code, into this code there are several files.

The main.py is the launcher, so to get working this app you should run (using python2):
 
*python main.py*

It will appear something like the following:

![alt tag](https://3.bp.blogspot.com/-HBnS-2dygb8/Vvz-3WNpKWI/AAAAAAAAASM/gFM96AOuN9MLvczEnueaC-cly_FgF8UUw/s320/form1.png)

To install library please follow the official wiki from kivy:

[Official wiki howto](https://kivy.org/docs/installation/installation.html)

If you're in ArchLinux you'll probably want to install the kivy library with yaourt, or Ubuntu with apt-get.

Also there is a file (buildozer.spec) which is the configuration used to test this app on Android. If you want to get the apk do:

*buildozer init* 

(it should override the previews buildozer.spec config file, so you can do a backup first)

*buildozer android deploy run logcat*

If you have an Android terminal/VM connected you will see it working, if not you can get the .apk from *bin* folder

Some screenshot of the first commit:
 
 ![screenshot2 with file explorer](https://4.bp.blogspot.com/-aPwCoIg_QpU/Vvz-3uXuP4I/AAAAAAAAASQ/5LbPwP5tG7geMyrkj0Ki_ppmmG91uIJSw/s1600/form2.png)
 
 ![screenshot3 with message](https://4.bp.blogspot.com/--EtLX3tV-_k/Vvz-3cW7CdI/AAAAAAAAASU/r1sL5s-ws481BeasHntxsFKEHATC46gpQ/s1600/form3.png)
 
 ![screenshot4](https://3.bp.blogspot.com/-QAogJxLrSjU/Vvz-3zjS_hI/AAAAAAAAASY/deIdC8wxs7sDdusDrWc5r2zx19XoLau6g/s1600/form4.png)
 
 ![screenshot5](https://4.bp.blogspot.com/-3R3MBDFlCl0/Vvz-6PC2MwI/AAAAAAAAASc/WbbhmMxVK7EgZsYiEmrJhwu9k593bKXlA/s1600/Captura%2Bde%2Bpantalla%2Bde%2B2016-03-31%2B12-40-49.png)
 
The GUI designs are inside downloader.kv file. 