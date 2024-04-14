<script setup>
import Navbar from './Navbar.vue'
import { useStore } from 'vuex'
import { onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router'
const store = useStore()
const router = useRouter()
let username = store.state.username
let roles = store.state.roles
let songs = ref([])
let songGroups = ref([])
let albums = ref([])
let albumGroups = ref([])
let playlists = ref([])
let playlistGroups = ref([])
let ifplaylist = ref(false);
let curralbum = ref('');
let currsong = ref('');
let curraudio = ref('');
let currsongid = ref('');
let currlyrics = ref('');
let rating = ref(0);
let currartist = ref('');
let isChecked1 = ref(false);
let isChecked2 = ref(false);
let isChecked3 = ref(false);
let isChecked4 = ref(false);
let isChecked5 = ref(false);
let count = ref(0);
let sq = ref('');

const rate = async (val) => {
    count.value = val;
    await updateRating(val);
}

const updateRating = async (val) => {
    try {
        const response = await fetch(subrate(currsong.value, val), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rating: val })
        });
        const data = await response.json()
        if (response.ok) {
            rating.value = data.rating;
            updateStars(val);
            await fetchsongs()
        } else {
            console.error('Failed to update rating:', response.statusText);
        }
    } catch (error) {
        console.error('Error updating rating:', error);
    }
}

const updateStars = (val) => {
    isChecked1.value = val >= 1;
    isChecked2.value = val >= 2;
    isChecked3.value = val >= 3;
    isChecked4.value = val >= 4;
    isChecked5.value = val >= 5;
}


const subrate = (name, val) => {
    return `http://127.0.0.1:5000/api/rate/${name}/${val}`;
}

const getAlbumart = (name) => {
    return `http://127.0.0.1:5000/api/album-art/${name}/album_art.jpg`;
}

const getSong = (name, album, song) => {
    curralbum.value = getAlbumart(album);
    currsong.value = song.title;
    rating.value = song.rating;
    currsongid.value = song.id;
    currartist.value = song.artist;
    currlyrics.value = song.lyrics;
    isChecked1.value = false;
    isChecked2.value = false;
    isChecked3.value = false;
    isChecked4.value = false;
    isChecked5.value = false;
    curraudio.value = `http://127.0.0.1:5000/api/song/${album}/${name}.mp3`;
    fetchsongs()
    return 0;
}


let newplaylist = ref('');
const addplaylist = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/playlist/${newplaylist.value}/${username}/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        });
        if (response.ok) {
            alert('Playlist and added successfully');
            fetchPlaylists();
        } else {
            alert('Failed to add playlist');
        }
    } catch (error) {
        console.error('Error adding playlist:', error);
    }
}


const selpl = ref('');
const selectedPls = (event) => {
    if (event.target.value != 'Choose Playlist') {
        selpl.value = event.target.value;
    }
}

const addexplaylist = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/playlist/${selpl.value}/${username}/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        });
        if (response.ok) {
            alert('Song added to playlist successfully');
            fetchPlaylists();
        } else {
            alert('Failed to add song to playlist');
        }
    } catch (error) {
        console.error('Error adding song to playlist:', error);
    }
}


