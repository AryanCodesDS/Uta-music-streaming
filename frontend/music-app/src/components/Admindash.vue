<script setup>
import { defineComponent, onMounted, ref } from 'vue';
import Navbar from './Navbar.vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);
const store = useStore()
const router = useRouter()
const Albums = ref([])
let username = store.state.username
let roles = store.state.roles
let currusongs = ref(0)
let currualbums = ref(0)
let currusers = ref(0)
let ccount = ref(0)
let gcount = ref(0)
let genre_song_count = ref({})
let barlabels = ref([])
let barGenrescount = ref([])


const PieCountChart = () => {
    const el = document.getElementById('pieChart').getContext('2d');
    new Chart(el, {
        type: 'pie',
        data: {
            labels: ['Creators', 'General Users'],
            datasets: [{
                label: 'User Count',
                data: [ccount.value, gcount.value],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                ],
                borderWidth: 1,
                hoverOffset: 4
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'User Count by Role',
                    color: 'black',
                    font: {
                        size: 15,   
                    }
                }
            }
        }
    })
}


const BarGenreChart = () => {
    const el = document.getElementById('barChart').getContext('2d');
    new Chart(el, {
        type: 'bar',
        data: {
            labels: barlabels.value,
            datasets: [{
                label: 'Genres',
                data: barGenrescount.value,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 205, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(201, 203, 207, 0.2)',
                    'rgba(254, 99, 132, 0.2)',
                    'rgba(65, 159, 64, 0.2)',
                    'rgba(255, 205, 69, 0.2)',
                    'rgba(95, 192, 192, 0.2)',
                    'rgba(33, 162, 235, 0.2)',
                    'rgba(150, 102, 254, 0.2)',
                    'rgba(199, 203, 207, 0.2)',
                    'rgba(133, 99, 132, 0.2)',
                    'rgba(155, 159, 64, 0.2)',
                    'rgba(205, 205, 86, 0.2)',

                ],
                borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(255, 159, 64)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(54, 162, 235)',
                    'rgb(153, 102, 255)',
                    'rgb(201, 203, 207)',
                    'rgb(254, 99, 132)',
                    'rgb(65, 159, 64)',
                    'rgb(255, 205, 69)',
                    'rgb(95, 192, 192)',
                    'rgb(33, 162, 235)',
                    'rgb(150, 102, 254)',
                    'rgb(199, 203, 207)',
                    'rgb(133, 99, 132)',
                    'rgb(155, 159, 64)',
                    'rgb(205, 205, 86)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Song Count by Genre',
                    color: 'black',
                    font: {
                        size: 15,
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Song Count',
                            color: 'black'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Genres',
                            color: 'black'
                        }
                    },
                }
            }
        }
    })
};


const flag = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/admin/flag/${id}`, {
            method: 'POST',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        }
        )
        const data = await response.json()
        if (response.ok) {
            console.log(data)
            alert("song status changed")
            window.location.reload()
        }
        else {
            console.log(JSON.stringify(body))
            alert("Error flagging song")
        }
    }
    catch (error) {
        console.error('Error flagging song:', error);
    }
}

const fetchStats = async () => {
    try {
        const response = await fetch("http://127.0.0.1:5000/app/stats", {
            method: 'GET',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        })
        const data = await response.json()
        if (response.ok) {
            currusongs.value = data.songs
            currualbums.value = data.albums
            currusers.value = data.users
            ccount.value = data.creators
            gcount.value = data.generals
            genre_song_count.value = { ...data.song_genre_count }

            barlabels.value = Object.keys(genre_song_count.value)
            barGenrescount.value = Object.values(genre_song_count.value)
            console.log(genre_song_count.value)
            BarGenreChart()
            PieCountChart()
        }
        else {
            console.log("loading")
        }
    }
    catch (error) {
        console.error('Error fetching stats:', error);
    }
}

const getAlbums = async () => {
    try {
        const resp = await fetch('http://127.0.0.1:5000/api/albums', {
            method: 'GET',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        })
        if (resp.ok) {
            const data = await resp.json()
            Albums.value = data
        }
        else {
            console.log("loading")
        }
    } catch (e) {
        console.log("Loading Internally")
    }
}

onMounted(async () => {
    try {
        await getAlbums()
        await fetchStats()
    } catch (e) {
        console.log(e)
    }
})

const playSong = (id) => {
    const audio = document.getElementById(id);
    console.log(id)
    if (audio.paused) {
        audio.play();
    } else {
        audio.pause();
    }
}

const delSong = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/admin/songs/delete/${id}`, {
            method: 'DELETE',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        })
        const data = await response.json()
        if (response.ok) {
            console.log(data)
            alert(data.message)
            window.location.reload()
        }
        else {
            console.log(JSON.stringify(body))
            alert("Error deleting song")
        }
    }
    catch (error) {
        console.error('Error deleting song:', error);
    }
}

const delAlbum = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/admin/albums/delete/${id}`, {
            method: 'DELETE',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        })
        const data = await response.json()
        if (response.ok) {
            console.log(data)
            alert(data.message)
            window.location.reload()
        }
        else {
            alert("Error deleting album")
        }
    }
    catch (error) {
        console.error('Error deleting album:', error);
    }
}

const getSongFile = (name, album) => {
    return `http://127.0.0.1:5000/api/song/${album}/${name}.mp3`;
}


