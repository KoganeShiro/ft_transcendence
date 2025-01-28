<template>
  <div class="settings-page">
    <HeaderOrganism />

    <div class="settings-body">
      <Sidebar
        class="sidebar"
        @page-selected="setPage"
      />
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
      currentPage: 'AccountPage',
    };
  },
  methods: {
    setPage(page) {
      if (page === 'Account') {
        this.currentPage = 'AccountPage';
      } else if (page === 'Appearance') {
        this.currentPage = 'AppearancePage';
      } else if (page === 'Languages') {
        this.currentPage = 'LanguagesPage';
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
  line-height: 0.5;
  flex-grow: 0.5;
}

.sidebar {
  flex-shrink: 0;
}

@media (max-width: 668px) {
  .settings-content {
    margin: 0;
    padding: 0;
    max-width: none;
    align-items: center;
  }

  .settings-body {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }
}
</style>