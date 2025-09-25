# Fate's Edge RPG Web Application

## Overview

Fate's Edge is a comprehensive web-based role-playing game management system designed for the Fate's Edge tabletop RPG system. This application provides tools for players and Game Masters (GMs) to manage campaigns, characters, dice rolls, and real-time communication.

## Features

### Core Features
- **User Authentication**: Secure JWT-based authentication with Google OAuth support
- **Campaign Management**: Create and manage campaigns with player rosters
- **Character Management**: Full CRUD operations for player characters
- **Dice Roller**: Fate's Edge dice mechanics with description ladder system
- **Real-time Chat**: WebSocket-based chat with channel support and typing indicators
- **Macro System**: Extensible macro system for game automation
- **Themeable Interface**: Multiple color themes with custom theme support

### Technical Features
- **Security Hardened**: Comprehensive security measures including input validation, CSRF protection, and rate limiting
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Socket.IO integration for instant updates
- **Persistent Storage**: Local storage for themes and authentication tokens

## Technology Stack

### Frontend
- **React** with **Zustand** for state management
- **Tailwind CSS** for styling
- **Socket.IO Client** for real-time communication
- **Axios** for HTTP requests

### Backend
- **Node.js** with **Express.js**
- **PostgreSQL** for data storage
- **Socket.IO** for real-time communication
- **JWT** for authentication
- **Google OAuth** for social authentication

### Deployment
- **Docker** containerization
- **Docker Compose** for multi-container orchestration

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- Docker and Docker Compose
- PostgreSQL (if running without Docker)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd fates-edge
```

2. **Set up environment variables:**
```bash
# Backend .env
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration

# Frontend .env
cp frontend/.env.example frontend/.env
# Edit frontend/.env with your configuration
```

3. **Start with Docker (recommended):**
```bash
docker-compose up --build
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:3001

### Manual Installation

**Backend:**
```bash
cd backend
npm install
npm run dev
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
fates-edge/
├── backend/
│   ├── config/          # Database configuration
│   ├── middleware/      # Security and validation middleware
│   ├── routes/          # API route handlers
│   ├── services/        # Business logic services
│   ├── server.js        # Main server entry point
│   └── .env             # Environment variables
├── frontend/
│   ├── public/          # Static assets
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API and Socket.IO services
│   │   ├── store/       # Zustand stores
│   │   ├── utils/       # Helper functions
│   │   ├── App.jsx      # Main application component
│   │   └── index.js     # Entry point
│   └── .env             # Environment variables
├── docker/              # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
└── README.md            # This file
```

---

# Fate's Edge API Reference

## Authentication

### Register User
**POST** `/api/auth/register`
```json
{
  "username": "player1",
  "email": "player1@example.com",
  "password": "SecurePass123"
}
```
**Response:**
```json
{
  "token": "jwt.token.here",
  "user": {
    "userid": "uuid",
    "username": "player1",
    "email": "player1@example.com",
    "role": "player"
  }
}
```

### Login User
**POST** `/api/auth/login`
```json
{
  "email": "player1@example.com",
  "password": "SecurePass123"
}
```
**Response:**
```json
{
  "token": "jwt.token.here",
  "user": {
    "userid": "uuid",
    "username": "player1",
    "email": "player1@example.com",
    "role": "player"
  }
}
```

### Google Login
**POST** `/api/auth/google`
```json
{
  "idToken": "google.id.token"
}
```
**Response:**
```json
{
  "token": "jwt.token.here",
  "user": {
    "userid": "uuid",
    "username": "player1",
    "email": "player1@example.com",
    "role": "player",
    "avatar": "https://..."
  }
}
```

### Verify Token
**GET** `/api/auth/verify`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
{
  "valid": true,
  "user": {
    "userid": "uuid",
    "username": "player1",
    "email": "player1@example.com"
  }
}
```

## Characters

### Get User Characters
**GET** `/api/characters/user/:userId`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
[
  {
    "characterid": "uuid",
    "userid": "uuid",
    "name": "Character Name",
    "description": "Character description",
    "species": "Human",
    "background": "Noble",
    "archetype": "Warrior",
    "experience": 15,
    "createdat": "2023-01-01T00:00:00Z",
    "updatedat": "2023-01-01T00:00:00Z"
  }
]
```

### Get Character by ID
**GET** `/api/characters/:id`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
{
  "characterid": "uuid",
  "userid": "uuid",
  "name": "Character Name",
  "description": "Character description",
  "species": "Human",
  "background": "Noble",
  "archetype": "Warrior",
  "experience": 15,
  "createdat": "2023-01-01T00:00:00Z",
  "updatedat": "2023-01-01T00:00:00Z"
}
```

### Create Character
**POST** `/api/characters`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "userid": "uuid",
  "name": "Character Name",
  "description": "Character description",
  "species": "Human",
  "background": "Noble",
  "archetype": "Warrior"
}
```
**Response:**
```json
{
  "characterid": "uuid",
  "userid": "uuid",
  "name": "Character Name",
  "description": "Character description",
  "species": "Human",
  "background": "Noble",
  "archetype": "Warrior",
  "experience": 0,
  "createdat": "2023-01-01T00:00:00Z",
  "updatedat": "2023-01-01T00:00:00Z"
}
```

