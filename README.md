Final project:
This project is a website which allows users, who sign-up for free profiles, to connect with friends, work colleagues or people they don’t know, online. It allows users to share own thought, opinions, and activities with however many people they like. It provides user with access to current weather status and encourages user to engage in small talk and leave posts in the message board.

Users send “friend requests” to people who they may – or may not – know. They can meet friends in the message board or through the Live Chat application that allow users to choose different chatrooms and have live instant conversations with other users all over the world.


Requirements:
This web application utilizes HTML, CSS, Javascript, Python, Django (including at least one model), Django Channels, Redis. Because I use windows OS, I also use Docker and WSL 2 to run Redis.

1. Weather API - Current Weather information at user current location using geolocation and API
2. Mobile Responsive - Adaptable for mobile user
3. Add Post - Users who are signed in should be able to write a new text-based post
4. Infinite Scroll - Allow user to scroll through message board by scrolling to the bottom of the screen
5. FriendList - A list of friends
6. Friend request - A list of friend requests from other users and buttons that allow user to accept or ignore them
7. Profile page - A page to show user profile and user's recent post
8. Add friend - A button in profile page to send a friend request
9. Bonus: Live chat beta - An app that allow user to choose different chatrooms and engage in live conversations with other users in real time


There are 2 apps in this project: weather and chat.

Weather app includes basic Django starter files like urls, that takes the user to different pages by running functions through views.py and rendering the specific HTML file. Paths include homepage, login, logout, register, profile page, friend requests page, friend list page and API routes that include functions to create post, add friend, request friend, and load posts which could be found in views.py. After loading a HTML page with CSS as stylesheet and jpg files as pictures, the app uses either weatherapp.js or profile.js (depending on the page) to fetch api for current weather information, load old posts using infinite scroll, load icons, add new post, load profile page, friend requests and accpeting requests. In models.py there are 3 models: User for user data, Post for post data, and UserFriend for data relating to user added by another user. In UserFriend model user_id is the user added by the other user who is listed in the friending_user_id column. If the relationship is one sided, that means a friend request had been sent to user listed under user_id. If however the relationship is mutual or both sided (they both added each other), then they are "friends" and will appear on each other's friendlist. Adding and accepting friend has the same effect in the database. 

Chat app uses Django Channels 2 to handle websockets and connections asyncrhonously. It uses Docker to install and run Redis as backing store for the channel layer. Chat app includes 2 url paths: index and room name. In index.html, Javascript is included to allow user to enter name of the chat room and be directed to that page. In room.html, the page shows the name of room the user had entered and a chatbox for the user to engage in live conversations with other users.