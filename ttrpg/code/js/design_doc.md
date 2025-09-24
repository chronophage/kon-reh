## Fate's Edge Web Client Design Outline

### Core Architecture
```
Frontend (React/Vue.js) ←→ Backend API (Node.js/Express) ←→ Database (MongoDB/PostgreSQL)
```

### Database Schema

**Users**
```
- userId (UUID)
- username, email, passwordHash
- role (player/gm)
- createdAt, lastLogin
```

**Characters**
```
- characterId (UUID)
- userId (FK)
- name, archetype, xpTotal, xpSpent
- attributes: {body, wits, spirit, presence}
- skills: [{name, rating}]
- followers: [{name, cap, condition}]
- assets: [{name, tier, condition}]
- talents: [string]
- complications: [string]
- boons: int
- lastUpdated
```

**Campaigns**
```
- campaignId (UUID)
- gmId (FK)
- name, description
- players: [userId]
- status (active/inactive)
- createdAt
```

**Sessions**
```
- sessionId (UUID)
- campaignId (FK)
- date, notes
- attendance: [userId]
- xpAwards: [{userId, amount, reason}]
```

### Frontend Components

**Character Sheet Module**
```
Features:
- Real-time attribute/skill/talent editing
- Visual XP allocation with cost calculation
- Follower/Asset condition tracking (Maintained/Neglected/Compromised)
- Complication/Boon management
- Export/Import JSON
- Print-friendly layout
```

**Campaign Management**
```
Features:
- Player invitation/permission system
- Session scheduling and notes
- Campaign clock tracking (Mandate/Crisis)
- Asset/Follower shared database
- Character roster with status
```

**Dice Roller Interface**
```
Features:
- Attribute + Skill dropdown selectors
- Description ladder buttons (Basic/Detailed/Intricate)
- Visual dice pool display (d10s)
- Automatic success/complication counting
- Result interpretation with GM prompts
- Roll history with timestamps
```

### Backend API Endpoints

**Authentication**
```
POST /api/auth/register
POST /api/auth/login
GET /api/auth/verify
```

**Characters**
```
GET /api/characters/:userId
POST /api/characters
PUT /api/characters/:id
DELETE /api/characters/:id
POST /api/characters/:id/advance
```

**Campaigns**
```
GET /api/campaigns/:userId
POST /api/campaigns
PUT /api/campaigns/:id
POST /api/campaigns/:id/invite
POST /api/campaigns/:id/sessions
```

**Dice Rolling**
```
POST /api/roll
GET /api/roll/history/:characterId
POST /api/roll/complications
```

### Chat System with Macros

**Core Features**
```
- Real-time WebSocket communication
- Channel-based organization (General, OOC, Private)
- Whisper functionality (@username message)
- Roll macro integration (!roll 4d10)
- Character sheet data access (!sheet attribute skill)
- Asset activation shortcuts (!asset "Safehouse Network")
- Complication drawing (!draw 2)
```

**Macro Examples**
```
!roll Body + Melee
!roll Wits + Arcana channel
!weave Fire 3 "Flame Burst"
!asset "Spy Ring" 
!boon spend
!boon convert
!xp check
!follower assist Scout
!initiative Scout&Signal
```

### GM Tools Module

**Campaign Dashboard**
```
- Clock visualization (Mandate/Crisis/Primary/Rails)
- Player character summaries
- Session planning tools
- XP award distribution
- Complication deck drawing
- Asset/Follower condition tracking
```

**Real-time GM Controls**
```
- Complication point spending interface
- Clock ticking with visual feedback
- Player status monitoring (Fatigue, Harm, Exposure)
- Initiative action approval/denial
- Private messaging with individual players
- Scene framing tools
```

### Technical Stack Recommendations

**Frontend**: React with Redux/Zustand for state management
**Backend**: Node.js with Express.js
**Database**: PostgreSQL (better for relationships) or MongoDB (flexible schema)
**Real-time**: Socket.IO for chat and live updates
**Authentication**: JWT with refresh tokens
**Deployment**: Docker containers with nginx reverse proxy

### Key Features Implementation

**Dice Roller Logic**
```javascript
function rollDice(pool, descriptionLevel) {
  const dice = Array(pool).fill().map(() => Math.floor(Math.random() * 10) + 1);
  const successes = dice.filter(d => d >= 6).length;
  const complications = dice.filter(d => d === 1).length;
  
  // Apply description ladder benefits
  if (descriptionLevel === 'Detailed' && complications > 0) {
    // Re-roll one 1
  } else if (descriptionLevel === 'Intricate' && complications > 0) {
    // Re-roll all 1s
  }
  
  return { dice, successes, complications };
}
```

**Asset Activation System**
```javascript
function activateAsset(asset, boons, xp) {
  if (boons >= 1) {
    // Activate with Boon
    return { success: true, cost: { boons: -1 } };
  } else if (xp >= 2) {
    // Emergency activation with XP
    return { success: true, cost: { xp: -2 } };
  }
  return { success: false, error: "Insufficient resources" };
}
```

**Complication Management**
```javascript
function handleComplications(points, gmSpends) {
  const complications = [];
  for (let i = 0; i < points; i++) {
    complications.push(drawComplicationCard());
  }
  // Apply GM spends to complications
  return complications;
}
```

### Security Considerations
- Input validation on all endpoints
- Rate limiting for dice rolls/asset activations
- Role-based access control
- Secure WebSocket connections
- Data encryption for sensitive information
- Session timeout and re-authentication

