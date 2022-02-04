import { useState } from 'react'
import axios from "axios";
import './App.css';

function App() {

  const [fName, setfName] = useState('');
  const [profileData, setProfileData] = useState(null);

  function getData() {
    axios({
      method: "GET",
      url: `/profile/${fName}`,
    })
    .then((response) => {
      const res = response.data
      setProfileData(({
        profile_name: res.name,
        about_me: res.about}))
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}

  return (
    <div className="App">
      <header className="App-header">
        <div>
          <input required type="text" placeholder="Type a query" className="App-input" onChange={e => setfName(e.target.value)}/>
          <button onClick={e => getData()} className="App-submit"> Search </button>
        </div>
        {profileData && <div>
              <p>Profile name: {profileData.profile_name}</p>
              <p>About me: {profileData.about_me}</p>
            </div>
        }
      </header>
    </div>
  );
}

export default App;
