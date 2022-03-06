import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Pagination from '@mui/material/Pagination';
import { useEffect, useState } from 'react';
import axios from "axios";
import {useLocation, useNavigate} from 'react-router-dom';

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

const Theme = { palette: { primary: { main: '#d7b067' }, secondary: { main: '#FFFFFF' } } };
const theme = createTheme(Theme);

export default function SearchPage() {

    const [offset, setOffset] = useState(0);
    const [perpage, setPerpage] = useState(10);
    const navigate = useNavigate();
    const [searchContent, setSearchContent] = useState('');

    const handleChange = (event, value) => {
        setOffset(perpage*(value-1));
    };

    const handleNumChange = (event) => {
        setPerpage(event.target.value);
    };

    const [profileData, setProfileData] = useState([{}]);
    const location = useLocation()

    function back() {
    navigate("/");
  }

    useEffect(() => {
        async function getSearchResult(state) {
        axios({
            method: "GET",
            url: `/profile/${state}`,
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
        getSearchResult(location.state);
        console.log(profileData);
    }, [])

    function getSearchResultData() {
        axios({
            method: "GET",
            url: `/profile/${searchContent}`,
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

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AppBar position="relative">
                <Toolbar>
                    <Paper
                        component="form"
                        sx={{ bgcolor: '#efd697', p: '2px 4px', display: 'flex', alignItems: 'center', width: 550 }}
                    >
                        <InputBase
                            sx={{ ml: 1, flex: 1 }}
                            placeholder="input lyrics you want to search"
                            defaultValue={location.state}
                            onChange={e => setSearchContent(e.target.value)}
                        />
                        <IconButton sx={{ p: '10px' }} aria-label="search" onClick={e => getSearchResultData()}>
                            <SearchIcon />
                        </IconButton>
                    </Paper>
                </Toolbar>
            </AppBar>
            <main>
                <Box
                    sx={{
                        bgcolor: '#ecd49a',
                        pt: 2,
                        pb: 6,
                    }}
                >
                    <Container maxWidth="sm">
                        <Typography
                            component="h1"
                            variant="h3"
                            align="center"
                            color={'#444444'}
                            sx={{mt: 5}}
                        >
                            Song Results
                        </Typography>
                        <Typography
                            component="h1"
                            variant="h3"
                            align="center"
                            color="text.primary"
                            sx={{mt: 5}}
                        >
                            <Button variant={"contained"} onClick={e => back()}>return to main page</Button>
                        </Typography>
                    </Container>
                </Box>
                <Container sx={{ py: 8 }}>
                    {/* End hero unit */}
                    <Grid container spacing={2}>
                        {profileData.slice(offset, offset + perpage).map((result) => (
                            <Grid item key={result.id} xs={12} sm={6} md={4}>
                                <Card
                                    sx={{ height: 400 }}
                                    // sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                                >
                                    <CardMedia
                                        component="img"
                                        height="220"
                                        image={result.image}
                                        alt="album image"
                                    />
                                    <CardContent sx={{ flexGrow: 1 }}>
                                        <Typography gutterBottom variant="h5" component="h2">
                                            {result.song_name}
                                        </Typography>
                                        <Typography>
                                            {result.singer_name}
                                        </Typography>
                                        <Typography>
                                            {result.lyrics}
                                        </Typography>
                                    </CardContent>
                                    <CardActions>
                                        <Button size="small">View</Button>
                                    </CardActions>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                    <Stack direction="row" spacing={2} sx={{mt: 10}} justifyContent="center">
                        <Pagination
                            limit={perpage}
                            offset={offset}
                            count={Math.ceil(profileData.length/perpage)}
                            onChange={handleChange}
                            showFirstButton showLastButton
                            sx={{ height: 20, mt: 1 }}
                        />
                        <Box sx={{ width: 70, height: 20 }}>
                            <FormControl>
                                <InputLabel id="demo-simple-select-label">number</InputLabel>
                                    <Select
                                        labelId="demo-simple-select-label"
                                        id="demo-simple-select"
                                        value={perpage}
                                        label="num"
                                        onChange={handleNumChange}
                                    >
                                        <MenuItem value={10}>10</MenuItem>
                                        <MenuItem value={30}>30</MenuItem>
                                        <MenuItem value={50}>50</MenuItem>
                                        <MenuItem value={100}>100</MenuItem>
                                    </Select>
                            </FormControl>
                        </Box>
                    </Stack>
                </Container>
            </main>
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
                    TTDS CW3
                </Typography>
                <Copyright />
            </Box>
        </ThemeProvider>
    );
}