### Mobile Responsiveness
- Responsive design for character sheets
- Touch-friendly dice roller interface
- Simplified chat interface for mobile
- Offline capability for character viewing

This design provides a comprehensive digital toolkit that enhances Fate's Edge gameplay while maintaining the collaborative, narrative-focused spirit of the system.

TEMP Roadmap:

You've got a **solid, detailed design document** for the Fate's Edge web client. It covers everything from architecture to security considerations. To help you move from design to implementation, here's a **step-by-step roadmap** and **key technical decisions** to guide your development.

---

## ✅ Step-by-Step Development Roadmap

### Phase 1: Project Setup & Authentication
1. **Initialize Project Structure**
   - Create separate folders for `frontend`, `backend`, and `shared`.
   - Initialize React frontend and Express backend with basic routing.
2. **Authentication System**
   - Implement JWT-based authentication.
   - Set up user registration/login endpoints.
   - Add middleware for token verification.
3. **Database Setup**
   - Choose PostgreSQL or MongoDB (see recommendations below).
   - Define schema/models for Users, Characters, Campaigns, Sessions.
   - Seed initial data if needed.

### Phase 2: Core Backend API
4. **Character CRUD API**
   - Build endpoints for creating, reading, updating, deleting characters.
   - Implement XP advancement logic.
5. **Campaign Management API**
   - Campaign creation, invitation system, session logging.
6. **Dice Roller Endpoint**
   - Implement `/api/roll` with logic for success/complications.
7. **Roll History & Complications**
   - Store roll history per character.
   - Add complication drawing endpoint.

### Phase 3: Frontend MVP
8. **Frontend Architecture**
   - Set up React app with state management (Zustand or Redux).
   - Create reusable components like modals, forms, and tables.
9. **Character Sheet Module**
   - Display/edit character data.
   - Implement XP allocation and talent tracking.
10. **Campaign Dashboard**
    - List campaigns, invite players, manage sessions.
11. **Dice Roller UI**
    - Interactive dice roller with visual feedback.
    - Macro support in input fields.

### Phase 4: Real-Time Features
12. **Chat System with Macros**
    - Integrate Socket.IO for real-time messaging.
    - Support channels, whispers, and macro parsing.
13. **GM Tools Module**
    - Clock visualization and initiative tracking.
    - Asset activation and complication drawing.

### Phase 5: Polish & Deployment
14. **Security Hardening**
    - Add rate limiting, input sanitization, secure headers.
15. **Mobile Responsiveness**
    - Use responsive design libraries (TailwindCSS, Bootstrap).
16. **Deployment**
    - Containerize with Docker.
    - Set up reverse proxy with Nginx.
    - Deploy to cloud provider (AWS, Vercel, Render, etc.).

---

## 🛠️ Technical Stack Recommendations

| Layer       | Choice                  | Reason                                                                 |
|-------------|-------------------------|------------------------------------------------------------------------|
| Frontend    | React + Zustand         | Fast rendering, predictable state management                          |
| Backend     | Node.js + Express       | Lightweight, great ecosystem                                          |
| Database    | PostgreSQL              | Better for relational data (users, campaigns, sessions)              |
| Real-time   | Socket.IO               | Mature solution for chat and live updates                             |
| Auth        | JWT + Refresh Tokens    | Secure, scalable authentication                                       |
| Deployment  | Docker + Nginx + AWS/Render | Portable, scalable deployment                                         |

---

## 🔐 Security Considerations Recap

- **Input Validation**: Use libraries like `express-validator`.
- **Rate Limiting**: Use `express-rate-limit` to prevent abuse.
- **Role-Based Access Control**: Middleware to check user roles (`player` vs `gm`).
- **Secure WebSockets**: Enforce authentication over Socket.IO connections.
- **Data Encryption**: Use bcrypt for passwords, encrypt sensitive fields at rest.
- **Session Timeout**: Implement idle timeout and re-authentication prompts.

---

## 📱 Mobile Responsiveness Strategy

- **Responsive Layouts**: Use CSS Grid/Flexbox or Tailwind.
- **Touch-Friendly UI**:
  - Larger buttons for dice rolling.
  - Swipe gestures for navigation.
- **Offline Capability**:
  - Use service workers or local storage for offline viewing.
- **Progressive Web App (PWA)**:
  - Enable installability and push notifications.

---

## 🧪 Testing Strategy

1. **Unit Tests**
   - Jest for backend logic (dice rolls, asset activation).
2. **Integration Tests**
   - Supertest for API endpoint testing.
3. **Frontend Tests**
   - React Testing Library for component behavior.
4. **End-to-End Tests**
   - Cypress or Playwright for full user flows.

---

## 📦 Folder Structure Suggestion

```
fates-edge-web/
├── backend/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── middleware/
│   ├── utils/
│   └── server.js
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/ (Zustand/Redux)
│   │   ├── services/ (API calls)
│   │   └── App.jsx
│   └── public/
├── shared/
│   └── types/ (shared interfaces between frontend/backend)
├── docker-compose.yml
└── README.md
```

---

## 🚀 Next Steps

If you're ready to start coding, here's what to do first:

1. **Set up your Git repo** (GitHub/GitLab).
2. **Initialize backend with Express + PostgreSQL**.
3. **Implement user registration/login**.
4. **Build the character CRUD API**.
5. **Start the frontend with a character sheet mockup**.
