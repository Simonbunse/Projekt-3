# Use the official Node.js image as a base image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your application code
COPY . .

# Build the Next.js application
RUN npm run build

# Expose the application port
EXPOSE 3001

# Start the Next.js application
CMD ["npm", "start"]
