FROM node:alpine AS base 
WORKDIR /app 
COPY package*.json .
RUN npm install 

FROM  base AS development 
COPY . .
EXPOSE 5173
CMD ["sh", "-c", "npm run dev"]
FROM base AS production
COPY . .
EXPOSE 5173
CMD ["npm" , "run" , "build"]