### Update Character
**PUT** `/api/characters/:id`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "name": "Updated Name",
  "description": "Updated description"
}
```
**Response:**
```json
{
  "characterid": "uuid",
  "userid": "uuid",
  "name": "Updated Name",
  "description": "Updated description",
  "species": "Human",
  "background": "Noble",
  "archetype": "Warrior",
  "experience": 0,
  "createdat": "2023-01-01T00:00:00Z",
  "updatedat": "2023-01-01T00:00:00Z"
}
```

### Delete Character
**DELETE** `/api/characters/:id`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
{
  "message": "Character deleted successfully"
}
```

### Advance Character (Spend XP)
**POST** `/api/characters/:id/advance`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "xpSpent": 5
}
```
**Response:**
```json
{
  "character": {
    "characterid": "uuid",
    "userid": "uuid",
    "name": "Character Name",
    "experience": 10,
    "createdat": "2023-01-01T00:00:00Z",
    "updatedat": "2023-01-01T00:00:00Z"
  }
}
```

## Campaigns

### Get User Campaigns
**GET** `/api/campaigns/user/:userId`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
[
  {
    "campaignid": "uuid",
    "gmuserid": "uuid",
    "name": "Campaign Name",
    "description": "Campaign description",
    "setting": "Fantasy",
    "createdat": "2023-01-01T00:00:00Z",
    "updatedat": "2023-01-01T00:00:00Z"
  }
]
```

### Get Campaign by ID
**GET** `/api/campaigns/:id`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
{
  "campaignid": "uuid",
  "gmuserid": "uuid",
  "name": "Campaign Name",
  "description": "Campaign description",
  "setting": "Fantasy",
  "createdat": "2023-01-01T00:00:00Z",
  "updatedat": "2023-01-01T00:00:00Z",
  "players": [...],
  "sessions": [...],
  "clocks": [...]
}
```

### Create Campaign
**POST** `/api/campaigns`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "name": "New Campaign",
  "description": "Campaign description",
  "setting": "Cyberpunk"
}
```
**Response:**
```json
{
  "campaignid": "uuid",
  "gmuserid": "uuid",
  "name": "New Campaign",
  "description": "Campaign description",
  "setting": "Cyberpunk",
  "createdat": "2023-01-01T00:00:00Z",
  "updatedat": "2023-01-01T00:00:00Z"
}
```

### Update Campaign
**PUT** `/api/campaigns/:id`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "name": "Updated Campaign Name",
  "description": "Updated description"
}
```
**Response:**
```json
{
  "campaignid": "uuid",
  "gmuserid": "uuid",
  "name": "Updated Campaign Name",
  "description": "Updated description",
  "setting": "Cyberpunk",
  "createdat": "2023-01-01T00:00:00Z",
  "updatedat": "2023-01-01T00:00:00Z"
}
```

### Delete Campaign
**DELETE** `/api/campaigns/:id`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
{
  "message": "Campaign deleted successfully"
}
```

### Invite Player to Campaign
**POST** `/api/campaigns/:id/invite`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "email": "player2@example.com"
}
```
**Response:**
```json
{
  "campaign": {
    "campaignid": "uuid",
    "players": [...]
  }
}
```

### Remove Player from Campaign
**POST** `/api/campaigns/:id/remove`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "userId": "player-uuid"
}
```
**Response:**
```json
{
  "campaign": {
    "campaignid": "uuid",
    "players": [...]
  }
}
```

### Create Campaign Session
**POST** `/api/campaigns/:id/sessions`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "title": "Session 1",
  "description": "First session description",
  "date": "2023-01-15T19:00:00Z"
}
```
**Response:**
```json
{
  "sessionid": "uuid",
  "campaignid": "uuid",
  "title": "Session 1",
  "description": "First session description",
  "date": "2023-01-15T19:00:00Z",
  "createdat": "2023-01-01T00:00:00Z"
}
```

## Dice Rolling

### Roll Dice
**POST** `/api/roll`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "pool": 5,
  "descriptionLevel": "detailed",
  "characterId": "optional-character-uuid",
  "notes": "Attack roll"
}
```
**Response:**
```json
{
  "rollid": "uuid",
  "userid": "uuid",
  "characterid": "optional-character-uuid",
  "pool": 5,
  "dice": [3, 7, 1, 8, 6],
  "successes": 3,
  "complications": 1,
  "descriptionlevel": "detailed",
  "notes": "Attack roll",
  "createdat": "2023-01-01T00:00:00Z"
}
```

