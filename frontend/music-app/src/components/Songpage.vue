<script setup>
import Navbar from './Navbar.vue'
import { useStore } from 'vuex'
import { reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router'
const store = useStore()
const router = useRouter()
const username = store.state.username
const roles = store.state.roles
let songs = new reactive([])
let songGroups = reactive([])
onMounted(async () => {
    try {
        const storedData = localStorage.getItem('songData');
        if (storedData) {
            const parsedData = JSON.parse(storedData);
            songs.value = parsedData.songs;
            songGroups.value = parsedData.songGroups;
        }
        else{
        const response = await fetch('http://127.0.0.1:5000/api/songs', {
            method: 'GET',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        })
        const data = await response.json()
        songs.value = data.map(song => ({
            title: song.Songname,
            album: song.Album,
        }))
        const chunkSize = 5;
        songGroups = [];
        for (let i = 0; i < songs.value.length; i += chunkSize) {
            songGroups.push(songs.value.slice(i, i + chunkSize));
        }
        localStorage.setItem('songData', JSON.stringify({ songs: songs.value, songGroups: songGroups }));
    }
    }
    catch (error) {
        console.error('Error fetching songs:', error);
    }
})
console.log(songs)
</script>

<template>
    <div class="mb-3">
        <Navbar :roles="roles" :username="username" />
    </div>
    <div class="m-3">
        <h3>Most Liked</h3>
    </div>
        <div id="songCarousel" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">
                <div v-for="(group, index) in songGroups.value" :key="index"
                    :class="{ 'carousel-item': true, 'active': index === 0 }">
                    <div class="row row-cols-1 row-cols-md-3 row-cols-lg-5 g-4">
                        <div v-for="(song, songIndex) in group" :key="songIndex" class="col">
                            <div class="card">
                                <img :src="'images/' + song.image" class="card-img-top" :alt="song.title">
                                <div class="card-body">
                                    <h5 class="card-title">{{ song.title }}</h5>
                                    <p class="card-text">Artist: {{ song.artist }}<br>Album: {{ song.album }}</p>
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
    <div class="sticky-audio-player">
        <div class="container">
            <div class="row">
                <div class="col-md-2">
                    <img src="https://via.placeholder.com/50" alt="Album Cover" class="img-fluid">
                </div>
                <div class="col-md-8">
                    <h5>Song Title</h5>
                    <p>Artist Name</p>
                </div>
                <div class="col-md-2">
                    <audio controls style="width: 100%;">
                        <source src="" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
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
    background-color: #333;
    color: #fff;
    padding: 10px;
    z-index: 1000;
}

.carousel-control-prev,
.carousel-control-next {
    color: #fff;
    background-color: #007bff;
    border-color: #007bff;
}

.carousel-control-prev:hover,
.carousel-control-next:hover {
    color: #fff;
    background-color: #0056b3;
    border-color: #0056b3;
}
</style>