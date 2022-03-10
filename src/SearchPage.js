import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Button from '@mui/material/Button';
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
import { styled } from '@mui/material/styles';
import ButtonBase from '@mui/material/ButtonBase';
import Skeleton from '@mui/material/Skeleton';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Collapse from '@mui/material/Collapse';
import CardContent from '@mui/material/CardContent';
import { useEffect, useState, Fragment } from 'react';
import axios from "axios";
import { useLocation, useNavigate } from 'react-router-dom';

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

const Img = styled('img')({
    margin: 'auto',
    display: 'block',
    maxWidth: '100%',
    maxHeight: '100%',
});

const ExpandMore = styled((props) => {
    const { expand, ...other } = props;
    return <IconButton {...other} />;
  })(({ theme, expand }) => ({
    transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
  }));

export default function SearchPage() {

    const [offset, setOffset] = useState(0);
    const [perpage, setPerpage] = useState(5);
    const navigate = useNavigate();
    const [searchContent, setSearchContent] = useState('');
    const [loading, setLoading] = useState(true);
    const [expanded, setExpanded] = useState(false);

    const handleChange = (event, value) => {
        setOffset(perpage*(value-1));
    };

    const handleExpandClick = () => {
        setExpanded(!expanded);
    };

    const handleNumChange = (event) => {
        setPerpage(event.target.value);
        setOffset(0);
    };

    const [profileData, setProfileData] = useState([{}]);
    const location = useLocation();

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
            setLoading(false)
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
        setLoading(true)
        axios({
            method: "GET",
            url: `/profile/${searchContent}`,
        })
        .then((response) => {
            setProfileData(response.data)
            setOffset(0)
            setLoading(false)
            console.log(response.data)
        }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    function toDetail(id) {
        navigate("/DetailPage", {state: id});
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
                {loading ?
                    Array.apply(null, { length: 5 }).map((e, i) => (
                        <Paper
                            sx={{
                                margin: 'auto',
                                maxWidth: 1000,
                                flexGrow: 1,
                                marginTop: 3,
                            }}
                        >
                            <Skeleton animation="wave" variant="rect" width={1000} height={220} className="skeleton-card" />
                        </Paper>
                    ))
                    : profileData.slice(offset, offset + perpage).map((result) => (
                        <Paper
                            sx={{
                                p: 2,
                                margin: 'auto',
                                maxWidth: 1000,
                                flexGrow: 1,
                                marginTop: 3,
                            }}
                        >
                            <Grid container spacing={2}>
                                <Grid item>
                                    <ButtonBase sx={{ width: 220, height: 220 }}>
                                        <Img alt="complex" src={result.album_cover_url} />
                                    </ButtonBase>
                                </Grid>
                                <Grid item xs={12} sm container>
                                    <Grid item xs container direction="column" spacing={2}>
                                        <Grid item xs>
                                            <Typography gutterBottom variant="h4" component="div">
                                                {result.song_name}
                                            </Typography>
                                            <Typography variant="h6" gutterBottom>
                                                Singer Name: {result.artist_name}
                                            </Typography>
                                            <Typography variant="body2" color="text.secondary">
                                                {result.mark_lyric}
                                            </Typography>
                                        </Grid>
                                        <Grid item>
                                            <Button size="medium" variant='outlined' onClick={e => toDetail(result.id)}>View</Button>
                                        </Grid>
                                        {/* <ExpandMore
                                            expand={expanded}
                                            onClick={handleExpandClick}
                                            aria-expanded={result.song_id}
                                            aria-label="show more"
                                            >
                                            <ExpandMoreIcon />
                                        </ExpandMore> */}
                                    </Grid>
                                </Grid>
                                {/* <Collapse in={expanded} timeout="auto" unmountOnExit>
                                    <CardContent>
                                        {result.lyrics.map(function(r) {
                                            return (
                                                <Typography>
                                                    {r}
                                                </Typography>
                                            )
                                        })}
                                    </CardContent>
                                </Collapse> */}
                            </Grid>
                        </Paper>
                    ))
                }
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
                                    <MenuItem value={5}>5</MenuItem>
                                    <MenuItem value={10}>10</MenuItem>
                                    <MenuItem value={20}>20</MenuItem>
                                </Select>
                        </FormControl>
                    </Box>
                </Stack>
            </main>
            <Box sx={{ bgcolor: '#efd697', p: 6, marginTop: 10 }} component="footer">
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