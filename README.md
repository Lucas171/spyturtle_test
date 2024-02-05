# SPY TURTLE

steps to begin!

1. Download files to a folder of your choice
2. Open in IDE
3. in terminal in location of app.py run:
  ```
  pip install Flask Flask-SocketIO 
  ```
4. cd into flask folder
5. In the terminal run app.py to start the flask app

NOTE: at this point your flask app is running on your local host port 5000 and waiting for a socket.io message

7. in a seperate terminal cd to the root directory where main.py is
8. in the termial run ```python3 main.py```

NOTE: this will send an image to the websocket for the webapp to recieve. you should now see the image appear on the screen.
If not run the previous command again.

