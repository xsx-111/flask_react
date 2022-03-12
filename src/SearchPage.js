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
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormLabel from '@mui/material/FormLabel';
import { useEffect, useState } from 'react';
import axios from "axios";
import { generatePath, useLocation, useNavigate } from 'react-router-dom';

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

export default function SearchPage() {

    const [offset, setOffset] = useState(0);
    const [perpage, setPerpage] = useState(5);
    const navigate = useNavigate();
    const [searchContent, setSearchContent] = useState('');
    const [loading, setLoading] = useState(true);
    const [artistFilter, setArtistFilter] = useState([{}]);
    const [albumFilter, setAlbumFilter] = useState([{}]);
    const [genresFilter, setGenresFilter] = useState([{}]);
    const [filterList, setFilterList] = useState([{}]);
    const [open, setOpen] = useState(false);
    const [content, setContent] = useState([{}]);
    const [filterType, setFilterType] = useState('disable');
    const [select, setSelect] = useState('None');
    const [data, setData] = useState([{}])

    const handleChange = (event, value) => {
        setOffset(perpage*(value-1));
    };

    const handleNumChange = (event) => {
        setPerpage(event.target.value);
        setOffset(0);
    };

    const handleRadioChange = (event) => {
        setFilterType(event.target.value);
        setProfileData(data["results"]);
        setSelect("None");
        switch (event.target.value) {
            case "singer":
                setFilterList(Object.keys(artistFilter));
                break;
            case "album":
                setFilterList(Object.keys(albumFilter));
                break;
            case "category":
                setFilterList(Object.keys(genresFilter));
                break;
            default:
                break;
        }
        console.log(filterList);
    };

    const handleSelectChange = (event) => {
        setSelect(event.target.value);
        if (event.target.value !== "None") {
            switch (filterType) {
                case "singer":
                    setProfileData(artistFilter[event.target.value]);
                    break;
                case "album":
                    setProfileData(albumFilter[event.target.value]);
                    break;
                case "category":
                    setProfileData(genresFilter[event.target.value]);
                    break;
                default:
                    break;
            }
        } else {
            setProfileData(data["results"]);
        }
        setOffset(0);
    };

    const [profileData, setProfileData] = useState([{}]);
    const location = useLocation();

    function back() {
        navigate("/");
    }

    const handleClickOpen = (result) => () => {
        setOpen(true);
        setContent(result);
        console.log(result);
    };
    
    const handleClose = () => {
        setOpen(false);
    };

    useEffect(() => {
        async function getSearchResult(state) {
            axios({
                method: "GET",
                url: `/profile/${state}`,
            })
            .then((response) => {
                setData(response.data)
                setProfileData(response.data['results'])
                setLoading(false)
                setArtistFilter(response.data['artist_name'][0])
                setAlbumFilter(response.data['album_name'][0])
                setGenresFilter(response.data['genres'][0])
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
        console.log(artistFilter);
        console.log(Object.keys(artistFilter))
    }, [])

    function getSearchResultData() {
        setLoading(true)
        setSelect("None")
        setFilterType("disable")
        axios({
            method: "GET",
            url: `/profile/${searchContent}`,
        })
        .then((response) => {
            setData(response.data)
            setProfileData(response.data['results'])
            setArtistFilter(response.data['artist_name'][0])
            setAlbumFilter(response.data['album_name'][0])
            setGenresFilter(response.data['genres'][0])
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
                            Song Results<br/>
                            <Stack spacing={2} justifyContent="center">
                                <FormControl>
                                    {/*<FormLabel id="demo-row-radio-buttons-group-label">Filter</FormLabel>*/}
                                    <RadioGroup
                                        row
                                        aria-labelledby="demo-row-radio-buttons-group-label"
                                        name="row-radio-buttons-group"
                                        value={filterType}
                                        onChange={handleRadioChange}
                                    >
                                        <FormControlLabel value="singer" control={<Radio />} label="Singer" />
                                        <FormControlLabel value="album" control={<Radio />} label="Album" />
                                        <FormControlLabel value="category" control={<Radio />} label="Category" />
                                        <FormControlLabel value="disabled" disabled control={<Radio />} label="other"/>
                                    </RadioGroup>
                                </FormControl>
                                {filterType === 'disable' ?
                                    <div></div>
                                    : <FormControl>
                                        <InputLabel id="demo-simple-select-label">{filterType}</InputLabel>
                                            <Select
                                                labelId="demo-simple-select-label"
                                                id="demo-simple-select"
                                                label="num"
                                                value={select}
                                                onChange={handleSelectChange}
                                            >
                                                <MenuItem value="None">None</MenuItem>
                                                {filterList.map((result) => (
                                                    <MenuItem value={result}>{result}</MenuItem>
                                                ))}
                                            </Select>
                                    </FormControl>
                                }
                            </Stack>
                            {/*<FormControlLabel control={<Checkbox defaultChecked />} label="Singer" />
                            <FormControlLabel control={<Checkbox />} label="Album" />
                            <FormControlLabel control={<Checkbox />} label="Type" /><br/><br/>*/}
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
                                            {/* <Button size="medium" variant='outlined' onClick={e => toDetail(result.id)}>View</Button> */}
                                            <Button size="medium" variant='outlined' onClick={handleClickOpen(result)}>Whole lyrics</Button>
                                        </Grid>
                                    </Grid>
                                </Grid>
                            </Grid>
                        </Paper>
                    ))
                }
                { open ?
                    <Dialog
                        open={open}
                        onClose={handleClose}
                        scroll="paper"
                        aria-labelledby="scroll-dialog-title"
                        aria-describedby="scroll-dialog-description"
                    >
                        <DialogTitle id="scroll-dialog-title">
                            {content.song_name}
                        </DialogTitle>
                        <DialogContent>
                            Singer Name: {content.artist_name}
                            <DialogContentText>
                                {content.lyrics.map(function(r) {
                                    return (
                                        <Typography>
                                            {r}
                                        </Typography>
                                    )
                                })}
                            </DialogContentText>
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={handleClose}>Cancel</Button>
                        </DialogActions>
                    </Dialog>
                    : <div></div>
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