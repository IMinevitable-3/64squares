import Chessboard from "chessboardjsx";
import { useEffect, useContext, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { WEB_SOCKET, WEB_SOCKET_PORT } from "../utils/config";
import { Load } from "./loading";
import generateRandomString from '../utils/groupGenerator'
const Index = () => {
  const [Work, setWork] = useState("idle");
  const navigate = useNavigate();
  let from = location.state?.from?.pathname || "/play/";
  const handleConnection = () => { 
    const socket = new WebSocket(
      `ws://${WEB_SOCKET}:${WEB_SOCKET_PORT}/ws/lobby/`
    );

    setWork("connecting");
    socket.onopen = () => {
      console.log("WebSocket connection opened");
    };

    socket.onmessage = (event) => {
      console.log("Message from server:", event.data);
      console.log("game begins in 3.2..") ;
      from = from  + event.data + '/' 
      navigate(from, { replace: true });

    };

    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };
  };
  const handleCreate = () =>{
    const GAME = generateRandomString(5) 
    from = from +'created/'+ GAME +'/' ;
    navigate(from , {replace:true}) ;
  }
  return (
    <>
      {Work === "connecting" ? (
        <Load></Load>
      ) : Work === "idle" ? (
        <>
          <Chessboard position="start" />
          <button onClick={handleConnection}>Play</button>
          <br />
          <button onClick={handleCreate}>Create Game</button>

        </>
      ) : null}
    </>
  );
};
export default Index;
