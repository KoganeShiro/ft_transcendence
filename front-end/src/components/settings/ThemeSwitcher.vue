<template>
  <div class="theme-switcher">
    <h2>{{ $t("choose-theme") }}</h2>
    <div class="theme-buttons">
      <ThemeButton
        v-for="(theme, index) in themes"
        :key="index"
        :themeName="theme.name"
        :imageUrl="theme.imageUrl"
        :isActive="theme.name.toLowerCase() === currentTheme.toLowerCase()"
        @select="switchTheme"
      />
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import ThemeButton from "@/components/settings/Themes.vue";
import ocean from "@/assets/ocean.webp";
import forest from "@/assets/forest.jpg";
import volcano from "@/assets/volcano.jpg";
import sun from "@/assets/sun.jpg";
import moon from "@/assets/moon.jpg";

export default {
  name: "ThemeSwitcher",
  components: {
    ThemeButton
  },
  data() {
    return {
      // Define your available themes
      themes: [
        { name: "Dark", imageUrl: moon },
        { name: "Light", imageUrl: sun },
        { name: "Ocean", imageUrl: ocean },
        { name: "Forest", imageUrl: forest },
        { name: "Volcano", imageUrl: volcano }
      ]
    };
  },
  computed: {
    ...mapGetters(["selectedTheme"]),
    currentTheme() {
      return this.selectedTheme;
    }
  },
  methods: {
    ...mapActions(["changeTheme"]),
    switchTheme(themeName) {
      if (themeName.toLowerCase() !== this.currentTheme.toLowerCase()) {
        this.changeTheme(themeName.toLowerCase());
        this.$emit("theme-changed", themeName);
      }
    }
  }
};
</script>

<style scoped>
.theme-switcher {
  text-align: center;
  margin-top: 20px;
}

.theme-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
  margin-top: 15px;
}
</style>
