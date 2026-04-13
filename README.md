

# ADNU League Scoring & Database System

A comprehensive web-based scoring and management system for ADNU League events and competitions.

## Overview

The ADNU League Scoring & Database System provides a centralized platform for managing sports and cultural events, tracking team participation, recording match results, and maintaining real-time leaderboards. Built with Vue.js 3 and designed for ease of use by administrators and tabulations committee members.

## Key Features

### Authentication & Role-Based Access
- **Dual-role login system** with secure authentication
- **Admin** - Full access to all system features including team management, event configuration, and system settings
- **Tabulations Committee** - Focused access for score entry and match management with view-only access to teams and leaderboards

### Events Management
- Create and configure events/sports categories (Sports, Cultural, Academic, Laro ng Lahi)
- Flexible scoring systems (Point-based, Judged, Timed)
- Configurable matchup types (1v1 Head-to-Head or Free-for-All)
- Set-based tournament support with threshold incremental scoring

### Teams Management
- Register and manage participating teams/colleges
- Custom team colors for visual identification
- Sport participation tracking per team
- Real-time team statistics

### Matches & Scoring
- Create and schedule matches with venue information
- Live score tracking for ongoing matches
- Finalize match results with automatic winner determination
- Set-by-set scoring for tournament-style events
- Match history with detailed results

### Leaderboard
- Auto-updated standings based on match results
- Podium display for top 3 teams
- Visual team color indicators
- Win/loss tracking across all events

### Match History
- Complete archive of all matches (ongoing and completed)
- Filter by status (All, Ongoing, Completed)
- Search functionality by event or team
- Detailed match results with winner highlights

### Customization
- Dynamic system title (admin-configurable)
- Responsive design for desktop and mobile
- Clean, modern UI with animated elements

## Tech Stack

- **Frontend:** Vue.js 3 (Composition API)
- **Routing:** Vue Router 4
- **Styling:** Custom CSS with CSS variables
- **Icons:** Font Awesome
- **Build Tool:** Vite

## Project Structure

```
src/
├── components/
│   ├── common/       # Reusable UI components
│   ├── layout/       # Layout components (Sidebar)
│   └── modals/       # Modal dialogs
├── composables/      # Composable functions (useAuth, useStore)
├── router/           # Route configuration
├── views/
│   ├── auth/         # Login page
│   ├── dashboard/    # Dashboard view
│   ├── events/       # Events management
│   ├── teams/        # Teams management
│   ├── matches/      # Matches & scoring
│   ├── leaderboard/  # Standings display
│   └── history/      # Match history
└── App.vue           # Root component
```

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Usage

1. Navigate to the login page
2. Select your role (Admin or Tabulations Committee)
3. Enter credentials to access the system
4. Use the sidebar navigation to access different modules

## License

This project is proprietary software developed for ADNU League.
