import { useState } from 'react'
import './App.css';
import { useNavigate } from "react-router-dom";

export default function App() {

  const [fName, setfName] = useState('');
  const navigate = useNavigate();

  function getData() {
    navigate("/SearchPage", {state: fName});
  }
  
  return (
    <div className="App">
      <header className="App-header">
        <div>
          <input required type="text" placeholder="Type a query" className="App-input" onChange={e => setfName(e.target.value)}/>
          <button onClick={e => getData()} className="App-submit"> Search </button>
        </div>
      </header>
    </div>
  );
}
