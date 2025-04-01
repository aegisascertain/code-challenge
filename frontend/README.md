# Frontend for Ascertain Code Challenge

This is the frontend application for the Ascertain Code Challenge, built with React, TypeScript, and Vite.

## Technology Stack

- React 19 with TypeScript
- Vite for building and development
- Mantine UI for component library
- TanStack React Query for data fetching
- React Router for navigation
- Tailwind CSS for styling
- Vitest and Testing Library for testing
- Storybook for component documentation

## Development

### Prerequisites

- Node.js (v20+)
- pnpm (v9+)

### Getting Started

1. Install dependencies:
   ```bash
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

### Available Scripts

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

## Docker Deployment

The frontend can be run in a Docker container. See the root `docker-compose.yml` for configuration details.
