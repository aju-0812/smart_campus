FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

# Expose Vite dev server to external requests
CMD ["npm", "run", "dev", "--", "--host"]
