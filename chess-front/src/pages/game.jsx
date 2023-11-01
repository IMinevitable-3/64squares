import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { WEB_SOCKET, WEB_SOCKET_PORT } from "../utils/config";

export function Game(){
    const { id } = useParams();
    useEffect(()=>{
        console.log("id" + id) ;
        const socket = new WebSocket(
            `ws://${WEB_SOCKET}:${WEB_SOCKET_PORT}/ws/play/${id}/`
          );
        socket.onopen = () => {
        console.log("WebSocket connection opened");
        };
    },[])

  return (
    <div>
      <h2>Play Component</h2>
      <p>Selected ID: {id}</p>
    </div>
  );
}