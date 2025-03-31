# Ascertain Code Challenge

A modern web application built for an interview code challenge using React, TypeScript, and a suite of quality tools.

## Technology Stack

- **Frontend**: React 19 with TypeScript
- **Build Tool**: Vite for fast development and building
- **UI Components**: Mantine UI
- **Data Fetching**: React Query
- **Routing**: React Router
- **Testing**: Vitest, Testing Library, and Storybook
- **Styling**: Tailwind CSS with Mantine integration
- **Code Quality**: ESLint, TypeScript, and Prettier
- **Deployment**: Docker containerization

## Getting Started

### Prerequisites

- Node.js (v20+)
- pnpm (v9+)
- Docker and Docker Compose (for containerized deployment)

### Installation

1. Install dependencies:
   ```bash
   cd frontend
   pnpm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

3. Start the development server:
   ```bash
   pnpm dev
   ```

## Available Scripts

- `pnpm dev` - Start the development server
- `pnpm build` - Build for production
- `pnpm preview` - Preview the production build
- `pnpm test` - Run tests
- `pnpm test:watch` - Run tests in watch mode
- `pnpm test:coverage` - Run tests with coverage
- `pnpm lint` - Run ESLint
- `pnpm format` - Format code with Prettier
- `pnpm storybook` - Start Storybook for component development
- `pnpm build-storybook` - Build Storybook for deployment

## Deployment

### Docker Deployment

1. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

2. Access the application at: `http://localhost:3000`

## Testing Strategy

- Component tests with React Testing Library
- Unit tests with Vitest
- Component documentation and visual testing with Storybook 