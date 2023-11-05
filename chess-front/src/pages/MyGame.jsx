import React, { useState, useEffect, useRef } from "react";
import Chessboard from "chessboardjsx";
import { Chess } from "chess.js";
import { useParams } from 'react-router-dom';
import { WEB_SOCKET, WEB_SOCKET_PORT } from "../utils/config";
import { Load } from "./loading";

function MyGame() {
  const gameRef = useRef(new Chess());
  const { id } = useParams();
  const [fen, setFen] = useState("start");
  const [playerColor, setPlayerColor] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);

  const socketRef = useRef(null);

  useEffect(() => {
    // Open WebSocket connection only once
    if (!socketRef.current) {
      socketRef.current = new WebSocket(`ws://${WEB_SOCKET}:${WEB_SOCKET_PORT}/ws/my/play/${id}/`);

      socketRef.current.onopen = () => {
        console.log("WebSocket connected");
      };

      socketRef.current.onmessage = (event) => {
        try{
            const data = JSON.parse(event.data);
            if (data.type === "color") {
              setPlayerColor(data.payload.color === 0 ? "white" : "black");
            } else if (data.type === "start") {
              setFen("start");
              setGameStarted(true);
            } else if (data.type === "gameOver") {
              const { result, winner } = data.payload;
    
              if (result === "checkmate") {
                alert(`Checkmate! ${winner} wins.`);
              } else if (result === "stalemate") {
                alert("Stalemate! The game is a draw.");
              }
            } else if (data.type === "move") {
                const { sourceSquare, targetSquare } = data.payload;
                console.log(sourceSquare , targetSquare) ;
                updateGame(sourceSquare, targetSquare);
            }

        }catch (error) {
            console.error(error);
          }

      };
    }

    return () => {
      // Close WebSocket connection when component unmounts
      if (socketRef.current) {
        console.log("WebSocket disconnected");
        socketRef.current.close();
      }
    };
  }, [id]);

  const updateGame = (sourceSquare, targetSquare) => {
    const newGame = new Chess(gameRef.current.fen());
    const move = newGame.move({
      from: sourceSquare,
      to: targetSquare,
    //   promotion: "q",
    });
  
    gameRef.current = newGame;
  
    setFen(newGame.fen());
  
    if (move !== null && gameRef.current.isCheckmate()) {
      socketRef.current.send(JSON.stringify({ type: "gameOver", payload: { winner: playerColor === "white" ? "black" : "white" } }));
    }
  };
  

  const handleMove = ({ sourceSquare, targetSquare }) => {
    console.log("Current turn:", gameRef.current.turn());
    if (gameRef.current.turn() !== playerColor[0]) {
      return;
    }

    const legalMoves = gameRef.current.moves({ square: sourceSquare, verbose: true });
    const isLegalMove = legalMoves.some(move => move.to === targetSquare);

    if (!isLegalMove) {
    //   alert("Illegal move! Please make a different move.");
      return;
    }

    gameRef.current.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: "q",
    });

    setFen((prevFen) => {
      return gameRef.current.fen();
    });

    socketRef.current.send(JSON.stringify({ type: "move", payload: { sourceSquare, targetSquare } }));

    if (gameRef.current.isCheckmate()) {
      socketRef.current.send(JSON.stringify({ type: "gameOver", payload: { result: "checkmate", winner: playerColor } }));
      alert(`Checkmate! ${playerColor} wins.`);
    } else if (gameRef.current.isStalemate()) {
      socketRef.current.send(JSON.stringify({ type: "gameOver", payload: { result: "stalemate" } }));
      alert(`Stalemate! The game is a draw.`);
    }
  };

  return (
    <div>
      {gameStarted && playerColor ? (
        <div>
          <div>
            <Chessboard
              position={fen}
              onDrop={({ sourceSquare, targetSquare }) => {
                console.log("onDrop called");
                handleMove({ sourceSquare, targetSquare });
              }}
              orientation={playerColor}
              draggable={!gameRef.current.game_over}
            />
          </div>
        </div>
      ) : (
        <Load></Load>
      )}
    </div>
  );
}

export default MyGame;
