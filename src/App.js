import { useState } from 'react'
import './App.css';
import { useNavigate } from "react-router-dom";
import {createTheme, ThemeProvider} from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
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
  const navigate = useNavigate();

  const Theme = { palette: { primary: { main: '#f1d692' }, secondary: { main: '#FFFFFF' } } };
  const theme = createTheme(Theme);

  function getData() {
    navigate("/SearchPage", {state: fName});
  }

  return (
    <ThemeProvider theme={theme}>
            <CssBaseline />
            <div className={"App"}>
                <header className={"App-header"}>
                    <div className={"App-title"}>
                        Lyrics Search
                    </div>
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