### Get Roll History
**GET** `/api/roll/history/:characterId`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
[
  {
    "rollid": "uuid",
    "userid": "uuid",
    "characterid": "character-uuid",
    "pool": 5,
    "dice": [3, 7, 1, 8, 6],
    "successes": 3,
    "complications": 1,
    "descriptionlevel": "detailed",
    "notes": "Attack roll",
    "createdat": "2023-01-01T00:00:00Z"
  }
]
```

### Draw Complications
**POST** `/api/roll/complications`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "points": 3,
  "gmSpends": [
    {
      "type": "narrative",
      "description": "Unexpected enemy appears"
    }
  ]
}
```
**Response:**
```json
{
  "complications": [
    {
      "type": "injury",
      "severity": "minor",
      "description": "Sprained ankle"
    }
  ],
  "totalPoints": 3
}
```

## Chat

### Get Campaign Messages
**GET** `/api/chat/messages/:campaignId`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
[
  {
    "messageid": "uuid",
    "campaignid": "uuid",
    "userid": "uuid",
    "characterid": "optional-character-uuid",
    "content": "Hello everyone!",
    "channel": "general",
    "createdat": "2023-01-01T00:00:00Z"
  }
]
```

### Get Channel Messages
**GET** `/api/chat/messages/:campaignId/:channel`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
[
  {
    "messageid": "uuid",
    "campaignid": "uuid",
    "userid": "uuid",
    "characterid": "optional-character-uuid",
    "content": "OOC discussion here",
    "channel": "ooc",
    "createdat": "2023-01-01T00:00:00Z"
  }
]
```

### Send Message
**POST** `/api/chat/messages`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "campaignId": "uuid",
  "content": "Hello campaign!",
  "channel": "general",
  "characterId": "optional-character-uuid"
}
```
**Response:**
```json
{
  "messageid": "uuid",
  "campaignid": "uuid",
  "userid": "uuid",
  "characterid": "optional-character-uuid",
  "content": "Hello campaign!",
  "channel": "general",
  "createdat": "2023-01-01T00:00:00Z"
}
```

## Macros

### Get Campaign Macros
**GET** `/api/macros/campaign/:campaignId`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
[
  {
    "macroid": "uuid",
    "campaignid": "uuid",
    "name": "Roll Dice",
    "command": "roll",
    "description": "Roll a pool of dice",
    "createdby": "uuid",
    "ispublic": true,
    "isapproved": true,
    "createdat": "2023-01-01T00:00:00Z",
    "updatedat": "2023-01-01T00:00:00Z"
  }
]
```

### Create Macro
**POST** `/api/macros`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "campaignId": "uuid",
  "name": "Custom Roll",
  "command": "custom",
  "description": "Custom dice roll",
  "isPublic": true
}
```
**Response:**
```json
{
  "macroid": "uuid",
  "campaignid": "uuid",
  "name": "Custom Roll",
  "command": "custom",
  "description": "Custom dice roll",
  "createdby": "uuid",
  "ispublic": true,
  "isapproved": false,
  "createdat": "2023-01-01T00:00:00Z",
  "updatedat": "2023-01-01T00:00:00Z"
}
```

### Update Macro
**PUT** `/api/macros/:id`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "name": "Updated Macro",
  "description": "Updated description"
}
```
**Response:**
```json
{
  "macroid": "uuid",
  "campaignid": "uuid",
  "name": "Updated Macro",
  "command": "custom",
  "description": "Updated description",
  "createdby": "uuid",
  "ispublic": true,
  "isapproved": false,
  "createdat": "2023-01-01T00:00:00Z",
  "updatedat": "2023-01-01T00:00:00Z"
}
```

