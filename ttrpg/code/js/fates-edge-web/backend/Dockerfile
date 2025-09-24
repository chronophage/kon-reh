FROM node:18-alpine

WORKDIR /app

# Install python and build tools for native modules on M1
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose ports
EXPOSE 3001

# Start development server
CMD ["npm", "run", "dev"]

