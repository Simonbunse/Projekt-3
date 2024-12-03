# Step 1: Use official Node.js image as the base image
FROM node:18 AS base

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy package.json and package-lock.json to the container
COPY package.json package-lock.json ./

# Step 4: Install dependencies
RUN npm install

# Step 5: Copy the rest of the application files
COPY . .

# Step 6: Build the Next.js application
RUN npm run build

# Step 7: Expose the ports for Next.js and the MQTT server
EXPOSE 3000 1883

# Step 8: Start both services (Next.js app and MQTT server)
CMD npm run start & npm run mqtt
