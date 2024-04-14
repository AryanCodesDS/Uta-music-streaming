<script setup>
import { onMounted, ref } from 'vue';
import Navbar from './Navbar.vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import UD from './UD.vue'

const store = useStore()
const router = useRouter()
let username = store.state.username
let roles = store.state.roles
let curruName = ref("User")
let currusongs = ref(0)
let currualbums = ref(0)
let currurates = ref(0)
let showForm1 = ref(false)
let showForm2 = ref(false)
let formpart = ref(false)
let Albums = ref([])
let upcount = ref(0)

let newalbum = ref('')
let albumid = ref(-1)
let songsup = ref([])
let newalyear = ref(0)
let albumArt = null
let albumgenre = ref('')

const getSongdata = (index) => {
  if (!songsup.value[index]) {
    songsup.value[index] = { name: '', genre: '', Lyrics: " ", file: null };
  }
  return songsup.value[index];
};


const submitForm = async () => {
  try {
    const formData = new FormData();
    for (let i = 1; i <= upcount.value; i++) {
      const song = getSongdata(i);
      console.log(song)
      formData.append(`songs[${i}][name]`, song.name);
      formData.append(`songs[${i}][genre]`, song.genre);
      formData.append(`songs[${i}][Lyrics]`, song.Lyrics);
      formData.append(`songs[${i}][file]`, song.file);
    }
    formData.append('albumid', albumid.value)
    formData.append('username', username)
    formData.append('upcount', upcount.value)

    let result = await fetch("http://127.0.0.1:5000/api/songs/add", {
      mode: "cors",
      method: "POST",
      headers: {
        'Authentication-Token': localStorage.getItem('authtoken'),
      },
      body: formData,
    });
    if (result.ok) {
      alert("Songs Added Succesfully")
      window.location.reload()
    }
    else {
      alert("Error Adding Songs")
    }
  } catch (e) {
    console.log("Loading Internally")
  }
}

const submitForm1 = async () => {
  try {
    const formData = new FormData();
    for (let i = 1; i <= upcount.value; i++) {
      const song = getSongdata(i);
      console.log(song)
      formData.append(`songs[${i}][name]`, song.name);
      formData.append(`songs[${i}][genre]`, song.genre);
      formData.append(`songs[${i}][Lyrics]`, song.Lyrics);
      formData.append(`songs[${i}][file]`, song.file);
    }
    formData.append('album_name', newalbum.value)
    formData.append('album_year', newalyear.value)
    formData.append('genre', albumgenre.value)
    formData.append('username', username)
    formData.append('album_art', albumArt)
    formData.append('upcount', upcount.value)

    let result = await fetch("http://127.0.0.1:5000/api/albums/add", {
      mode: "cors",
      method: "POST",
      headers: {
        'Authentication-Token': localStorage.getItem('authtoken'),
      },
      body: formData,
    });
    if (result.ok) {
      alert("Album Added Succesfully")
      window.location.reload()
    }
    else {
      alert("Error Adding Songs")
    }
  } catch (e) {
    console.log(e)
  }
}

const handleFile = (index, event) => {
  const file = event.target.files[0];
  if (file) {
    getSongdata(index).file = file;
  }
};

const handleimgFile = (event) => {
  const file = event.target.files[0];
  if (file && file.type == 'image/jpeg') {
    albumArt = file;
  }
  else {
    alert("Please Upload a .jpg file")
  }
};
const switchF = (num) => {
  if (num == 1) {
    if (showForm2.value == true) {
      showForm2.value = false
    }
    showForm1.value = !showForm1.value
  }
  else if (num == 2) {
    if (showForm1.value == true) {
      showForm1.value = false
    }
    showForm2.value = !showForm2.value
  }
}