const getAlbumart = (name) => {
    return `http://127.0.0.1:5000/api/album-art/${name}/album_art.jpg`;
}


</script>
<template>
    <div class="mb-5">
        <Navbar :roles="roles" :username="username" />
        <div class="d-flex justify-content-center m-3">
            <p class="display-5"> Welcome Admin </p>
        </div>
        <div class="p-3">
            <div class="container text-center">
                <div class="row">
                    <div class="col border border-secondary m-2">
                        <p class="fs-4 fst-italic">Total Songs</p>
                        <p class="fs-5 fw-bold">{{ currusongs }}</p>
                    </div>
                    <div class="col border border-secondary m-2">
                        <p class="fs-4 fst-italic">Total Albums</p>
                        <p class="fs-5 fw-bold">{{ currualbums }}</p>
                    </div>
                    <div class="col border border-secondary m-2">
                        <p class="fs-4 fst-italic">Total Users</p>
                        <p class="fs-5 fw-bold">{{ currusers - 1 }}</p>
                    </div>
                </div>
            </div>
            <div class="container text-center">
                <div class="row">
                    <div class="col border border-secondary m-2" style="max-height: 400px; max-width: 700px;">
                        <canvas class="p-1" id="barChart" height="150" width="200"></canvas>
                    </div>
                    <div class="col border border-secondary m-2 d-flex justify-content-center"
                        style="max-height: 400px;">
                        <canvas class="p-1" id="pieChart" height="150" width="200"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="custom-box">
                    <div class="box-header">
                        <h2 class="text-center"> Albums</h2>
                    </div>
                    <div class="box-content p-3">
                        <div v-for="album in Albums" :key="album.id">
                            <div class="card m-3" style=" max-width:60rem;">
                                <div class="row g-0">
                                    <div class="col-md-4">
                                        <img :src="getAlbumart(album.name)"
                                            class="img-fluid img-thumbnail rounded-start" alt="...">
                                    </div>
                                    <div class="col-md-8">
                                        <div class="card-body">
                                            <h5 class="card-title">Album Title : {{ album.name }} </h5>
                                            <p class="card-text">
                                            <p class="text-body-secondary m-1">Year : {{ album.year }}</p>
                                            <p class="text-body-secondary m-1 ">Artist : {{ album.artist }}</p>
                                            <p class="text-body-secondary m-1">Genre : {{ album.genre }}</p>
                                            <button class="btn btn-primary m-2" :id="'delAlbum' + album.id"
                                                @click="delAlbum(album.id)">Delete
                                            </button>
                                            </p>
                                        </div>
                                    </div>
                                    <div class="accordion accordion-flush" :id="'accordionFlushExample' + album.id">
                                        <div class="accordion-item">
                                            <h2 class="accordion-header">
                                                <button class="accordion-button collapsed" type="button"
                                                    data-bs-toggle="collapse"
                                                    :data-bs-target="'#flush-collapseOne' + album.id"
                                                    aria-expanded="false"
                                                    :aria-controls="'flush-collapseOne' + album.id">
                                                    Edit/Display Songs
                                                </button>
                                            </h2>
                                            <div :id="'flush-collapseOne' + album.id"
                                                class="accordion-collapse collapse"
                                                :data-bs-parent="'#accordionFlushExample' + album.id">
                                                <div class="accordion-body">
                                                    <div v-for="song in album.Songs">
                                                        <div class="card w-100 mb-3">
                                                            <div class="card-body d-flex justify-content-between ">
                                                                <div class="d-flex">
                                                                    <span>
                                                                        <h5 class="card-title m-3">Title : {{ song.Name
                                                                            }}
                                                                        </h5>
                                                                        <p class=" m-3">Year : {{ song.Year }}</p>
                                                                    </span>
                                                                    <span>
                                                                        <p class="card-text m-3">
                                                                            Rating : {{ song.Ratings }}⭐
                                                                        </p>
                                                                        <p class=" m-3">Genre : {{ song.Genre }}</p>
                                                                        <p class=" m-3">Flagged : {{ song.flagged }}</p>
                                                                    </span>
                                                                </div>
                                                                <span class="m-3">
                                                                    <button class="btn btn-primary m-2"
                                                                        @click="playSong('currAud' + song.id)">
                                                                        Play/Pause
                                                                        <audio :id="'currAud' + song.id"
                                                                            :src="getSongFile(song.Name, album.name)"></audio>
                                                                    </button>
                                                                    <button class="btn btn-primary m-2"
                                                                        :id="'currAudi' + song.id"
                                                                        @click="flag(song.id)">Flag/Unflag</button>

                                                                    <button class="btn btn-primary m-2"
                                                                        :id="'delSong' + song.id"
                                                                        @click="delSong(song.id)">Delete
                                                                    </button>
                                                                </span>
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
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.custom-box {
    border: 2px solid black;
    padding: 10px;

}

.box-header {
    background-color: #e9ecef;
    padding: 0%;
    border-bottom: 2px solid black;
}

.box-content {
    flex-grow: 1;
}

audio::-webkit-media-controls-enclosure {
    border-radius: 0;
}

.edit-form {
    display: none;
}

.edit-form.show {
    display: block;
}
</style>
