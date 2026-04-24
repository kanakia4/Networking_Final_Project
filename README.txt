# CSE 3461, Section 36975, Final Project
## Contributors: Esha Kanakia, Waiz Kayani, Hana Winchester

How to run final project:

Open 1 terminal for the server, and at least 2 terminals for the clients (the best would be 3 terminals. This would show the true difference between one-to-one and broadcast messaging).
Run the server file first using python server.py. May need to use python3 or py -3 depending on your OS and python version installed.
In the other terminals, run python client.py. This will begin the chat features.

The client terminals will ask to enter a username. Enter your name (ie, Hana).
From there, you are prompted to enter a message.
To send a broadcast message, write any message and hit enter. This will send a message to every client currently on the server.
To send a one-to-one message, type @[username] before your message. For example, if you want to send to Esha, put @Esha [message]. This will send communication only to that person.
If you have recieved a message, press Enter to acknowledge the message and send another message.

If you would like to send an image to the others, use /sendimage as the first argument of the message. Then, type the path for where the image is stored. For example, C:\Users\Esha\Desktop\BuckID.jpeg
The other users will get a notification of recieving an image, the size of the image, and the time and speed at which it was recieved. The client will be able to go into the directory where they are running the file (for example, the folder where you are running the code), and the image will be there to view.