const getAlbums = async () => {
  try {
    const resp = await fetch(`http://127.0.0.1:5000/api/albums?alt&username=${username}`, {
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

const getudet = async (uname) => {
  try {
    const resp = await fetch(`http://127.0.0.1:5000/profile/${uname}`, {
      method: 'GET',
      type: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('authtoken'),
      },
    })
    if (resp.ok) {
      const data = await resp.json()
      curruName.value = data.Name
      currusongs.value = data.Totalsongs
      currualbums.value = data.Totalalbums
      currurates.value = data.userrates
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
    await getudet(username)
    await getAlbums()
  } catch (e) {
    console.log(e)
  }
})

const getSelection = (k) => {
  albumid.value = k.target.value
}

const setGenre = (i, k) => {
  getSongdata(i).genre = k.target.value
}
const changeVal = (k) => {
  const opt = k.target.value
  if (opt == 1) {
    formpart.value = true
  }
  else if (opt == 2) {
    switchF(opt)
    formpart.value = false
  }
  else {
    formpart.value = false
  }
}


</script>
<template>
  <div class="mb-5">
    <Navbar :roles="roles" :username="username" />
    <div class="d-flex justify-content-center m-3">
      <p class="display-3"> Welcome {{ curruName }} </p>
    </div>
    <div class="p-4">
      <div class="container text-center">
        <div class="row">
          <div class="col border border-secondary m-2">
            <p class="fs-4 fst-italic">Your Songs</p>
            <p class="fs-5 fw-bold">{{ currusongs }}</p>
          </div>
          <div class="col border border-secondary m-2">
            <p class="fs-4 fst-italic">Your Albums</p>
            <p class="fs-5 fw-bold">{{ currualbums }}</p>
          </div>
          <div class="col border border-secondary m-2">
            <p class="fs-4 fst-italic">No. of Times Users Rated your songs</p>
            <p class="fs-5 fw-bold">{{ currurates }}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="d-flex justify-content-center flex-column p-4">
      <div class="mb-3 d-flex justify-content-center">
        <button type="button" class="btn btn-outline-success btn-lg m-2" @click="switchF(1)">Add Songs</button>
        <button type="button" class="btn btn-outline-success btn-lg m-2" @click="switchF(2)">Add Album</button>
      </div>
      <div v-show="showForm1" class="mb-3" style="display: flex; flex-direction:row; justify-content: center;">
        <form class="form-group" enctype="multipart/form-data" @submit.prevent="submitForm">
          <div class="form-floating m-3">
            <select class="form-select" id="floatingSelect" aria-label="Floating label select example"
              @change="changeVal($event)" style="font-size:14px;">
              <option selected>Do Nothing</option>
              <option value="1">Assign/Add to existing Album</option>
              <option value="2">Create a New Album and Add Songs</option>
            </select>
            <label for="floatingSelect" style="font-size: small;">Select an Option</label>
          </div>
          <p class="m-3" style="font-size: medium; font-style: italic;">*Each song must belong to an album.</p>
          <div v-if="formpart == true" style="width: 100%;">
            <div class="form-floating m-3">
              <select class="form-select" id="floatingSelect2" aria-label="Floating label select example" required
                @change="getSelection($event)" style="font-size: 14px;">
                <option selected>None</option>
                <option :value="albumli.id" v-for="albumli in Albums">{{ albumli.name }}</option>
              </select>
              <label for="floatingSelect2" style="font-size: small;">Select an Album</label>
            </div>
            <div class="form-floating m-3">
              <input type="number" class="form-control" id="floatingSelect3" placeholder="Example Song Count" max="10"
                v-model="upcount" required>
              <label for="floatingSelect3">No. of Songs to Add (Max 10 per request)</label>
            </div>
            <div v-for="i in upcount">
              <div class="m-3 d-flex flex-row">
                <div class="form-floating m-3">
                  <input type="text" class="form-control" :id="'floatingInput' + i" placeholder="Example Song Name"
                    v-model="getSongdata(i).name" required style="font-size: 14px;">
                  <label :for="'floatingInput' + i" style="font-size: small;">Song Name</label>
                </div>
                <div class="form-floating m-3">
                  <select class="form-select" id="floatingSelect3" aria-label="Floating label select example" required
                    @change="setGenre(i, $event)" style="font-size:small;">
                    <option selected>None</option>
                    <option value="Pop">Pop</option>
                    <option value="Rock">Rock</option>
                    <option value="Jazz">Jazz</option>
                    <option value="Blues">Blues</option>
                    <option value="Country">Country</option>
                    <option value="Hip-Hop">Hip-Hop</option>
                    <option value="Rap">Rap</option>
                    <option value="Classical">Classical</option>
                    <option value="Electronic">Electronic</option>
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
                  <label for="floatingSelect3" style="font-size: small;">Select a Genre</label>
                </div>
                <div class="form-floating m-3">
                  <textarea :id="'Lyrics' + i" class="form-control" rows="8" cols="20" wrap="hard"
                    aria-label="With textarea" v-model="getSongdata(i).Lyrics" style="font-size: small;"></textarea>
                  <label :for="'Lyrics' + 1" style="font-size: small;">Lyrics</label>
                </div>
                <div class="form-floating m-3">
                  <input type="file" class="form-control" :id="'floatingFile' + i" placeholder="Upload Song"
                    style="font-size:small;" @change="handleFile(i, $event)" accept="audio/mp3" required>
                  <label :for="'floatingFile' + i" style="font-size:small;">Upload Song File(.mp3 only)</label>
                </div>
              </div>
            </div>
            <span class="d-flex justify-content-center align-items-center flex-column">
              <button type="submit" class="btn btn-primary">
                Upload
              </button>
            </span>
          </div>
        </form>
      </div>
      <div v-show="showForm2" class="mb-3" style="display: flex; justify-content: center;">
        <form enctype="multipart/form-data" @submit.prevent="submitForm1">
          <div class="form-group input-group-lg p-5">
            <div class="form-floating mb-3">
              <input type="text" class="form-control" id="floatingInputAlbum" placeholder="Example Album Name"
                v-model="newalbum" required style="font-size: 14px;">
              <label for="floatingInputAlbum" style="font-size: small;">Album Name</label>
            </div>
            <div class="form-floating mb-3">
              <input type="text" class="form-control" id="floatingInputAlbumG" placeholder="Example Album Name"
                v-model="albumgenre" required style="font-size: 14px;">
              <label for="floatingInputAlbumG" style="font-size: small;">Album Genre</label>
            </div>
            <div class="form-floating mb-3">
              <input type="number" class="form-control " id="floatingInputYear" placeholder="Example Album Year"
                v-model="newalyear" required style="font-size: 14px;">
              <label for="floatingInputYear" style="font-size: small;">Album Year</label>
            </div>
            <div class="form-floating m-2">
              <input type="file" class="form-control" id="floatingFileArt" placeholder="Upload Song"
                style="font-size:small;" @change="handleimgFile($event)" accept="image/jpg" required>
              <label for="floatingFileArt" style="font-size:small;">Upload Album Art(.jpg only)</label>
            </div>
            <div class="form-floating mb-3">
              <input type="number" class="form-control" id="floatingSelect4" placeholder="Example Song Count" max="10"
                min="1" v-model="upcount" required>
              <label for="floatingSelect4" style="font-size: small;">No. of Songs(Max 10)</label>
            </div>
            <div v-for="i in upcount" class="mb-3 d-flex">
              <div class="form-floating m-2">
                <input type="text" class="form-control" :id="'floatingInput' + i" placeholder="Example Song Name"
                  v-model="getSongdata(i).name" required style="font-size: 14px;">
                <label :for="'floatingInput' + i" style="font-size: small;">Song Name</label>
              </div>
              <div class="form-floating m-2">
                <select class="form-select" id="floatingSelect3" aria-label="Floating label select example" required
                  @change="setGenre(i, $event)" style="font-size:small;">
                  <option selected>None</option>
                  <option value="Pop">Pop</option>
                  <option value="Rock">Rock</option>
                  <option value="Jazz">Jazz</option>
                  <option value="Blues">Blues</option>
                  <option value="Country">Country</option>
                  <option value="Hip-Hop">Hip-Hop</option>
                  <option value="Rap">Rap</option>
                  <option value="Classical">Classical</option>
                  <option value="Electronic">Electronic</option>
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
                <label for="floatingSelect3" style="font-size: small;">Genre</label>
              </div>
              <div class="form-floating m-2">
                <textarea :id="'Lyrics' + i" class="form-control" rows="8" cols="20" wrap="hard"
                  aria-label="With textarea" v-model="getSongdata(i).Lyrics" style="font-size: small;"></textarea>
                <label :for="'Lyrics' + 1" style="font-size: small;">Lyrics</label>
              </div>
              <div class="form-floating m-2">
                <input type="file" class="form-control" :id="'floatingFile' + i" placeholder="Upload Song"
                  style="font-size:small;" @change="handleFile(i, $event)" accept="audio/mp3" required>
                <label :for="'floatingFile' + i" style="font-size:small;">Upload Song File(.mp3 only)</label>
              </div>
            </div>
            <span class="d-flex justify-content-center align-items-center flex-column">
              <button type="submit" class="btn btn-primary">
                Upload
              </button>
            </span>
          </div>
        </form>
      </div>
    </div>
    <UD/>
  </div>
</template>
