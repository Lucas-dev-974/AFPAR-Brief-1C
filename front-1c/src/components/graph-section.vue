<template>
    <main>
        <div class="d-flex justify-space-between">
            <div>
                <v-btn :color="on_graph == 'pays' ?     'blue' : '#005db7'" class="mx-1" size="x-small" @click='byRegions'>Ventes par pays</v-btn>      
                <v-btn :color="on_graph == 'products' ? 'blue' : '#005db7'" class="mx-1" size="x-small" @click="byProducts">Ventes par produit</v-btn>
                <v-btn :color="on_graph == 'regions_products' ? 'blue' : '#005db7'" class="mx-1" size="x-small" @click="byRegionsProducts">Ventes par régions des produits</v-btn>
            </div>

            <div class="d-flex w-50 align-center">
                <v-select      style="max-width: 120px;" density="compact" label="Année" variant="outlined" v-model="data_options.year" :items="years" ></v-select>
                <v-text-field  style="max-width: 120px;" label="Nombre d'items" type="number" density='compact' v-model="nb_items" variant="outlined" class="mx-4"></v-text-field>
                <v-select variant="outlined" :items="select.items" v-model="data_options.regions" :label="on_graph" multiple density="compact" chips></v-select>

                <v-icon style="cursor: pointer" class="mb-5 mx-2" @click="search">mdi-magnify</v-icon>
            </div>
                
        </div>
        
        <v-card variant="tonal" color='gray' class="pa-3 w-100 mx-auto d-flex" elevation="6">
            <div class="d-flex">
                <canvas ref="canvas" id="chart_container"></canvas>
            </div>
            
            <PieChart v-if='on_graph == "regions_products"' />
        </v-card>
    </main>
</template>

<script src="./js/graph-section.js"></script>