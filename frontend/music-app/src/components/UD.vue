<script setup>
import { onMounted, ref } from 'vue'
import { useStore } from 'vuex'
const store = useStore()
let Albums = ref([])
let showForm = ref(-1)
let showAlbumForm = ref(-1)
let username = store.state.username

const editedSong = ref({ name: '', genre: '', lyrics: '' })
const initialSong = ref(null)

const editedAlbum = ref({ name: '', year: '', genre: '' })
const initialAlbum = ref(null)

const editThisAlbum = (e, obj) => {
    editedAlbum.value = { ...obj }
    initialAlbum.value = { ...obj }
    showAlbumForm.value = e
}

const editThis = (e, obj) => {
    editedSong.value = { ...obj }
    initialSong.value = { ...obj }
    showForm.value = e
}

let setGenre = (id, e) => {
    console.log(e.target.value)
    editedSong.value.genre = e.target.value
}

let setalbumGenre = (id, e) => {
    console.log(e.target.value)
    editedAlbum.value.genre = e.target.value
}

const editAlbum = async (id) => {
    const updatedAlbum = { name: '', year: '', genre: '' }
    if (editedAlbum.value.name !== initialAlbum.value.name) {
        updatedAlbum.name = editedAlbum.value.name
    }
    if (editedAlbum.value.year !== initialAlbum.value.year) {
        updatedAlbum.year = editedAlbum.value.year
    }
    if (editedAlbum.value.genre !== initialAlbum.value.genre) {
        updatedAlbum.genre = editedAlbum.value.genre
    }

    console.log(updatedAlbum)
    const body = {
        new_album_name: updatedAlbum.name,
        albumyear: updatedAlbum.year,
        albumgenre: updatedAlbum.genre,
        album_id: id,
        username: store.state.username
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/albums/update", {
            method: 'PUT',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
            body: JSON.stringify(body)
        })
        const data = await response.json()
        if (response.ok) {
            console.log(data)
            alert(data.message)
            window.location.reload()
        }
        else {
            alert("Error updating album")
        }
    }
    catch (error) {
        console.error('Error updating album:', error);
    }
}

const editSong = async (id) => {

    const updatedSong = { name: '', genre: '', lyrics: '' }
    if (editedSong.value.name !== initialSong.value.name) {
        updatedSong.name = editedSong.value.name
    }
    if (editedSong.value.genre !== initialSong.value.genre) {
        updatedSong.genre = editedSong.value.genre
    }
    if (editedSong.value.lyrics !== initialSong.value.lyrics) {
        updatedSong.lyrics = editedSong.value.lyrics
    }

    console.log(updatedSong)
    const body = {
        new_song_name: updatedSong.name,
        genre: updatedSong.genre,
        lyrics: updatedSong.lyrics,
        albumid: showForm.value,
        song_id: id,
        username: store.state.username
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/songs/update", {
            method: 'PUT',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
            body: JSON.stringify(body)
        })
        const data = await response.json()
        if (response.ok) {
            console.log(data)
            alert(data.message)
            window.location.reload()
        }
        else {
            alert("Error updating song")
        }
    }
    catch (error) {
        console.error('Error updating song:', error);
    }
}


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
    const body = {
        song_id: id,
        username: store.state.username
    }
    try {
        const response = await fetch("http://127.0.0.1:5000/api/songs/delete", {
            method: 'DELETE',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
            body: JSON.stringify(body)
        })
        const data = await response.json()
        if (response.ok) {
            console.log(data)
            alert(data.message)
            window.location.reload()
        }
        else {
            alert("Error deleting song")
        }
    }
    catch (error) {
        console.error('Error deleting song:', error);
    }
}

