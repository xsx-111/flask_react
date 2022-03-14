import { useState } from 'react'
import './App.css';
import { useNavigate } from "react-router-dom";
import {createTheme, ThemeProvider} from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import * as React from "react";
import Link from "@mui/material/Link";

function Copyright() {
    return (
        <Typography variant="body2" color="text.secondary" align="center">
            {'Copyright © '}
            <Link color="inherit" href="https://mui.com/">
                Your Website
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

export default function App() {

  const [fName, setfName] = useState('');
  const [searchType, setSearchType] = useState('Lyrics');
  const navigate = useNavigate();

  const Theme = { palette: { primary: { main: '#f1d692' }, secondary: { main: '#FFFFFF' } } };
  const theme = createTheme(Theme);

  function getData() {
    navigate("/SearchPage", {state: {
        query: fName,
        type: searchType
    }});
    }

  const handleTypeChange = (event) => {
    setSearchType(event.target.value);
    };
  
  return (
    <ThemeProvider theme={theme}>
            <CssBaseline />
            <div className={"App"}>
                <header className={"App-header"}>
                    <div className={"App-title"}>
                        Lyrics Search
                    </div>
                    <Stack direction="row" spacing={2} sx={{mt: 10}} justifyContent="center">
                        <Box sx={{ width: 70, height: 20, mr: 8 }}>
                            <FormControl>
                                <InputLabel id="demo-simple-select-label">Type</InputLabel>
                                    <Select
                                        labelId="demo-simple-select-label"
                                        id="demo-simple-select"
                                        value={searchType}
                                        label="num"
                                        onChange={handleTypeChange}
                                    >
                                        <MenuItem value={"Lyrics"}>Lyrics</MenuItem>
                                        <MenuItem value={"song_name_preprocess"}>Song Name</MenuItem>
                                        <MenuItem value={"album_name_preprocess"}>Album Name</MenuItem>
                                        <MenuItem value={"artist_name_preprocess"}>Singer Name</MenuItem>
                                        <MenuItem value={"genres_preprocess"}>Genres</MenuItem>
                                    </Select>
                            </FormControl>
                        </Box>
                        <Grid>
                            <div>
                                <input 
                                    onKeyPress={(event) => {
                                        if (event.key === 'Enter') {
                                            getData()
                                        }
                                    }}
                                    required type="text" placeholder="Type a query" className={"App-input"} onChange={e => setfName(e.target.value)}/>
                                <button onClick={e => getData()} className={"App-submit"}> 
                                    Search 
                                </button>
                            </div>
                        </Grid>
                    </Stack>
                </header>
                <Box sx={{ bgcolor: '#efd697', p: 6 }} component="footer">
                    <Typography variant="h6" align="center" gutterBottom>
                        Footer
                    </Typography>
                    <Typography
                        variant="subtitle1"
                        align="center"
                        color="text.secondary"
                        component="p"
                    >
                        TTDS cw3
                    </Typography>
                    <Copyright />
                </Box>
            </div>
    </ThemeProvider>
  );
}
