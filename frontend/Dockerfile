# # Use official Node.js runtime as base image
# FROM node:20-alpine

# # Set working directory
# WORKDIR /app

# # Copy package files
# COPY frontend/package*.json ./

# # Install dependencies
# RUN npm ci --only=production

# # Copy application code
# COPY frontend/ .

# # Build the Next.js application
# RUN npm run build

# # Expose port
# EXPOSE 3000

# # Start the application
# CMD ["npm", "start"]



# Use official Node.js runtime as base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install --omit=dev

# Copy application code
COPY frontend/ .

# Build the Next.js application
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]