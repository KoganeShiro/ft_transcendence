# ft_transcendence

### Table of Content
- [Mandatory Rules](#mandatory)
- [Modules](#modules)
    - [Notes](#notes)
	- [Roadmap](#roadmap)
- [Launch](#launch)


[trello](https://trello.com/b/r4gjArPg/fttranscendence)

[figma](https://www.figma.com/design/StkSWr1YVLh2fYExErcrea/Transcendance?node-id=0-1&t=TEepryumGqKd7wGn-1)

Framework back module:
    Django ?

Database module:
    PostgreSQL/MariaDB

Framework front:
    Vuejs ?



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
~~◦ Minor module: Use a front-end [Bootstrap toolkit](https://getbootstrap.com/) (with only vanilla js ?)~~

◦ Major module: Use a Framework for the (Django)

◦ Minor module: Use a database for the backend. ([ProgreSQL](https://www.postgresql.org/))

◦ Major module: Replacing Basic Pong with Server-Side Pong and Implementing an API.

◦ Major module: Designing the Backend as Microservices.

◦ Major module: Remote players

◦ Major module: Standard user management, authentication, users across tournaments.

◦ Major module: Implementing a remote authentication. Gameplay and user experience

◦ Minor module: Multiple language supports.


◦ Major module: Add Another Game with User History and Matchmaking.
◦ Major module: Introduce an AI Opponent.
◦ Minor module: User and Game Stats Dashboards

◦ Minor module: Game Customization Options.

◦ Major module: Multiplayers (more than 2 in the same game)

◦ Minor module: Support on all devices.
◦ Minor module: Add accessibility for Visually Impaired Users.


## Notes
Atoms: Smallest components (e.g., buttons, text).
Molecules: Groups of atoms working together (e.g., a button group).
Organisms: Larger sections composed of molecules (e.g., header with navigation).
Templates: Page structure.
Pages: Complete views.

Frontend: Vue.js
    Purpose: Provides an interactive user interface for the game (Pong and Tic Tac Toe), authentication, user profile, settings, and other features.
    Components:
        Game Interface: Visual representation of the games (Pong, Tic Tac Toe).
        User Management: Login, signup, and profile management pages.
        Multiplayer Features: Real-time matchmaking and game customization.
        Stats and Dashboards: Displays user statistics and match history.
        Settings & Accessibility: Language support, customization options, and accessibility settings.
    Libraries/Tools:
        Vue Router for navigation.
        Vuex/Pinia for state management (e.g., user session, settings).
        Axios for API communication.

Backend: Django
    Purpose: Manages server-side logic, user authentication, game mechanics, and API endpoints.
    Modules:
        Authentication & User Management:
            Standard login/logout functionality.
            Remote authentication via OAuth or JWT.
            User profiles (with stats, match history, settings).
        Game Logic:
            Server-side mechanics for Pong and Tic Tac Toe.
            AI opponent logic for single-player mode.
            Multiplayer matchmaking (real-time game sessions).
        API:
            REST API (via Django REST Framework) for communication with the frontend.
            Endpoints for:
                Game state management (e.g., moves, scores).
                User actions (e.g., login, sign-up).
                Tournament and leaderboard data.
        Microservices Design:
            Modularized services:
                UserService for authentication and profiles.
                GameService for game logic and matchmaking.
                StatService for tracking user and game stats.
        Language & Accessibility Support:
            Integrated with Django translation tools for multiple languages.
            Accessibility features (e.g., screen reader compatibility).

Database: PostgreSQL
    Purpose: Stores user data, game states, statistics, and other persistent information.
    Schema Design:
        User Table:
            User credentials (hashed passwords, email).
            Profile settings (preferred language, avatar, etc.).
        Game History Table:
            Match ID, player IDs, winner/loser, score.
            Timestamp of matches.
        Game State Table:
            Current game state for active sessions.
            Used for resuming interrupted games.
        Statistics Table:
            User stats (wins, losses, ranking points).
            Global leaderboard data.
        Multiplayer Sessions Table:
            Stores active multiplayer game session details.

Communication Layer:
    API: REST API with Django REST Framework.
    WebSockets:
        Real-time communication for multiplayer games.
        Server-side implementation in Django Channels.

Additional Features:
    Matchmaking System:
        Real-time player pairing using a queue-based algorithm.
        Filters for skill level and preferences.
    Multiplayer Support:
        Ability to host games with more than two players.
    Device Support:
        Fully responsive design in the frontend.
        Support for various input methods (mouse, keyboard, touchscreen).
    Game Customization:
        Options like difficulty levels, themes, and gameplay speed.
    Accessibility:
        ARIA-compliant UI for visually impaired users.

Deployment & Hosting:
    Backend:
        Host Django on a platform like Heroku, AWS, or Google Cloud.
    Frontend:
        Deploy Vue.js on platforms like Netlify or Vercel.
    Database:
        Use managed PostgreSQL services (e.g., AWS RDS, Heroku Postgres).


## Directory listing

```
/project_root
├── /backend                # Django backend
│   ├── /users              # User authentication microservice
│   ├── /games              # Game logic (Pong, Tic Tac Toe, etc.)
│   ├── /stats              # Stats and history microservice
│   ├── Dockerfile          # Docker setup for backend
│   ├── requirements.txt    # Python dependencies
│   └── manage.py           # Django management
│
├── /frontend               # Vue.js frontend
│   ├── /src
│   │   ├── /components     # Vue components (Pong UI, stats, etc.)
│   │   ├── /views          # Pages (Home, Login, Game)
│   │   ├── App.vue         # Main Vue app
│   │   └── main.js         # Vue entry point
│   ├── package.json        # Frontend dependencies
│   └── Dockerfile          # Docker setup for frontend
│
├── /database               # PostgreSQL setup
│   ├── init.sql            # Initial database schema
│   ├── migrations          # Django migrations
│   └── Dockerfile          # Docker setup for database
│
├── /ai                     # AI logic
│   ├── /pong_ai            # AI scripts for Pong
│   ├── /tic_tac_toe_ai     # AI scripts for Tic Tac Toe
│   └── requirements.txt    # Python dependencies for AI
│
├── docker-compose.yml      # Docker Compose for full stack
└── README.md               # Documentation
```

## Roadmap
Week 1: Project Setup and Basics

    Georg:
        Set up Docker environment for local development and deployment.
        Create the Django project structure with microservices (e.g., user management, game logic).
        Implement user authentication (sign-up, login, remote authentication).

    Damien:
        Design the PostgreSQL database schema:
            Users, game history, matches, stats, etc.
        Set up database migrations in Django.
        Create APIs for basic game data retrieval and updates (e.g., user profiles).

    Celine:
        Set up the Vue.js project and basic UI components (e.g., login, dashboard).
        Integrate authentication flows with the backend (sign-up, login, logout).
        Design a basic frontend layout for Pong.

Week 2: Core Game Implementation

    Georg:
        Implement backend game history storage:
            Track wins, losses, and stats.
        Set up API endpoints for starting/joining matches.
        Develop the matchmaking system API (for 2 players initially).

    Damien:
        Implement the server-side logic for Pong, handling:
            Game state (real-time ball/paddle updates).
            Remote players (via WebSockets).

    Celine:
        Build the Pong UI with Vue.js:
            Paddle and ball movement.
            Integrate real-time data via WebSocket (basic 2-player mode).
        Build the Tic Tac Toe with Vue.js:
            Integrate real-time data via WebSocket (basic 2-player mode).

Week 3: Advanced Features

    Georg:
        Implement game customization options (e.g., paddle size, ball speed).
        Finalize microservices (deploy each separately in Docker containers).

    Damien:
        Implement the AI opponent for Pong:
            Simple algorithm (predictive ball movement).
        Enable storing match history with AI or human players.

    Celine:
        Add UI for matchmaking (join/create game).
        Build a user dashboard:
            Game stats, match history, and user profile.

Week 4: Final Features and Deployment

    Georg:
        (**Add support for multiplayer (4 players):
            Update backend game state logic for more paddles and interactions.
            Modify WebSocket broadcasts for additional players.**)

    Damien:
        Add support for a second game (Tic Tac Toe or similar):
            Backend logic, APIs, and history storage.
        Refine database queries and optimize performance.

    Celine:
        Finalize UI for the second game.
        Add support for multiple languages.
        AI Tic Tac Toe
        //Test and ensure responsive design for all devices.



## Questions
    Comment se fait l'interaction entre le front et le back
        Quelle format de message ?
        Lorsque le back donne des info pour afficher dynamiquement sur le front
        Lorsque le front envoit des choses qui doivent etre stocke sur la databese dans le back


### Github
https://github.com/C-est-quand-la-prochaine-reu-han
https://github.com/LaTeam-Trancendence/transcendence


```
/project_root
├── docker-compose.yml      # Orchestrates the backend, frontend, database, and AI services
├── README.md               # Documentation for the project setup and usage
```
```
/backend
├── Dockerfile               # Docker image definition for the backend
├── requirements.txt         # Python dependencies for Django (Django, DRF, etc.)
├── manage.py                # Django management script
├── /users                   # User authentication and management microservice
│   ├── __init__.py          # Python package initialization
│   ├── admin.py             # Django admin configuration for user models
│   ├── apps.py              # App configuration for the 'users' app
│   ├── models.py            # Defines the User model
│   ├── serializers.py       # Serializes user data (e.g., login, registration responses)
│   ├── views.py             # Handles login, registration, and user API endpoints
│   ├── urls.py              # Routes user-related endpoints (e.g., /api/users)
│   ├── tests.py             # Unit tests for user authentication
│   └── migrations           # Auto-generated database schema migrations for users
│       └── <auto_generated_migration_files>.py
├── /games                   # Game logic microservice (Pong and Tic Tac Toe)
│   ├── __init__.py          # Python package initialization
│   ├── admin.py             # Django admin configuration for game models
│   ├── apps.py              # App configuration for the 'games' app
│   ├── models.py            # Models for games (e.g., Game, Match)
│   ├── serializers.py       # Serializes game data for the frontend
│   ├── views.py             # API views for game logic (e.g., start/join a game)
│   ├── urls.py              # Routes game-related endpoints (e.g., /api/games)
│   ├── tests.py             # Unit tests for game logic and API endpoints
│   ├── websockets.py        # Real-time game updates using Django Channels
│   └── migrations           # Auto-generated database schema migrations for games
│       └── <auto_generated_migration_files>.py
├── /stats                   # Stats and history microservice
│   ├── __init__.py          # Python package initialization
│   ├── admin.py             # Django admin configuration for stats models
│   ├── apps.py              # App configuration for the 'stats' app
│   ├── models.py            # Models for stats (e.g., MatchHistory, Leaderboard)
│   ├── serializers.py       # Serializes stats data for frontend dashboards
│   ├── views.py             # API views for fetching stats and match history
│   ├── urls.py              # Routes stats-related endpoints (e.g., /api/stats)
│   ├── tests.py             # Unit tests for stats endpoints
│   └── migrations           # Auto-generated database schema migrations for stats
│       └── <auto_generated_migration_files>.py
```

```
/frontend
├── Dockerfile               # Docker image definition for the frontend
├── package.json             # Node.js dependencies for Vue.js
├── /src                     # Source code for Vue.js app
│   ├── App.vue              # Main Vue app layout and structure
│   ├── main.js              # Vue entry point, initializes app and routing
│   ├── /assets              # Static assets (images, fonts, etc.)
│   │   └── logo.png         # Example static asset
│   ├── /components          # Reusable Vue components
│   │   ├── PongGame.vue     # Vue component for Pong game UI
│   │   ├── UserStats.vue    # Vue component for displaying user stats
│   │   ├── Matchmaking.vue  # Vue component for matchmaking
│   │   └── Header.vue       # Navbar/header component
│   ├── /views               # Top-level pages
│   │   ├── Home.vue         # Home page with game options and stats
│   │   ├── Login.vue        # Login and registration page
│   │   └── Game.vue         # Game interface for Pong/Tic Tac Toe
│   ├── /store               # Vuex store for state management
│   │   └── index.js         # Vuex store configuration (e.g., user, game states)
│   └── /router              # Vue Router for navigation
│       └── index.js         # Routing configuration for frontend views
```

```
/database
├── Dockerfile               # Docker image definition for PostgreSQL
├── init.sql                 # Initial SQL script for setting up the database schema
├── /migrations              # Auto-generated database schema migrations
│   └── <auto_generated_migration_files>.py
```

```
/ai
├── Dockerfile               # Docker image definition for AI microservice
├── requirements.txt         # Python dependencies for AI (e.g., numpy)
├── /pong_ai                 # AI logic for Pong
│   ├── ai_logic.py          # Core logic for Pong AI (e.g., ball prediction)
│   ├── tests.py             # Unit tests for Pong AI logic
│   └── __init__.py          # Python package initialization
├── /tic_tac_toe_ai          # AI logic for Tic Tac Toe
│   ├── ai_logic.py          # Minimax algorithm or other logic for Tic Tac Toe AI
│   ├── tests.py             # Unit tests for Tic Tac Toe AI
│   └── __init__.py          # Python package initialization
```


## Launch

clone the repo

cd in the repo, cd front-end

```
npm install
npm run dev
```

You may have to install nodejs