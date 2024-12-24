# Shadowing App
The shadowing technique is a language learning method that involves repeating what you hear in a foreign language as closely as possible.

## How this App works
- Paste a YouTube video URL and click in Download.
- The App will split the audio into sentences.
- Record your voice repeating what you've heard as closely as possible.

## Example
<img src="./assets/gif/app-intro.gif" />

## To run the back-end
First you need to install FFmpeg on your machine: [FFmpeg](https://www.ffmpeg.org/download.html) <br>

Change the HOST var in "main.py" file: <br>
```HOST = <your network IP goes here>```

Install the dependecies: <br>
```pip install -r requirements.txt```

Now you can run: <br>
```python main.py```

When you're using the App make sure that you are connected to the same internet connection as the server.

React Native repo: [Shadowing-App-react-native](https://github.com/GabriellBarbosa/Shadowing-App-react-native)