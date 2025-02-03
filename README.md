## MY TODO

- [x] Design for mobile
- [x] card component
- [x] Text input field component
- [x] Login page (IMPORTANT)
- [x] Register page (IMPORTANT)
- [x] Logout page (MIDDLE)

- [x] Finish the .json terms and service file EN
- [x] Finish the .json private policy EN
- [x] Finish the .json terms and service file FR
- [x] Finish the .json private policy FR (need to review)
- [x] Finish the .json terms and service file DE
- [x] Finish the .json private policy DE (need to review)


- [x] Profile page (MIDDLE)
- [x] (got the structure of it, stats component + history + friends)

- [x] Start Language page to be able to change language (MIDDLE)
- [x] Settings sidebar component (MIDDLE)

- [x] Credits page


- [x] Game choice page (MIDDLE)
- [x] Game mode page (MIDDLE)
- [x] Pong page (IMPORTANT)

- [x] Searching opponent page

- [x] Create tournament or Join tournament
- [x] Waiting for players
- [x] Matchmaking page (IMPORTANT)

- [x] Already fill text field component where i can modify it
- [x] Account page (IMPORTANT)
- [x] Make the sidebar of the Parameter mobile friendly

- [x] Tic Tac Toe page (IMPORTANT)
- [x] Tic Tac Toe game page (IMPORTANT)

- [x] Add in mode choice, 4 players games

- [x] Make the multi player icon
- [x] Start Appearence page to be able to change theme (MIDDLE)
- [x] Add Teapot theme to have power up


- [ ] Implement power up

- [ ] Add in Avatar component the possibility to modify the image

- [ ] Add the tournament id when creating the tournament
- [ ] Make the tournament matchmaking page to game better

- [ ] How do we add a friend ?
- [ ] In friend, add a chat component
- [ ] In friend, add a way to tell if the friend is online


- [ ] Tic Tac Toe AI


        ## When I can communicate with the back
- [ ] Make each part into container

- [ ] Call the back for the game
- [ ] Matchmaking logic
- [ ] Tournament logic
- [ ] Games logic with following pages...

- [ ] Can register
- [ ] Can login
- [ ] Can logout

- [ ] Call the back for stats
- [ ] Call the back for history (ten last battles)
- [ ] Call the back for friends list (max of 10)
- [ ] Add a component for the chat ?

- [ ] Call the back for account --> PATCH request to modify informations + avatar
        - [ ] Can modify avatar
        - [ ] Can modify username
        - [ ] Can modify password
        - [ ] Can modify email

- [ ] Pong AI


- [ ] More than 2 players game page (x2)



(Presentation du "produit", Les jeux, Les services, Les commandes (how/notice), Tout est details (user-friendly))
# Ft_Transcendence

### Table of Content

## Introduction
This project is the final projet of the 42 common core. As the subject states, we have the possibility to choose up to 7 major modules to complete it.
I did this project with [@Lapinew](https://github.com/Lapinew) and [@gkubina](https://github.com/gkubina).

TL;DR, This is a web application built using the Django framework. It features a server-side implementation of the classic Pong game, designed with a microservices architecture using docker. The application supports remote players, user management, authentication, and multiple languages and themes. Additionally, it includes advanced features such as AI opponents, live chat, and multiplayer support (4 players in the same game).

## Description
**Major Modules**
- Framework: The project is built using the Django framework.
- Server-Side Pong: Replaces the basic Pong game with a server-side implementation and provides an API.
- Microservices Architecture: The backend is designed as microservices to enhance scalability and maintainability.
- Remote Players: Supports gameplay with remote players.
- User Management: Includes standard user management, authentication, and user handling across tournaments.
- Remote Authentication: Implements remote authentication to enhance gameplay and user experience.
- Additional Game: Adds another game with user history and matchmaking features.
- AI Opponent: Introduces an AI opponent for single-player mode.
- Live Chat: Integrates a live chat feature for real-time communication.
- Multiplayer Support: Supports more than two players in the same game.

**Minor Modules**
- Database: Uses PostgreSQL for the backend database.
- Multiple Language Support: Supports multiple languages to cater to a diverse user base.
- User and Game Stats Dashboards: Provides dashboards for user and game statistics.
- Game Customization Options: Allows users to customize game settings.
- Device Support: Ensures compatibility across all devices.


## The Project
put screenshot + "tuto"

## Quick Start
```
git clone git@github.com:KoganeShiro/ft_transcendence.git
cd ft_transcendence
```

or the link of the github page ??

## Usage
If you don't have make or docker and docker composed installed, you should in order to compile and run this project

If you did, then you can make and follow the instruction !
```
make
```