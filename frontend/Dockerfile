FROM node:20-alpine

# Install libc6-compat for SWC compatibility on Alpine
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copy dependency files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy the rest of the code
COPY . .

# Use 'dev' instead of 'start' for Part 1 to allow hot-reloading
CMD ["npm", "run", "dev"]