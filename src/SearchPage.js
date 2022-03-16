import * as React from 'react';
import './App.css';
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
import OutlinedInput from '@mui/material/OutlinedInput';
import ListItemText from '@mui/material/ListItemText';
import Checkbox from '@mui/material/Checkbox';
import { useEffect, useState } from 'react';
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

class RegExp1 extends RegExp {
    [Symbol.match](str) {
      const result = RegExp.prototype[Symbol.match].call(this, str);
      if (result) {
        return 'VALID';
      }
      return 'INVALID';
    }
}

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

export default function SearchPage() {

    const [offset, setOffset] = useState(0);
    const [perpage, setPerpage] = useState(5);
    const navigate = useNavigate();
    const [searchContent, setSearchContent] = useState('');
    const [loading, setLoading] = useState(true);
    const [artistFilter, setArtistFilter] = useState([{}]);
    const [albumFilter, setAlbumFilter] = useState([{}]);
    // const [genresFilter, setGenresFilter] = useState([{}]);
    const [filterList, setFilterList] = useState([{}]);
    const [open, setOpen] = useState(false);
    const [content, setContent] = useState([{}]);
    const [filterType, setFilterType] = useState('all');
    const [data, setData] = useState([{}]);
    const [searchType, setSearchType] = useState('');
    const [input, setInput] = useState(false);
    const [personName, setPersonName] = useState([]);

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
        setPersonName([]);
        switch (event.target.value) {
            case "singer":
                setFilterList(Object.keys(artistFilter));
                break;
            case "album":
                setFilterList(Object.keys(albumFilter));
                break;
            default:
                break;
        }
        console.log(filterList);
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

    const handleTypeChange = (event) => {
        setSearchType(event.target.value);
    };

    useEffect(() => {
        setSearchContent(location.state.query)
        setSearchType(location.state.type)
        async function getSearchResult(state) {
            axios({
                method: "GET",
                url: `/profile?query=${state.query}&type=${state.type}`,
            })
            .then((response) => {
                setData(response.data)
                setProfileData(response.data['results'])
                setLoading(false)
                setInput(false)
                setArtistFilter(response.data['artist_name'][0])
                setAlbumFilter(response.data['album_name'][0])
                // setGenresFilter(response.data['genres'][0])
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
    }, [])

    function getSearchResultData() {
        setLoading(true)
        setInput(false)
        setFilterType("all")
        axios({
            method: "GET",
            url: `/profile?query=${searchContent}&type=${searchType}`,
        })
        .then((response) => {
            setData(response.data)
            setProfileData(response.data['results'])
            setArtistFilter(response.data['artist_name'][0])
            setAlbumFilter(response.data['album_name'][0])
            // setGenresFilter(response.data['genres'][0])
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

    const changeInput = (event) => {
        setSearchContent(event.target.value);
        setInput(true)
    }

    const Highlighted = ({text = '', highlight = ''}) => {
        const list = highlight.replaceAll(" ", "|\\b")
        const t = text.replaceAll(" ", "* *")
        const textList = t.split("*")
        return (
            <span>
                {textList.map((t, i) => (
                    t.match(new RegExp1(`\\b${list}+`, "gi")) === 'VALID' ? 
                        <mark key={i}>{t}</mark> : <span key={i}>{t}</span>
                ))}
            </span>
        )
    }

    const handleMultiChange = (event) => {
        const {
            target: { value },
        } = event;
        var v = typeof value === 'string' ? value.split(',') : value;
        setPersonName(v)
        setPersonName(prev => {
            console.log(prev);
            var dict = [];
            if (filterType === 'singer') {
                prev.map((result) => {
                    artistFilter[result].map((r) => {
                        dict.push(r);
                        return 0;
                    })
                    return 0;
                });
                setProfileData(dict);
            } else if (filterType === 'album') {
                prev.map((result) => {
                    albumFilter[result].map((r) => {
                        dict.push(r);
                        return 0;
                    })
                    return 0;
                });
                setProfileData(dict);
            } else {
                setProfileData(data["results"]);
            }
            return prev;
        });
        setOffset(0);
        setOffset(p => {
            return p;
        });
    };

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AppBar position="relative">
                <Toolbar>
                    <Stack direction="row" spacing={2} justifyContent="center" sx={{mt:2, mb:2}}>
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
                                        <MenuItem value={"lyrics"}>Lyrics</MenuItem>
                                        <MenuItem value={"song_name_preprocess"}>Song Name</MenuItem>
                                        <MenuItem value={"album_name_preprocess"}>Album Name</MenuItem>
                                        <MenuItem value={"artist_name_preprocess"}>Singer Name</MenuItem>
                                    </Select>
                            </FormControl>
                        </Box>
                        <Grid>
                            <div>
                                <input 
                                    onKeyPress={(event) => {
                                        if (event.key === 'Enter') {
                                            getSearchResultData()
                                        }
                                    }}
                                    required type="text" defaultValue={searchContent} 
                                    placeholder="Input a query" className={"App-input-search"}
                                    onChange={changeInput} maxLength={50}/>
                                <IconButton sx={{ p: '10px' }} aria-label="search" onClick={e => getSearchResultData()}>
                                    <SearchIcon />
                                </IconButton>
                                {/* <button onClick={e => getSearchResultData()} className={"App-submit"}> 
                                    Search 
                                </button> */}
                            </div>
                        </Grid>
                    </Stack>
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
                            {loading ? 
                                <div></div>
                            :
                            <Stack justifyContent="center">
                                <Grid>
                                    <FormControl>
                                        <RadioGroup
                                            row
                                            aria-labelledby="demo-row-radio-buttons-group-label"
                                            name="row-radio-buttons-group"
                                            value={filterType}
                                            onChange={handleRadioChange}
                                        >
                                            <FormControlLabel value="singer" control={<Radio />} label="Singer" />
                                            <FormControlLabel value="album" control={<Radio />} label="Album" />
                                            <FormControlLabel value="all" control={<Radio />} label="All Result"/>
                                        </RadioGroup>
                                    </FormControl>
                                </Grid>
                                {filterType === 'all' ?
                                    <div></div>
                                    : <FormControl>
                                        <InputLabel id="demo-multiple-checkbox-label">{filterType}</InputLabel>
                                            <Select
                                                labelId="demo-multiple-checkbox-label"
                                                id="demo-multiple-name"
                                                multiple
                                                value={personName}
                                                onChange={handleMultiChange}
                                                input={<OutlinedInput label="Name" />}
                                                renderValue={(selected) => selected.join(', ')}
                                                MenuProps={MenuProps}
                                                >
                                                {filterList.map((name) => (
                                                    <MenuItem
                                                        key={name}
                                                        value={name}
                                                    >
                                                        <Checkbox checked={personName.indexOf(name) > -1} />
                                                        <ListItemText primary={name} />
                                                    </MenuItem>
                                                ))}
                                            </Select>
                                    </FormControl>
                                }
                            </Stack>}
                            <Button variant={"contained"} onClick={e => back()}>return to main page</Button>
                        </Typography>
                    </Container>
                </Box>
                {loading ? 
                    Array.apply(null, { length: 5 }).map((e, i) => (
                        <Paper
                            key={i}
                            sx={{
                                margin: 'auto',
                                maxWidth: 1000,
                                flexGrow: 1,
                                marginTop: 3,
                            }}
                        >
                            <Skeleton animation="wave" variant="rect" width={1000} height={250} className="skeleton-card" />
                        </Paper>
                    ))
                    : profileData.slice(offset, offset + perpage).map((result, i) => (
                        <Paper
                            key={i}
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
                                            <Typography variant="h4" component="div">
                                                {/* {result.song_name} */}
                                                {searchType !== 'song_name_preprocess' ?
                                                    result.song_name
                                                    : input ? result.song_name
                                                    : <Highlighted text={result.song_name} highlight={searchContent}/> }
                                            </Typography>
                                            <Typography variant="body1">
                                                <b>Singer Name:</b> 
                                                {searchType !== 'artist_name_preprocess' ?
                                                    result.artist_name
                                                    : input ? result.artist_name
                                                    : <Highlighted text={result.artist_name} highlight={searchContent}/> }
                                            </Typography>
                                            <Typography variant="body1">
                                                <b>Album Name:</b>
                                                {searchType !== 'album_name_preprocess' ?
                                                    result.album_name
                                                    : input ? result.album_name
                                                    : <Highlighted text={result.album_name} highlight={searchContent}/> }
                                            </Typography>
                                            <Typography variant="body1">
                                                <b>Genres:</b> {result.genres}
                                            </Typography>
                                            <Typography variant="body1" gutterBottom>
                                                <b>Release Date:</b> {result.release_date}
                                            </Typography>
                                            <Typography variant="body2" color="text.secondary">
                                                <b>Part Lyrics: </b>
                                                {searchType !== 'lyrics' ?
                                                    result.mark_lyric
                                                : input ? result.mark_lyric
                                                : <Highlighted text={result.mark_lyric} highlight={searchContent}/> }
                                            </Typography>
                                        </Grid>
                                        <Grid item>
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
                            <Typography>
                                <b>Singer Name:</b> {content.artist_name}
                            </Typography>
                            <Typography>
                                <b>Album Name:</b> {content.album_name}
                            </Typography>
                            <Typography>
                                <b>Genres:</b> {content.genres}
                            </Typography>
                            <Typography>
                                <b>Release Date:</b> {content.release_date}
                            </Typography>
                        </DialogTitle>
                        <DialogContent>
                            <DialogContentText>
                                <b>Whole Lyris:</b>
                                {content.all_lyrics.map(function(r) {
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
                                    <MenuItem value={5}>-5-</MenuItem>
                                    <MenuItem value={10}>-10-</MenuItem>
                                    <MenuItem value={20}>-20-</MenuItem>
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
