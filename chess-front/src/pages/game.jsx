import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { WEB_SOCKET, WEB_SOCKET_PORT } from "../utils/config";
import Chessboard from "chessboardjsx";

export function Game(){
    const { id } = useParams();
    useEffect(()=>{
        const socket = new WebSocket(
            `ws://${WEB_SOCKET}:${WEB_SOCKET_PORT}/ws/play/${id}/`
          );
        socket.onopen = () => {
            console.log("WebSocket connection opened");
        };
    },[])

  return (
    <div>
      <Chessboard position="start"/>
    </div>
  );
}