### Delete Macro
**DELETE** `/api/macros/:id`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
{
  "message": "Macro deleted successfully"
}
```

### Execute Macro
**POST** `/api/macros/execute`
**Headers:** `Authorization: Bearer <token>`
```json
{
  "campaignId": "uuid",
  "macroCommand": "roll 5 detailed Attack roll",
  "characterId": "optional-character-uuid"
}
```
**Response:**
```json
{
  "message": "Macro executed successfully",
  "result": {
    "type": "roll",
    "result": {
      "dice": [3, 7, 1, 8, 6],
      "successes": 3,
      "complications": 1,
      "pool": 5,
      "descriptionLevel": "detailed"
    }
  }
}
```

## Socket.IO Events

### Client to Server

#### Join Campaign
```javascript
socket.emit('join_campaign', campaignId);
```

#### Leave Campaign
```javascript
socket.emit('leave_campaign', campaignId);
```

#### Send Message
```javascript
socket.emit('send_message', {
  campaignId: 'uuid',
  content: 'Hello!',
  channel: 'general',
  characterId: 'optional-uuid'
});
```

#### Roll Dice
```javascript
socket.emit('roll_dice', {
  campaignId: 'uuid',
  pool: 5,
  descriptionLevel: 'detailed',
  characterId: 'optional-uuid',
  notes: 'Attack roll'
});
```

#### Execute Macro
```javascript
socket.emit('execute_macro', {
  campaignId: 'uuid',
  macroCommand: 'roll 5 detailed Attack roll',
  characterId: 'optional-uuid'
});
```

#### Typing Indicator
```javascript
socket.emit('typing', {
  campaignId: 'uuid',
  isTyping: true
});
```

### Server to Client

#### New Message
```javascript
socket.on('new_message', (message) => {
  // Handle new chat message
});
```

#### Dice Rolled
```javascript
socket.on('dice_rolled', (rollResult) => {
  // Handle dice roll result
});
```

#### Macro Executed
```javascript
socket.on('macro_executed', (macroResult) => {
  // Handle macro execution result
});
```

#### User Typing
```javascript
socket.on('user_typing', (data) => {
  // Handle typing indicator
  // data: { userId, isTyping, timestamp }
});
```

#### User Joined
```javascript
socket.on('user_joined', (data) => {
  // Handle user join notification
  // data: { userId, timestamp }
});
```

#### Error
```javascript
socket.on('error', (error) => {
  // Handle socket error
  // error: { message }
});
```

## Macro Commands Reference

### Dice Rolling Macros
- `/roll <pool> [descriptionLevel] [notes]` - Roll dice with optional description level
- `/r <pool> [descriptionLevel] [notes]` - Short form of roll command

**Examples:**
```
/roll 5
/roll 7 detailed Complex attack
/r 3 intricate Sneak attack
```

### Character Macros
- `/xp <+|->amount [reason]` - Gain or spend experience points
- `/boon convert [details]` - Convert a boon
- `/boon spend [details]` - Spend a boon

**Examples:**
```
/xp +3 Defeated the dragon
/xp -5 New skill purchase
/boon convert Gained narrative advantage
/boon spend Avoid complication
```

### Campaign Macros
- `/clock tick <name> [amount]` - Tick a campaign clock
- `/clock reset <name>` - Reset a campaign clock
- `/session start [details]` - Start a new session
- `/session end [details]` - End current session

**Examples:**
```
/clock tick investigation 2
/clock reset conspiracy
/session start Investigating the haunted mansion
/session end Great session everyone!
```

### Communication Macros
- `/whisper <@target> <message>` - Send private message
- `/w <@target> <message>` - Short form of whisper
- `/me <action>` - Emote action

**Examples:**
```
/whisper @gm Need help with something
/w @player Secret info here
/me looks around nervously
```

## Error Handling

All API endpoints return appropriate HTTP status codes:
- **200**: Success
- **201**: Created
- **400**: Bad Request (validation errors)
- **401**: Unauthorized (authentication required)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found
- **429**: Too Many Requests (rate limited)
- **500**: Internal Server Error

Error responses follow this format:
```json
{
  "message": "Error description"
}
```

Validation errors include additional details:
```json
{
  "message": "Validation failed",
  "errors": [
    {
      "param": "email",
      "msg": "Please provide a valid email"
    }
  ]
}
```

## Security Features

### Authentication
- JWT tokens with 24-hour expiration
- Password hashing with bcrypt (12 rounds)
- Google OAuth integration
- Refresh token support

### Input Validation
- Comprehensive input sanitization
- SQL injection prevention
- XSS protection
- CSRF protection

### Rate Limiting
- General API: 100 requests/15 minutes
- Authentication: 5 requests/15 minutes
- Dice rolls: 20 requests/minute

### Security Headers
- Content Security Policy
- XSS Protection
- Frame Options
- Content Type Options
- Strict Transport Security

## Deployment

### Docker Deployment
```bash
# Build and start all services
docker-compose up --build -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f
```

### Environment Variables

**Backend (.env):**
```env
PORT=3001
DATABASE_URL=postgresql://user:pass@localhost:5432/fatesedge
JWT_SECRET=your-super-secret-jwt-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FRONTEND_URL=http://localhost:3000
NODE_ENV=production
```

**Frontend (.env):**
```env
REACT_APP_API_URL=http://localhost:3001/api
REACT_APP_SOCKET_URL=http://localhost:3001
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
```

### Database Schema

The application uses PostgreSQL with the following key tables:
- `users` - User accounts and authentication
- `campaigns` - Campaign information
- `characters` - Player characters
- `campaign_players` - Campaign membership
- `sessions` - Campaign sessions
- `messages` - Chat messages
- `macros` - User-defined macros
- `rolls` - Dice roll history
- `complications` - Complication tracking

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the GitHub repository or contact the development team.
