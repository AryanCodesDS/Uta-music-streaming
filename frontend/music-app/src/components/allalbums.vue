<script setup>
import { onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import Navbar from './Navbar.vue';
const store = useStore()
let Album = ref({})
let route = useRoute()
let username = store.state.username
let roles = store.state.roles
let currsong = ref('');
let curraudio = ref('');
let curralbums = ref('');
let currartist = ref('');
let currlyrics = ref('');

const curralbum = route.query.data;
console.log(curralbum)

const getSong = (name, album, song) => {
  curralbums.value = getAlbumart(Album.value.name);
  currsong.value = song.name;
  currartist.value = Album.value.creator;
  currlyrics.value = song.lyrics;
  curraudio.value = `http://127.0.0.1:5000/api/song/${album}/${name}.mp3`;
  return 0;
}

const getAlbums = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:5000/customapi/album/${curralbum}`, {
      method: 'GET',
      type: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('authtoken'),
      },
    })
    const data = await response.json()
    Album.value = data
    console.log(Album.value)
  }
  catch (error) {
    console.error('Error fetching songs:', error);
  }
}

const getAlbumart = (name) => {
  return `http://127.0.0.1:5000/api/album-art/${name}/album_art.jpg`;
}


onMounted(async () => {
  await getAlbums()
})


</script>

<template>
  <div class="mb-3">
    <Navbar :roles="roles" :username="username" />
  </div>
  <div style="display:flex; justify-content: center; align-items: center;">
    <div class="card m-5">
      <div class="row">
        <div class="col-md-2">
          <img :src="getAlbumart(Album.name)" class="img-thumbnail rounded-start" alt="...">
        </div>
        <div class="col-md-3">
          <div class="card-body">
            <h5 class="card-title">Album Title : {{ Album.name }} </h5>
            <p class="card-text">
            <p class="text-body-secondary m-1">Year : {{ Album.year }}</p>
            <p class="text-body-secondary m-1 ">Artist : {{ Album.creator }}</p>
            <p class="text-body-secondary m-1">Genre : {{ Album.genre }}</p>
            </p>
          </div>
        </div>
        <div v-for="song in Album.songs" :key="song.id">
          <div class="card mb-3">
            <div class="card-body d-flex justify-content-between ">
              <div class="d-flex">
                <span>
                  <h5 class="card-title m-3">Title : {{ song.name
                    }}
                  </h5>
                  <p class=" m-3">Year : {{ song.year }}</p>
                </span>
                <span>
                  <p class="card-text m-3">
                    Rating : {{ song.ratings }}⭐
                  </p>
                  <p class=" m-3">Genre : {{ song.genre }}</p>
                </span>
              </div>
              <span class="m-3">
                <button class="btn btn-primary m-2" @click="getSong(song.name,Album.name, song)">
                  Play
                </button>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="currsong != ''">
    <div class="sticky-audio-player" style="height:7rem;max-height: 7rem;margin: 0%; ">
      <div class="container" style="padding: 2%;">
        <div class="row">
          <div class="col-md-1 ">
            <img :src="curralbums" alt="Album Cover" class="img-fluid" style="height: 60px; width: 60px;">
          </div>
          <div class="col-md-2">
            <h5>{{ currsong }}</h5>
            <p style="font-size: small;">{{ currartist }}</p>
          </div>
          <div class="col-md-6">
            <audio controls autoplay controlslist="nodownload noplaybackrate" style="width: 100%;" :src="curraudio"
              type="audio/mp3">
              Your browser does not support the audio element.
            </audio>
          </div>
          <div class="col-md-2 p-2">
            <!-- Button trigger modal -->
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
              Read Lyrics
            </button>

            <!-- Modal -->
            <div class="modal fade" id="exampleModal" tabindex="999" aria-labelledby="exampleModalLabel"
              aria-hidden="true">
              <div class="modal-dialog modal-dialog-scrollable">
                <div class="modal-content">
                  <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel" style="color: black;">Lyrics</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body">
                    <p style="white-space:pre;text-align: center;color: black;">{{ currlyrics }}</p>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                  </div>
                </div>
              </div>
            </div>
            <button type="button" class="btn btn-close btn-close-white m-2 " @click="currsong = ''"></button>
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
