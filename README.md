
# Youtube Tool
Download Youtube Video | Convert MP4 to MP3 | Generate Description File .txt | Create Transcript of Audio

![Youtube GUI](https://github.com/lucascrlsn/hello/blob/master/Other/youtube_main.png)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)      

## Dependencies:

*tkinter*
```python

pip3 install tkinter
```
*moviepy*
```python

pip install moviepy
```
*pydub*
```python
pip3 install pydub
```
*speech recongnition*
```python
pip3 install speech_recognition
```
*pytube*
```python
pip3 install pytube
```
*pillow*
```python
pip3 install PIL
```
*webview*
```python
pip3 install webview
```

## Notes:
**After cloning to your PC or Mac be sure to update lines 41 and 43 with the correct information. The application will open if not accomplished however there will be limited functionality without it. 

I am currently working on the following:
- multiprocessing for system logging
- stringVar updates for system logging (to replace cmd line printing)
- create a process to measure download speeds of user's network several times during the session to refine average speed over time. this would be used to drive progress bar for downloads thus giving the user an estimated time of completion for their files
