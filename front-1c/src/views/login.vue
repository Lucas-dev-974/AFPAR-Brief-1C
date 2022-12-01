<template>
    <main class="full-height d-flex align-center">
        <v-card color="dark" class="mx-auto w-50" elevation="10" variant='tonal' max-width="450px" min-width="350px">
            <v-card-title class="py-3"> 
                <h3 class="d-flex justify-center letter-space py-3">Connexion</h3>    
            </v-card-title>

            <div class="px-3 w-100">
                <v-text-field name="username" label="Nom d'utilisateur" id="username_field" v-model="username"></v-text-field>
                <v-text-field name="password" label="Mot de passe" id="password_field" v-model="password" type="password"></v-text-field>
            </div>

            <v-card-actions class="d-flex justify-end">
                <v-btn color="#005db7" variant="tonal" @click="login">Se connecter</v-btn>
            </v-card-actions>
        </v-card>
    </main>
</template>

<script src="./js/login.js"></script>