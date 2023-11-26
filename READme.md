# Real time chess

## Installation
```
docker-compose build
```
#### After successful build 

```
docker-compose up
```
#### After server is started update  [ VITE_FKED  ](chess-front/.env)  with IP
```
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' backend
```

