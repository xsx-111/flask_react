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
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import DirectionsIcon from '@mui/icons-material/Directions';
import { styled } from '@mui/material/styles';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useEffect, useState } from 'react';
import axios from "axios";
import {useLocation} from 'react-router-dom';

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

const cards = [1, 2, 3, 4, 5, 6, 7, 8, 9];
const Theme = { palette: { primary: { main: '#e0b159' }, secondary: { main: '#FFFFFF' } } };
const theme = createTheme(Theme);


//constant for the self-defined selector
const BootstrapInput = styled(InputBase)(({ theme }) => ({
    'label + &': {
        marginTop: theme.spacing(3),
    },
    '& .MuiInputBase-input': {
        //圆角的半径
        borderRadius: 4,
        position: 'relative',
        backgroundColor: '#f3dda6',
        border: '0px solid #efd697',
        fontSize: 10,
        padding: '8px 26px 10px 5px',
        transition: theme.transitions.create(['border-color', 'box-shadow']),
        // Use the system font instead of the default Roboto font.
        fontFamily: [
            '-apple-system',
            'BlinkMacSystemFont',
            '"Segoe UI"',
            'Roboto',
            '"Helvetica Neue"',
            'Arial',
            'sans-serif',
            '"Apple Color Emoji"',
            '"Segoe UI Emoji"',
            '"Segoe UI Symbol"',
        ].join(','),
        '&:focus': {
            borderRadius: 4,
            borderColor: '#efd697',
            boxShadow: '0 0 0 0.2rem rgba(0,123,255,.25)',
        },
    },
}));

export default function SearchPage() {

    const [displayNum, setDisplayNum] = React.useState('');
    const handleChange = (event) => {
        setDisplayNum(event.target.value);
    };

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
                            inputProps={{ 'aria-label': 'search google maps' }}
                        />
                        <IconButton type="submit" sx={{ p: '10px' }} aria-label="search">
                            <SearchIcon />
                        </IconButton>
                    </Paper><div>
                        <FormControl sx={{ m: 1 }} variant="filled" size={'small'}>
                            <InputLabel htmlFor="demo-customized-textbox">diaplayNum</InputLabel>
                            <BootstrapInput id="demo-customized-textbox" />
                        </FormControl>
                        <FormControl sx={{ m: 1 }} variant="standard">
                            <InputLabel id="demo-customized-select-label">displayNum</InputLabel>
                            <Select
                                labelId="demo-customized-select-label"
                                id="demo-customized-select"
                                value={displayNum}
                                onChange={handleChange}
                                input={<BootstrapInput />}
                            >
                               <MenuItem value="">
                                    <em>None</em>
                                </MenuItem>
                                <MenuItem value={5}>5</MenuItem>
                                <MenuItem value={10}>10</MenuItem>
                                <MenuItem value={15}>15</MenuItem>
                            </Select>
                        </FormControl>
                    </div>
                </Toolbar>
            </AppBar>
            <main>
                {/* Hero unit */}
                <Box
                    sx={{
                        bgcolor: '#efd697',
                        pt: 2,
                        pb: 6,
                    }}
                >
                    <Container maxWidth="sm">
                        <Typography
                            component="h1"
                            variant="h3"
                            align="center"
                            color="text.primary"
                            gutterBottom
                        >
                            Song Results
                        </Typography>
                        <Typography variant="h5" align="center" color="text.secondary" paragraph>

                        </Typography>
                        <Stack
                            sx={{ pt: 4 }}
                            direction="row"
                            spacing={2}
                            justifyContent="center"
                        >
                            <Button variant="contained">Main call to action</Button>
                            <Button variant="outlined">Secondary action</Button>
                        </Stack>
                    </Container>
                </Box>
                <Container sx={{ py: 8 }}>
                    {/* End hero unit */}
                    <Grid container spacing={2}>
                        {profileData.map((result) => (
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
                                        // component="img"
                                        // sx={{
                                        //     // 16:9
                                        //     pt: '56.25%',
                                        // }}
                                        // image={result.image}
                                        // alt="random"
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
                    Something here to give the footer a purpose!
                </Typography>
                <Copyright />
            </Box>
        </ThemeProvider>
    );
}