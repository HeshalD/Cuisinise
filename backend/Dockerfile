# Use Node 20 LTS Alpine
FROM node:20-alpine

# Create app directory
WORKDIR /app

# Install dependencies only from package files
COPY package*.json ./

# If you have dev dependencies needed for build, keep NODE_ENV=development here and set production later
RUN npm ci --omit=dev

# Copy app source
COPY . .

# Set NODE_ENV to production in container runtime
ENV NODE_ENV=production

# Expose the port your app listens on (adjust if not 3000)
EXPOSE 5000

# Healthcheck (optional: replace /health with your endpoint)
# HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 CMD wget -qO- http://localhost:3000/health || exit 1

# Start
CMD ["node", "app.js"]