const fetchPlaylists = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/playlist/${username}`, {
            method: 'GET',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        })
        const data = await response.json()
        if (response.ok) {
            playlists.value = data.map(playlist => ({
                id: playlist.id,
                name: playlist.name,
                songs: playlist.songs,
            }))
            const chunkSize = 5;
            for (let i = 0; i < playlists.value.length; i += chunkSize) {
                playlistGroups.value.push(playlists.value.slice(i, i + chunkSize));
            }
            if (playlists.value.length > 0) {
                ifplaylist.value = true;
            }
        } else {
            console.error('Failed to fetch playlists:', response.statusText);
        }
    }
    catch (error) {
        console.error('Error fetching playlists:', error);
    }
}
const fetchAlbums = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/albums?alt', {
            method: 'GET',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        })
        const data = await response.json()

        if (response.ok) {
            albums.value = data.map(album => ({
                id: album.id,
                name: album.name,
                year: album.year,
                genre: album.genre,
                artist: album.artist
            }))
            const chunkSize = 5;
            for (let i = 0; i < albums.value.length; i += chunkSize) {
                albumGroups.value.push(albums.value.slice(i, i + chunkSize));
            }
        } else {
            console.error('Failed to fetch albums:', response.statusText);
        }
    }
    catch (error) {
        console.error('Error fetching albums:', error);
    }
}

const fetchsongs = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/songs', {
            method: 'GET',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        })
        const data = await response.json()
        if (response.ok) {
            if (data.length == 0) {
                songs.value = []
            }
            else {
                songs.value = data.map(song => ({
                    id: song.id,
                    title: song.Songname,
                    year: song.Year,
                    genre: song.Genre,
                    album: song.Album,
                    artist: song.Artist,
                    rating: ref(song.Ratings),
                    lyrics: song.Lyrics,
                    image: song.Album_art,
                    audio: song.Song_location,
                    flagged: song.flagged
                })).filter(song => song.flagged == false);
                const chunkSize = 5;
                for (let i = 0; i < songs.value.length; i += chunkSize) {
                    songGroups.value.push(songs.value.slice(i, i + chunkSize));
                }
            }
        }
    }
    catch (error) {
        console.error('Error fetching songs:', error);
    }
}

onMounted(async () => {
    await fetchsongs();
    await fetchAlbums();
    await fetchPlaylists();
});


const handleSearchQuery = (query) => {
    sq.value = query;
    filteredItems();
    console.log('Search query:', query);
}

let filteredSongs = ref([]);
let filteredAlbums = ref([]);
let filteredPlaylists = ref([]);

const filteredItems = () => {
    const searchQuery = sq.value.toLowerCase();
    const tempFilteredSongs = songs.value.filter(song =>
        song.title.toLowerCase().includes(searchQuery) ||
        song.artist.toLowerCase().includes(searchQuery) ||
        song.rating.toString().includes(searchQuery)
    );

    const tempFilteredAlbums = albums.value.filter(album =>
        album.name.toLowerCase().includes(searchQuery) ||
        album.artist.toLowerCase().includes(searchQuery) ||
        album.genre.toLowerCase().includes(searchQuery)
    );

    const tempFilteredPlaylists = playlists.value.filter(playlist =>
        playlist.name.toLowerCase().includes(searchQuery)
    );

    filteredSongs.value = chunkArray(tempFilteredSongs, 5);
    filteredAlbums.value = chunkArray(tempFilteredAlbums, 5);
    filteredPlaylists.value = chunkArray(tempFilteredPlaylists, 5);
}


const chunkArray = (arr, size) => {
    const chunkedArr = [];
    for (let i = 0; i < arr.length; i += size) {
        chunkedArr.push(arr.slice(i, i + size));
    }
    return chunkedArr;
}

const hover = ref([]);
</script>

<template>
    <div class="mb-3">
        <Navbar :roles="roles" :username="username" @searchAttribute="handleSearchQuery" />
    </div>
    <div v-if="sq == ''" style="height:100%;" class="mb-5">
        <div id="musiccont1">
            <div class="m-3">
                <h4><img src="../assets/sparkpost.svg"> Recently Added</h4>
                <hr>
            </div>
            <div id="songCarousel" class="carousel slide">
                <div class="carousel-inner" style="padding-left: 6%;padding-right: 6%;">
                    <div v-for="(group, index) in songGroups" :key="index"
                        :class="{ 'carousel-item': true, 'active': index === 0 }">
                        <div class="row row-cols-1 row-cols-md-3 row-cols-lg-5 g-4">
                            <div v-for="(song, songIndex) in group" :key="songIndex" class="col">
                                <div class="card" :id="`cv${songIndex}`" style="width: 15rem;"
                                    @mouseenter="hover[songIndex] = true" @mouseleave="hover[songIndex] = false">
                                    <div class="container">
                                        <img :src="getAlbumart(song.album)" class="card-img-top" :alt="song.title">
                                        <button class="btn btb rounded-circle" v-if="hover[songIndex]"
                                            data-bs-toggle="modal1" @click="getSong(song.title, song.album, song)"><img
                                                src="../assets/play.svg"></button>
                                    </div>
                                    <div class="card-body d-flex flex-column justify-content-between">
                                        <div class="d-flex justify-content-between">
                                            <span>
                                                <h5 class="card-title">{{ song.title }}</h5>
                                                <p class="card-text" style="font-size: small;">{{ song.artist }} - {{
            song.year }}
                                                </p>
                                            </span>
                                            <span v-if="currsong == ''">
                                                <p>{{ song.rating }}⭐</p>
                                            </span>
                                            <span v-else-if="currsong == song.title">
                                                <p>{{ rating }}⭐</p>
                                            </span>
                                        </div>
                                        <div class="row p-2">
                                            <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                                :data-bs-target="'#exampleModal' + song.id">
                                                + Playlist
                                            </button>
                                            <div class="modal fade" :id="'exampleModal' + song.id" tabindex="-1"
                                                aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h1 class="modal-title fs-5" id="exampleModalLabel">Add to
                                                                Playlist</h1>
                                                            <button type="button" class="btn-close"
                                                                data-bs-dismiss="modal" aria-label="Close"></button>
                                                        </div>
                                                        <div class="modal-body">
                                                            <div class="input-group mb-3">
                                                                <input type="text" class="form-control"
                                                                    placeholder="Playlist Name"
                                                                    :id="'playlist' + song.id"
                                                                    aria-label="Playlist Name"
                                                                    :aria-describedby="'button-addon' + song.id"
                                                                    v-model="newplaylist">
                                                                <button class="btn btn-outline-secondary" type="button"
                                                                    :id="'button-addon' + song.id"
                                                                    @click.prevent="addplaylist(song.id)">Create</button>
                                                            </div>
                                                            <p>Or....</p>
                                                            <div class="list-group mb-3">
                                                                <select class="form-select mb-3"
                                                                    :aria-describedby="'button-addon2' + song.id"
                                                                    aria-label="Default select example"
                                                                    @change="selectedPls($event)">
                                                                    <option selected>Choose Playlist</option>
                                                                    <option v-for="playlist in playlists"
                                                                        :key="playlist.id" :value="playlist.name">{{
            playlist.name }}</option>
                                                                </select>
                                                                <button class="btn btn-outline-secondary" type="button"
                                                                    :id="'button-addon3' + song.id"
                                                                    @click.prevent="addexplaylist(song.id)">Add to
                                                                    existing playlist</button>
                                                            </div>
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary"
                                                                data-bs-dismiss="modal"
                                                                @click="window.location.reload()">Close</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#songCarousel" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#songCarousel" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
        </div>
        <div id="musiccont2">
            <div class="m-3">
                <h4><img src="../assets/sparkpost.svg"> Albums</h4>
                <hr>
            </div>
            <div id="albumCarousel" class="carousel slide">
                <div class="carousel-inner" style="padding-left: 6%;padding-right: 6%;">
                    <div v-for="(group, index) in albumGroups" :key="index"
                        :class="{ 'carousel-item': true, 'active': index === 0 }">
                        <div class="row row-cols-1 row-cols-md-3 row-cols-lg-5 g-4">
                            <div v-for="(album, albumIndex) in group" :key="albumIndex" class="col">
                                <div class="card" :id="`cv${albumIndex}`" style="width: 14rem;"
                                    @mouseenter="hover[albumIndex] = true" @mouseleave="hover[albumIndex] = false">
                                    <div class="container">
                                        <img :src="getAlbumart(album.name)" class="card-img-top" :alt="album.name">
                                    </div>
                                    <div class="card-body d-flex justify-content-between">
                                        <div>
                                            <h5 class="card-title
                                        ">{{ album.name }}</h5>
                                            <p class="card-text" style="font-size: small;">{{ album.artist
                                                }}-{{ album.year }}
                                            </p>
                                            <button class="btn btn-primary"
                                                @click="router.push({ name: 'albums', query: { data: album.id } })">Explore
                                                This Album</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#albumCarousel"
                    data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#albumCarousel"
                    data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
        </div>
        <div id="musicConst3" v-if="ifplaylist">
            <div class="m-3">
                <h4><img src="../assets/sparkpost.svg"> Playlists</h4>
                <hr>
            </div>
            <div id="playlistCarousel" class="carousel slide">
                <div class="carousel-inner" style="padding-left: 6%;padding-right: 6%;">
                    <div v-for="(group, index) in playlistGroups" :key="index"
                        :class="{ 'carousel-item': true, 'active': index === 0 }">
                        <div class="row row-cols-1 row-cols-md-3 row-cols-lg-5 g-4">
                            <div v-for="(playlist, playlistIndex) in group" :key="playlistIndex" class="col">
                                <div class="card" :id="`cv${playlistIndex}`" style="width: 14rem;">
                                    <div class="container">
                                        <img src="../assets/playlist.jpeg" class="card-img-top" :alt="playlist.name">
                                    </div>
                                    <div class="card-body d-flex justify-content-between">
                                        <div>
                                            <h5 class="card-title">{{ playlist.name }}</h5>
                                            <p class="card-text" style="font-size: small;">{{ playlist.songs.length }}
                                                songs
                                            </p>
                                            <button class="btn btn-primary"
                                                @click="router.push({ name: 'allplaylists', query: { data: playlist.id } })">Explore
                                                This Playlist</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <button class="carousel-control-prev" type="button" data-bs-target="#playlistCarousel"
                    data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#playlistCarousel"
                    data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
        </div>
        <div v-if="currsong != ''">
            <div class="sticky-audio-player" style="height:7rem;max-height: 7rem;margin: 0%; ">
                <div class="container" style="padding: 2%;">
                    <div class="row">
                        <div class="col-md-1 ">
                            <img :src="curralbum" alt="Album Cover" class="img-fluid"
                                style="height: 60px; width: 60px;">
                        </div>
                        <div class="col-md-2">
                            <h5>{{ currsong }}</h5>
                            <p style="font-size: small;">{{ currartist }}</p>
                        </div>
                        <div class="col-md-5">
                            <audio controls autoplay controlslist="nodownload noplaybackrate" style="width: 100%;"
                                :src="curraudio" type="audio/mp3">
                                Your browser does not support the audio element.
                            </audio>
                        </div>
                        <div class="col-md-2 d-flex flex-row p-3">
                            <p class="row" style="margin-right: 1%;">Rate this Song : </p>
                            <span style="margin:1%;">
                                <span :class="{ 'fa': true, 'fa-star': true, 'checked': isChecked1 }"
                                    @click="rate(1)"></span>
                                <span :class="{ 'fa': true, 'fa-star': true, 'checked': isChecked2 }"
                                    @click="rate(2)"></span>
                                <span :class="{ 'fa': true, 'fa-star': true, 'checked': isChecked3 }"
                                    @click="rate(3)"></span>
                                <span :class="{ 'fa': true, 'fa-star': true, 'checked': isChecked4 }"
                                    @click="rate(4)"></span>
                                <span :class="{ 'fa': true, 'fa-star': true, 'checked': isChecked5 }"
                                    @click="rate(5)"></span>
                            </span>
                        </div>
                        <div class="col-md-2 p-2">
                            <!-- Button trigger modal -->
                            <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                data-bs-target="#exampleModal">
                                Read Lyrics
                            </button>

                            <!-- Modal -->
                            <div class="modal fade" id="exampleModal" tabindex="999" aria-labelledby="exampleModalLabel"
                                aria-hidden="true">
                                <div class="modal-dialog modal-dialog-scrollable">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h1 class="modal-title fs-5" id="exampleModalLabel" style="color: black;">
                                                Lyrics</h1>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <p style="white-space:pre;text-align: center;color: black;">{{ currlyrics }}
                                            </p>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary"
                                                data-bs-dismiss="modal">Close</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <button type="button" class="btn btn-close btn-close-white m-2"
                                @click="currsong = ''"></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-else style="height:100%;" class="mb-5">
        <div style="display: flex;justify-content: space-between">
            <h5 class="p-2">Search Results</h5>
            <button class="btn-close p-2 m-2" @click="sq = ''"></button>
        </div>
        <div id="musiccont1">
            <div class="m-3">
                <h4><img src="../assets/sparkpost.svg"> Songs containing word {{ sq }}</h4>
                <hr>
            </div>
            <div id="songCarousel" class="carousel slide">
                <div class="carousel-inner" style="padding-left: 6%;padding-right: 6%;">
                    <div v-for="(group, index) in filteredSongs" :key="index"
                        :class="{ 'carousel-item': true, 'active': index === 0 }">
                        <div class="row row-cols-1 row-cols-md-3 row-cols-lg-5 g-4">
                            <div v-for="(song, songIndex) in group" :key="songIndex" class="col">
                                <div class="card" :id="`cv${songIndex}`" style="width: 15rem;"
                                    @mouseenter="hover[songIndex] = true" @mouseleave="hover[songIndex] = false">
                                    <div class="container">
                                        <img :src="getAlbumart(song.album)" class="card-img-top" :alt="song.title">
                                        <button class="btn btb rounded-circle" v-if="hover[songIndex]"
                                            data-bs-toggle="modal1" @click="getSong(song.title, song.album, song)"><img
                                                src="../assets/play.svg"></button>
                                    </div>
                                    <div class="card-body d-flex flex-column justify-content-between">
                                        <div class="d-flex justify-content-between">
                                            <span>
                                                <h5 class="card-title">{{ song.title }}</h5>
                                                <p class="card-text" style="font-size: small;">{{ song.artist }} - {{
            song.year }}
                                                </p>
                                            </span>
                                            <span v-if="currsong == song.title">
                                                <p class="m-3">{{ rating }}⭐</p>
                                            </span>
                                            <span v-else>
                                                <p>{{ song.rating }}⭐</p>
                                            </span>
                                        </div>
                                        <div class="row p-2">
                                            <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                                :data-bs-target="'#exampleModal' + song.id">
                                                + Playlist
                                            </button>
                                            <div class="modal fade" :id="'exampleModal' + song.id" tabindex="-1"
                                                aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h1 class="modal-title fs-5" id="exampleModalLabel">Add to
                                                                Playlist</h1>
                                                            <button type="button" class="btn-close"
                                                                data-bs-dismiss="modal" aria-label="Close"></button>
                                                        </div>
                                                        <div class="modal-body">
                                                            <div class="input-group mb-3">
                                                                <input type="text" class="form-control"
                                                                    placeholder="Playlist Name"
                                                                    :id="'playlist' + song.id"
                                                                    aria-label="Playlist Name"
                                                                    :aria-describedby="'button-addon' + song.id"
                                                                    v-model="newplaylist">
                                                                <button class="btn btn-outline-secondary" type="button"
                                                                    :id="'button-addon' + song.id"
                                                                    @click.prevent="addplaylist(song.id)">Create</button>
                                                            </div>
                                                            <p>Or....</p>
                                                            <div class="list-group mb-3">
                                                                <select class="form-select mb-3"
                                                                    :aria-describedby="'button-addon2' + song.id"
                                                                    aria-label="Default select example"
                                                                    @change="selectedPls($event)">
                                                                    <option selected>Choose Playlist</option>
                                                                    <option v-for="playlist in playlists"
                                                                        :key="playlist.id" :value="playlist.name">{{
            playlist.name }}</option>
                                                                </select>
                                                                <button class="btn btn-outline-secondary" type="button"
                                                                    :id="'button-addon3' + song.id"
                                                                    @click.prevent="addexplaylist(song.id)">Add to
                                                                    existing playlist</button>
                                                            </div>
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary"
                                                                data-bs-dismiss="modal"
                                                                @click="window.location.reload()">Close</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#songCarousel" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#songCarousel" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
        </div>
        <div id="musiccont2">
            <div class="m-3">
                <h4><img src="../assets/sparkpost.svg"> Albums containing word {{ sq }}</h4>
                <hr>
            </div>
            <div id="albumCarousel" class="carousel slide">
                <div class="carousel-inner" style="padding-left: 6%;padding-right: 6%;">
                    <div v-for="(group, index) in filteredAlbums" :key="index"
                        :class="{ 'carousel-item': true, 'active': index === 0 }">
                        <div class="row row-cols-1 row-cols-md-3 row-cols-lg-5 g-4">
                            <div v-for="(album, albumIndex) in group" :key="albumIndex" class="col">
                                <div class="card" :id="`cv${albumIndex}`" style="width: 14rem;"
                                    @mouseenter="hover[albumIndex] = true" @mouseleave="hover[albumIndex] = false">
                                    <div class="container">
                                        <img :src="getAlbumart(album.name)" class="card-img-top" :alt="album.name">
                                    </div>
                                    <div class="card-body d-flex justify-content-between">
                                        <div>
                                            <h5 class="card-title
                                        ">{{ album.name }}</h5>
                                            <p class="card-text" style="font-size: small;">{{ album.artist
                                                }}-{{ album.year }}
                                            </p>
                                            <button class="btn btn-primary"
                                                @click="router.push({ name: 'albums', query: { data: album.id } })">Explore
                                                This Album</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#albumCarousel"
                    data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#albumCarousel"
                    data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
        </div>
        <div id="musicConst3" v-if="ifplaylist">
            <div class="m-3">
                <h4><img src="../assets/sparkpost.svg"> Playlists containing word {{ sq }}</h4>
                <hr>
            </div>
            <div id="playlistCarousel" class="carousel slide">
                <div class="carousel-inner" style="padding-left: 6%;padding-right: 6%;">
                    <div v-for="(group, index) in filteredPlaylists" :key="index"
                        :class="{ 'carousel-item': true, 'active': index === 0 }">
                        <div class="row row-cols-1 row-cols-md-3 row-cols-lg-5 g-4">
                            <div v-for="(playlist, playlistIndex) in group" :key="playlistIndex" class="col">
                                <div class="card" :id="`cv${playlistIndex}`" style="width: 14rem;">
                                    <div class="container">
                                        <img src="../assets/playlist.jpeg" class="card-img-top" :alt="playlist.name">
                                    </div>
                                    <div class="card-body d-flex justify-content-between">
                                        <div>
                                            <h5 class="card-title">{{ playlist.name }}</h5>
                                            <p class="card-text" style="font-size: small;">{{ playlist.songs.length }}
                                                songs
                                            </p>
                                            <button class="btn btn-primary"
                                                @click="router.push({ name: 'allplaylists', query: { data: playlist.id } })">Explore
                                                This Playlist</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <button class="carousel-control-prev" type="button" data-bs-target="#playlistCarousel"
                    data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#playlistCarousel"
                    data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
        </div>
        <div v-if="currsong != ''">
            <div class="sticky-audio-player" style="height:7rem;max-height: 7rem;margin: 0%; ">
                <div class="container" style="padding: 2%;">
                    <div class="row">
                        <div class="col-md-1 ">
                            <img :src="curralbum" alt="Album Cover" class="img-fluid"
                                style="height: 60px; width: 60px;">
                        </div>
                        <div class="col-md-2">
                            <h5>{{ currsong }}</h5>
                            <p style="font-size: small;">{{ currartist }}</p>
                        </div>
                        <div class="col-md-5">
                            <audio controls autoplay controlslist="nodownload noplaybackrate" style="width: 100%;"
                                :src="curraudio" type="audio/mp3">
                                Your browser does not support the audio element.
                            </audio>
                        </div>
                        <div class="col-md-2 d-flex flex-row p-3">
                            <p class="row" style="margin-right: 1%;">Rate this Song : </p>
                            <span style="margin:1%;">
                                <span :class="{ 'fa': true, 'fa-star': true, 'checked': isChecked1 }"
                                    @click="rate(1)"></span>
                                <span :class="{ 'fa': true, 'fa-star': true, 'checked': isChecked2 }"
                                    @click="rate(2)"></span>
                                <span :class="{ 'fa': true, 'fa-star': true, 'checked': isChecked3 }"
                                    @click="rate(3)"></span>
                                <span :class="{ 'fa': true, 'fa-star': true, 'checked': isChecked4 }"
                                    @click="rate(4)"></span>
                                <span :class="{ 'fa': true, 'fa-star': true, 'checked': isChecked5 }"
                                    @click="rate(5)"></span>
                            </span>
                        </div>
                        <div class="col-md-2 p-2">
                            <!-- Button trigger modal -->
                            <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                data-bs-target="#exampleModal">
                                Read Lyrics
                            </button>

                            <!-- Modal -->
                            <div class="modal fade" id="exampleModal" tabindex="999" aria-labelledby="exampleModalLabel"
                                aria-hidden="true">
                                <div class="modal-dialog modal-dialog-scrollable">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h1 class="modal-title fs-5" id="exampleModalLabel" style="color: black;">
                                                Lyrics</h1>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <p style="white-space:pre;text-align: center;color: black;">{{ currlyrics }}
                                            </p>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary"
                                                data-bs-dismiss="modal">Close</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <button type="button" class="btn btn-close btn-close-white m-2"
                                @click="currsong = ''"></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.sticky-audio-player {
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: #242424;
    color: #fff;
    z-index: 1051;
}

.carousel-control-next-icon,
.carousel-control-prev-icon {
    width: 1vw;
    height: 1vw;

}

.container .btb {
    position: absolute;
    top: 35%;
    left: 50%;
    transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    color: white;
    border: none;
    cursor: pointer;
}

.ig:hover {
    filter: blur(4px);
}

.btb {
    --bs-btn-active-border-color: #{shade-color($bd-violet, 54%)};
}

.carousel-control-prev,
.carousel-control-next {
    width: 2vw;
    background-color: black;
}

.checked {
    color: orange;
}

.carousel-control-prev:hover,
.carousel-control-next:hover {
    filter: invert(100%);
}

audio::-webkit-media-controls-panel {
    background-color: #242424;
}

audio::-webkit-media-controls-enclosure {
    border-radius: 0;
}

audio::-webkit-media-controls-play-button,
audio::-webkit-media-controls-pause-button,
audio::-webkit-media-controls-mute-button,
audio::-webkit-media-controls-timeline,
audio::-webkit-media-controls-current-time-display,
audio::-webkit-media-controls-panel-menu,
audio::-webkit-media-controls-time-remaining-display,
audio::-webkit-media-controls-volume-slider {
    filter: invert(100%);
}
</style>