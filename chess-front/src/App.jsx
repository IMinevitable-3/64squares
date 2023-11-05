import Oops from './pages/404'
import Index from './pages/home'
import Layout from './pages/layout'
import { Game } from './pages/game'
import MyGame from './pages/MyGame'
import './App.css'
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="/" element={<Index />} />
        <Route path='/play/:id' element={<Game/>}/>
        <Route path='/play/created/:id' element={<MyGame/>}/>


        <Route path="*" element={<Oops />} />
      </Route>
    </Routes>
  );
}

export default App
