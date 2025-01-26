<template>
  <div id="app" :class="$store.state.theme">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
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
  background-color: #222;
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

/* #app.blue a {
  color: #ffffff;
}

#app.red a {
  color: #ffffff;
}

#app.green a {
  color: #ffffff;
} */

body, html {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
</style>
