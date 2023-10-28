FROM node:alpine AS base 
WORKDIR /usr/src/app 
COPY package*.json /usr/src/app/
RUN npm install 

FROM  base AS development 
COPY . .
EXPOSE 5173
CMD ["npm", "run" ,"dev"]

FROM base AS production
COPY . .
EXPOSE 5173
CMD ["npm" , "run" , "build"]
