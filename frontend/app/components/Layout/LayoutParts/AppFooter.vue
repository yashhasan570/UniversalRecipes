<template>
  <v-footer
    color="primary"
    padless
    app
  >
    <v-row
      justify="center"
      align="center"
      density="comfortable"
      no-gutters
    >
      <v-col
        class="py-2 text-center white--text"
        cols="12"
      >
        <v-btn
          color="white"
          icon
          href="https://github.com/universalrecipes-recipes/universalrecipes"
          target="_blank"
        >
          <v-icon>
            {{ $globals.icons.github }}
          </v-icon>
        </v-btn>
        {{ new Date().getFullYear() }} — <strong> UniversalRecipes </strong>
      </v-col>
    </v-row>
  </v-footer>
</template>
