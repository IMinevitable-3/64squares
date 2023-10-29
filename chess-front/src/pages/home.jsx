import Chessboard from 'chessboardjsx'
import { useEffect } from 'react';
import { WEB_SOCKET , WEB_SOCKET_PORT } from '../utils/config';
const  Index = ()=>{
    
        useEffect(() => {
            
            // const socket = new WebSocket('ws://172.19.0.5:8000/ws/lobby/');
            const socket = new WebSocket(`ws://${WEB_SOCKET}:${WEB_SOCKET_PORT}/ws/lobby/`);
             
            socket.onopen = () => {
                console.log('WebSocket connection opened');
            };
    
            socket.onmessage = (event) => {
                console.log('Message from server:', event.data);
            };
    
            socket.onclose = () => {
                console.log('WebSocket connection closed');
            };
    
            return () => {
                // Cleanup the WebSocket connection when the component unmounts
                socket.close();
            };
        }, []);
    
   
    return(
        <>
            <Chessboard position="start" />
        </>
    )
}
export default Index