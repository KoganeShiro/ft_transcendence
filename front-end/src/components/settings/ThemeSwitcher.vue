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
import { mapGetters } from "vuex";
import API from '@/api.js';
import ThemeButton from "@/components/settings/Themes.vue";
import ocean from "@/assets/ocean.webp";
import forest from "@/assets/forest.jpg";
import volcano from "@/assets/volcano.jpg";
import sun from "@/assets/sun.jpg";
import moon from "@/assets/moon.jpg";
import teapot from "@/assets/teapot.jpg";
import { useTheme } from '@/components/useTheme.js';

export default {
  name: "ThemeSwitcher",
  components: {
    ThemeButton
  },
  data() {
    return {
      themes: [
        { name: "Dark", imageUrl: moon },
        { name: "Light", imageUrl: sun },
        { name: "Ocean", imageUrl: ocean },
        { name: "Forest", imageUrl: forest },
        { name: "Volcano", imageUrl: volcano },
        { name: "Teapot", imageUrl: teapot }
      ]
    };
  },
  setup() {
    const { changeTheme } = useTheme();
    return {
      changeTheme
    };
  },
  computed: {
    ...mapGetters(["selectedTheme"]),
    currentTheme() {
      return this.selectedTheme;
    }
  },
  methods: {
    async switchTheme(themeName) {
      if (themeName.toLowerCase() !== this.currentTheme.toLowerCase()) {
        try {
          await API.patch('/api/profile_update/', { theme: themeName });
          this.changeTheme(themeName.toLowerCase());
          this.$emit("theme-changed", themeName);
        } catch (error) {
          console.error("Error updating theme:", error);
        }
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
