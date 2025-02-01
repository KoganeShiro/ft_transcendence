<template>
    <div class="appearence-content">
      <h1>{{ $t("appearance") }}</h1>
      <ThemeSwitcher @theme-changed="onThemeChanged" />
    </div>
</template>

<script>
import ThemeSwitcher from "@/components/settings/ThemeSwitcher.vue";

export default {
  name: "AppearancePage",
  components: {
    ThemeSwitcher,
  },
  methods: {
    onThemeChanged(themeName) {
      // Here you can implement the logic to apply the new theme
      console.log("Theme changed to:", themeName);
      // For example, you could update a CSS variable or call an API to save the preference.
    },
  },
};
</script>

<style scoped>

.appearence-content {
  margin: 50px auto;
  padding: 20px;
  max-width: 800px;
  color: white;
  font-size: 1rem;
  line-height: 1.6;
}
</style>
