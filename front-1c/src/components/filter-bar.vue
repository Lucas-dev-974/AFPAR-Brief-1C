<template>
    <div class="d-flex justify-space-between">
        <div>
            <v-btn :color="$store.state.on_graph == 'pays' ?     'blue' : '#005db7'" class="mx-1 my-1 text-white" size="small" @click='byRegions'>Ventes par pays</v-btn>      
            <v-btn :color="$store.state.on_graph == 'products' ? 'blue' : '#005db7'" class="mx-1 my-1 text-white" size="small" @click="byProducts">Ventes par produit</v-btn>
            <v-btn :color="$store.state.on_graph == 'regions_products' ? 'blue' : '#005db7'" class="mx-1 text-white" size="small" @click="byRegionsProducts">Ventes par régions des produits</v-btn>
        </div>

        <div class="d-flex w-50 align-center">
            <v-select style="max-width: 120px;" density="compact" label="Année" variant="outlined" v-model="year_model" :items="$store.state.year_select.years"></v-select>
            <v-text-field  style="max-width: 120px;" label="Nombre d'items" type="number" density='compact' v-model="nb_items" variant="outlined" class="mx-4"></v-text-field>
            <v-select variant="outlined" :items="$store.state.pays_select.pays" v-model="pays" :label="$store.state.on_graph" multiple density="compact" chips></v-select>

            <v-icon style="cursor: pointer" class="mb-5 mx-2" @click="search">mdi-magnify</v-icon>
        </div>
            
    </div>
</template>

<script src="./js/filter-bar.js"></script>