# README #

Python shell utilities

A better cd: pcd
================

A better cd utility for linux shell . Inspired by autojump and Charles Leifer's  blog post
	http://charlesleifer.com/blog/-j-for-switching-directories---improving-the-cd-command-/
Pattern matching from history of browsed files using "pcd"

Example 1: Same Weight folders /home/<user-name>/Documents and Downloads are 9 characters each, so more recent is preferred
       ```bash
       $ pcd Downloads/
       $ pcd /home/<user-name>
       $ pcd D          # goes to Downloads folder
       $ pcd /home/<user-name>/Documents
       $ pcd /home/<user-name>
       $ pcd D       #Now goes to Documents folder because Documents is more recent
       $ pcd Dow     #Will go to Downloads
       $ pcd D       # Will remain in downloads
       ```

Example 2: Different weight folders /home/<user-name>/py-src , /home/<user-name>/py-build start with 'py-' but build has more characters /home/username/py-build so py-src is preferred because it is shorter
    ```bash
    $ pcd py-src
    $ pcd /home/<user-name>
    $ pcd py-build
    $ pcd /home/<user-name>
    $ pcd py   # py-src is preferred typing py-b would have taken you to build
    ```
List ten recent visits of directories using -l option
Example 3: List and select
      ```bash
      $ pcd -l #prints list of ten recent folders input number to navigate
      ```
Installation
============
Clone Repository
```bash 
   $ git clone https://github.com/vrakesh/pcd-python-cd
```
Run
```bash
    $ sudo install.sh
```
        
