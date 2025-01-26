<template>
  <div class="template">
    <HeaderOrganism />
  <div class="profile-page">
    <!-- Sidebar with menu -->
    <PseudoSidebar
      :menuItems="menuItems"
      :activeItem="activeTab"
      @update:activeItem="setActiveTab"
    />

    <!-- Main content -->
    <router-view />
  </div>
  <FooterOrganism />
</div>
</template>

<script>
import PseudoSidebar from "@/components/profile/PseudoSidebar.vue";
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";

export default {
  components: {
    PseudoSidebar,
    HeaderOrganism,
    FooterOrganism,
  },
  data() {
    return {
      menuItems: [
        { key: "stats", label: "Stats", route: "/stats" },
        { key: "history", label: "History", route: "/history" },
        { key: "friends", label: "Friends", route: "/friends" },
      ],
    };
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab;
    },
  },
};
</script>
