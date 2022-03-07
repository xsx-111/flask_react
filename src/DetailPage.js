import { useEffect, useState } from 'react';
import axios from "axios";
import {useLocation} from 'react-router-dom';

export default function DetailPage() {

  const [profileData, setProfileData] = useState([{}]);
  const location = useLocation();
  const [wholeLyrics, setWholeLyrics] = useState([]);

  useEffect(() => {
    async function getSearchResult() {
      axios({
        method: "GET",
        url: `/whole/${location.state}`,
      })
      .then((response) => {
        setProfileData(response.data)
        setWholeLyrics(response.data[0]['wholeLyrics'])
        console.log(wholeLyrics)
      }).catch((error) => {
        if (error.response) {
          console.log(error.response)
          console.log(error.response.status)
          console.log(error.response.headers)
        }
      })
    }
    getSearchResult();
    console.log(profileData);
  }, [])

  return (
    <div>
        {wholeLyrics.map(function(result) {
            return (
                <div>{result}</div>
            )
        })}
    </div>
  );
}