import './App.css';
import EmotionDashboard from './EmotionDashboard';
//import Exper5 from './exp5';
//import Exper6 from './exp6';
import Home from "./homw";
import { Route, Routes } from 'react-router-dom';
//import { UserProvider } from './UserContext';
//import Fetchdata from './exp8';

function App() {
  return (
    <Routes>
        <Route path='/' element={<Home/>} />
        <Route path='/represent' element={<EmotionDashboard/>}/>
    </Routes>
  );
}

export default App;
//<UserProvider>
//<Routes>
//  <Route path='/' element={<Exper5 />} />
//    <Route path='/home' element={<Home/>} />
//    <Route path='/exp6' element={<Exper6 />} />
//    <Route path='/fetch' element={<Fetchdata/>}/>
//  </Routes>
// </UserProvider> }
