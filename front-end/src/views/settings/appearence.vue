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
      // console.log("Theme changed to:", themeName);
      // Additional logic can be added here if needed.
    },
  },
};
</script>

<style scoped>
.appearence-content {
  margin: 50px auto;
  padding: 20px;
  max-width: 800px;
  color: var(--text-color);
  font-size: 1rem;
  line-height: 1.6;
}
</style>
