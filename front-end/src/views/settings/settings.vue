<template>
  <div class="settings-page">
    <HeaderOrganism />

    <div class="settings-body">
      <!-- Sidebar is always visible on desktop. On mobile, the Sidebar component handles its own toggle via the arrow. -->
      <Sidebar @page-selected="setPage" />

      <!-- Settings content area -->
      <div class="settings-content">
        <component :is="currentPage" />
      </div>
    </div>

    <FooterOrganism />
  </div>
</template>

<script>
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import Sidebar from "@/components/settings/Sidebar.vue";
import LanguagesPage from "@/components/settings/LanguageSwitcher.vue";
import AccountPage from "@/views/settings/account.vue";
import AppearancePage from "@/views/settings/appearence.vue";

export default {
  name: "SettingsPage",
  components: {
    HeaderOrganism,
    FooterOrganism,
    Sidebar,
    AccountPage,
    AppearancePage,
    LanguagesPage,
  },
  data() {
    return {
      currentPage: "AccountPage",
    };
  },
  methods: {
    setPage(page) {
      if (page === "Account") {
        this.currentPage = "AccountPage";
      } else if (page === "Appearance") {
        this.currentPage = "AppearancePage";
      } else if (page === "Languages") {
        this.currentPage = "LanguagesPage";
      }
    },
  },
};
</script>

<style scoped>
.settings-page {
  text-align: center;
  color: white;
  background-color: #222;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.settings-body {
  display: flex;
  flex: 1;
}

.settings-content {
  padding: 20px;
  color: white;
  font-size: 1.5rem;
  line-height: 1.5;
  flex-grow: 1;
}

/* Responsive styles for mobile */
@media (max-width: 668px) {
  .settings-body {
    flex-direction: column;
  }
  .settings-content {
    margin: 0;
    padding: 10px;
    align-items: center;
  }
}
</style>
