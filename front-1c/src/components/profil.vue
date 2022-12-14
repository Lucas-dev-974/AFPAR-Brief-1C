<template>
    <v-card class="d-flex justify-space-between pa-3" color="gray" variant="tonal" id="profil_card" elevation="6">
        <div id="user-informations">
            <div class="d-flex">
                <p style="width: 140px"> Nom d'utilisateur:</p>  {{$store.state.user.username}}
            </div>
            <div class="d-flex">
                <p style="width: 140px"> email:</p> {{$store.state.user.email}}
            </div>
        </div>

        <div class="mx-5 d-flex align-center">
            <v-btn color="red" @click="logout" size="small">déconnexion</v-btn>
        </div>
    </v-card>

</template>

<script src="./js/profil.js"></script>