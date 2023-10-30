import Chessboard from "chessboardjsx";
import { useEffect, useContext, useState } from "react";
import { WEB_SOCKET, WEB_SOCKET_PORT } from "../utils/config";
import '../assets/loading.css'
const Index = () => {
  const [Work, setWork] = useState("idle");

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
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };
  };
  return (
    <>
      {Work === "connecting" ? (
        <div className="lds-facebook"><div></div><div></div><div></div></div>
      ) : Work === "idle" ? (
        <>
          <Chessboard position="start" />
          <button onClick={handleConnection}>Play</button>
        </>
      ) : null}
    </>
  );
};
export default Index;
