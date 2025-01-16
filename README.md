# ft_transcendence

### Table of Content
- [Mandatory Rules](#mandatory)
- [Modules](#modules)
<!--
    - [](#)
	- [](#)
-->

[trello](https://trello.com/b/r4gjArPg/fttranscendence)
[figma](https://www.figma.com/design/StkSWr1YVLh2fYExErcrea/Transcendance?node-id=0-1&t=TEepryumGqKd7wGn-1)

Framework module:
    Django ?

Database module:
    PostgreSQL

### Mandatory 

The user should be able to use the Back and Forward buttons of the browser

Your website must be compatible with the latest stable up-to-date version of
Google Chrome 

The user should encounter no unhandled errors and no warnings when browsing the
website.

Everything must be launched with a single command line to run an autonomous
container provided by Docker . Example : docker-compose up --build
    You can’t use so called “bind-mount volumes” between the host and the container if non-root UIDs are used in the container


Mult local player:
    Ask the account owner (if not guest mode) to write the username of the second player

Mult remote player (will be like solo):
    Wait page to find another player (or the AI)

A player must be able to play against another player, but it should also be possible to propose a tournament. This tournament will consist of multiple players who can take turns playing against each other. You have flexibility in how you implement the tournament, but it must clearly display who is playing against whom and the order of the players

A registration system is required: at the start of a tournament, each player must input their alias name. The aliases will be reset when a new tournament begins. However, this requirement can be modified using the Standard User Management module.

There must be a matchmaking system: the tournament system organize the matchmaking of the participants, and announce the next fight

During the evaluation, the team will justify any usage of library or tool that is not explicitly approved by the subject


• Any password stored in your database, if applicable, must be hashed.
• Your website must be protected against SQL injections/XSS.
• If you have a backend or any other features, it is mandatory to enable an HTTPS connection for all aspects (Utilize wss instead of ws...).
• You must implement some form of validation for forms and any user input, either within the base page if no backend is used or on the server side if a backend is employed.
• Regardless of whether you choose to implement the JWT Security module with 2FA, it’s crucial to prioritize the security of your website. For instance, if you opt to create an API, ensure your routes are protected. Remember, even if you decide not to use JWT tokens, securing the site remains essential.

For obvious security reasons, any credentials, API keys, env variables etc... must be saved locally in a .env file and ignored by git. Publicly stored credentials will lead you directly to a failure of the project.


### Modules

◦ Major module: Use a Framework (Django)

◦ Minor module: Use a front-end [Bootstrap toolkit](https://getbootstrap.com/) (with only vanilla js ?)

◦ Minor module: Use a database for the backend. ([ProgreSQL](https://www.postgresql.org/))

◦ Major module: Replacing Basic Pong with Server-Side Pong and Implementing an API.

◦ Major module: Designing the Backend as Microservices.

◦ Major module: Remote players

◦ Major module: Standard user management, authentication, users across tournaments.

◦ Major module: Implementing a remote authentication. Gameplay and user experience



◦ Minor module: Support on all devices.
◦ Major module: Add Another Game with User History and Matchmaking.
◦ Major module: Introduce an AI Opponent.
◦ Major module: Multiplayers (more than 2 in the same game)
◦ Minor module: Multiple language supports.

◦ Minor module: Game Customization Options.
◦ Minor module: User and Game Stats Dashboards
◦ Minor module: Add accessibility for Visually Impaired Users.


### Github
https://github.com/C-est-quand-la-prochaine-reu-han
https://github.com/LaTeam-Trancendence/transcendence
