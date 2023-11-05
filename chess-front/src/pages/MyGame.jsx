import React, { useState, useEffect, useRef } from "react";
import Chessboard from "chessboardjsx";
import {Chess} from "chess.js";
import { useParams } from 'react-router-dom';
import { WEB_SOCKET, WEB_SOCKET_PORT } from "../utils/config";
function MyGame(){
    const { id } = useParams();
    useEffect(()=>{
        console.log(id) 
        const socket = new WebSocket(
            `ws://${WEB_SOCKET}:${WEB_SOCKET_PORT}/ws/my/play/${id}/`
          );
        socket.onopen = () => {
            console.log("WebSocket connection opened");//returns color 
        };

        socket.onmessage = (event) => {
            console.log(event.data);
      
          };
      
          socket.onclose = () => {
            console.log("WebSocket connection closed");
          };
    },[])
    return (
        <>
            <Chessboard position="start"/>
        </>
    )
}
export default MyGame;