const delAlbum = async (id) => {
    const body = {
        album_id: id,
        username: store.state.username
    }
    try {
        const response = await fetch("http://127.0.0.1:5000/api/albums/delete", {
            method: 'DELETE',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
            body: JSON.stringify(body)
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

const getAlbums = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/albums?alt=false&username=${username}`, {
            method: 'GET',
            type: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('authtoken'),
            },
        })
        const data = await response.json()
        Albums.value = data
        console.log(Albums.value)
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
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="custom-box">
                    <div class="box-header">
                        <h2 class="text-center">Your Albums</h2>
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
                                            <button class="btn btn-primary m-2" :id="'editAlb' + album.id"
                                                @click="editThisAlbum(album.id, album)">Edit</button>

                                            <button class="btn btn-primary m-2" :id="'delAlbum' + album.id"
                                                @click="delAlbum(album.id)">Delete
                                            </button>
                                            </p>
                                            <div :id="'editAlbumCard' + album.id"
                                                :class="{ 'edit-form': true, 'show': showAlbumForm === album.id }">
                                                <div class="card-body">
                                                    <form @submit.prevent="editAlbum(album.id)">
                                                        <div class="mb-3">
                                                            <label :for="'AlbumName' + album.id"
                                                                class="form-label">Album
                                                                Name</label>
                                                            <input type="text" class="form-control"
                                                                :id="'AlbumName' + album.id" v-model="editedAlbum.name">
                                                        </div>
                                                        <div class="form-floating mb-3">
                                                            <select class="form-select" :id="'songGenre' + album.id"
                                                                aria-label="Floating label select example" required
                                                                @change="setalbumGenre(album.id, $event)"
                                                                style="font-size:small;">
                                                                <option selected>
                                                                    None</option>
                                                                <option value="Pop">Pop</option>
                                                                <option value="Rock">Rock</option>
                                                                <option value="Jazz">Jazz</option>
                                                                <option value="Blues">Blues</option>
                                                                <option value="Country">Country</option>
                                                                <option value="Hip-Hop">Hip-Hop</option>
                                                                <option value="Rap">Rap</option>
                                                                <option value="Classical">Classical
                                                                </option>
                                                                <option value="Electronic">Electronic
                                                                </option>
                                                                <option value="Folk">Folk</option>
                                                                <option value="Reggae">Reggae</option>
                                                                <option value="Metal">Metal</option>
                                                                <option value="Punk">Punk</option>
                                                                <option value="Soul">Soul</option>
                                                                <option value="Techno">Techno</option>
                                                                <option value="Disco">Disco</option>
                                                                <option value="House">House</option>
                                                                <option value="Trance">Trance</option>
                                                            </select>
                                                            <label :for="'albumGenre' + album.id"
                                                                style="font-size: small;">Genre</label>

                                                        </div>

                                                        <div class="mb-3">
                                                            <label :for="'AlbumYear' + album.id"
                                                                class="form-label">Year</label>
                                                            <input type="number" class="form-control"
                                                                :id="'AlbumYear' + album.id" v-model="editedAlbum.year">
                                                        </div>
                                                        <button type="submit" class="btn btn-primary">Submit</button>
                                                    </form>
                                                </div>
                                            </div>
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
                                                                        @click="editThis(song.id, song)">Edit</button>

                                                                    <button class="btn btn-primary m-2"
                                                                        :id="'delSong' + song.id"
                                                                        @click="delSong(song.id)">Delete
                                                                    </button>
                                                                    <button type="button" class="btn-close m-2"
                                                                        aria-label="Close"
                                                                        @click="editThis(-1, song)"></button>

                                                                </span>
                                                            </div>
                                                            <div :id="'editCard' + song.id"
                                                                :class="{ 'edit-form': true, 'show': showForm === song.id }">

                                                                <div class="card-body">
                                                                    <form @submit.prevent="editSong(song.id)">
                                                                        <div class="mb-3">
                                                                            <label :for="'songName' + song.id"
                                                                                class="form-label">Song
                                                                                Name</label>
                                                                            <input type="text" class="form-control"
                                                                                :id="'songName' + song.id"
                                                                                v-model="editedSong.name">
                                                                        </div>
                                                                        <div class="form-floating mb-3">
                                                                            <select class="form-select"
                                                                                :id="'songGenre' + song.id"
                                                                                aria-label="Floating label select example"
                                                                                required
                                                                                @change="setGenre(song.id, $event)"
                                                                                style="font-size:small;">
                                                                                <option selected>
                                                                                    None</option>
                                                                                <option value="Pop">Pop</option>
                                                                                <option value="Rock">Rock</option>
                                                                                <option value="Jazz">Jazz</option>
                                                                                <option value="Blues">Blues</option>
                                                                                <option value="Country">Country</option>
                                                                                <option value="Hip-Hop">Hip-Hop</option>
                                                                                <option value="Rap">Rap</option>
                                                                                <option value="Classical">Classical
                                                                                </option>
                                                                                <option value="Electronic">Electronic
                                                                                </option>
                                                                                <option value="Folk">Folk</option>
                                                                                <option value="Reggae">Reggae</option>
                                                                                <option value="Metal">Metal</option>
                                                                                <option value="Punk">Punk</option>
                                                                                <option value="Soul">Soul</option>
                                                                                <option value="Techno">Techno</option>
                                                                                <option value="Disco">Disco</option>
                                                                                <option value="House">House</option>
                                                                                <option value="Trance">Trance</option>
                                                                            </select>
                                                                            <label :for="'songGenre' + song.id"
                                                                                style="font-size: small;">Genre</label>
                                                                        </div>

                                                                        <div class="mb-3">
                                                                            <label :for="'songLyrics' + song.id"
                                                                                class="form-label">Lyrics</label>
                                                                            <textarea class="form-control"
                                                                                :id="'songLyrics' + song.id"
                                                                                v-model="editedSong.lyrics"></textarea>
                                                                        </div>
                                                                        <button type="submit"
                                                                            class="btn btn-primary">Submit</button>
                                                                    </form>
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
