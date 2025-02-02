<template>
  <div id="app" :class="selectedTheme">
    <router-view />
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "App",
  computed: {
    ...mapGetters(["selectedTheme"])
  },
  watch: {
    selectedTheme(newTheme) {
      document.body.setAttribute("data-theme", newTheme);
    }
  },
  mounted() {
    document.body.setAttribute("data-theme", this.selectedTheme);
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  min-height: 100vh;
}

.footer-link {
  color: #00aaff;
  text-decoration: none;
}

.template {
  text-align: center;
  color: white;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

#app.dark {
  color: #ffffff;
  background-color: #222;
}

#app.light {
  color: #2c3e50;
  background-color: #ffffff;
}

#app.ocean {
  color: #ffffff;
  background-color: #1e3a5f;
}

#app.forest {
  color: #ffffff;
  background-color: #086108;
}

#app.volcano {
  color: #ffffff;
  background-color: #b22222;
}

#app.teapot {
  color: #ffffff;
  background-color: #8b4513;
}


/* Define CSS variables for each theme */
:root {
  --header-color: #3333;
  --background-color: #222;
  --text-color: #ffffff;
  --icon-color: #ffffff;
}

[data-theme="light"] {
  --header-color: #ffffff;
  --background-color: #ffffff;
  --text-color: #000000;
  --icon-color: #000000;
}

[data-theme="dark"] {
  --header-color: #000000;
  --background-color: #333333;
  --text-color: #ffffff;
  --icon-color: #ffffff;
}

[data-theme="ocean"] {
  --header-color: #000000;
  --background-color: #1e3a5f;
  --text-color: #ffffff;
  --icon-color: #ffffff;
}

[data-theme="forest"] {
  --header-color: #00932C;
  --footer-color: #00932C;
  --burger-btn-color: #00932C;
  --background-color: #086108;
  --link-color: #00aaff;
  --card-color: #00932C;
  --text-box-color: #00932C;
  --side-btn-color: #00932C;
  --text-color: #ffffff;
  --icon-color: #ffffff;
}

[data-theme="volcano"] {
  --header-color: #ffffff;
  --secondary-color: #000000;
  --background-color: #b22222;
  --text-color: #ffffff;
  --icon-color: #ffffff;
}

[data-theme="teapot"] {
  --header-color: #ffffff;
  --secondary-color: #000000;
  --background-color: #8b4513;
  --text-color: #ffffff;
  --icon-color: #ffffff;
}

body, html {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
</style>