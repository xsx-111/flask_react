import { useEffect, useState } from 'react';
import axios from "axios";
import {useLocation} from 'react-router-dom';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

export default function SearchPage() {

  const [profileData, setProfileData] = useState([{}]);
  const location = useLocation();

  useEffect(() => {
    async function getSearchResult() {
      axios({
        method: "GET",
        url: `/profile/${location.state}`,
      })
      .then((response) => {
        setProfileData(response.data)
        console.log(response.data)
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
    <Box sx={{display: 'flex', flexDirection: 'row', p: 1, m: 1, flexWrap: 'wrap'}}>
      {profileData.map(function(result) {
        return (
          <Card sx={{ width: 220, height: 400, p: 1, m: 1 }}>
            <CardMedia
              component="img"
              height="220"
              image={result.image}
              alt="album image"
            />
            <CardContent sx={{ height: 110 }}>
              <Typography gutterBottom variant="h5" component="div">
                {result.song_name}
              </Typography>
              <Typography>
                {result.singer_name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {result.lyrics}
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small">Learn More</Button>
            </CardActions>
          </Card>
        )
      })}
    </Box>
  );
}