<template>
  <div class="template">
    <HeaderOrganism />
    <div class="profile-page">
      <!-- Left section: Avatar + Sidebar -->
      <div class="left-section">
        <!-- Avatar + Username -->
        <div class="avatar-container">
          <AvatarComponent :pseudo="username" :imageUrl="cover_photo" />
        </div>

        <!-- Pseudo Sidebar -->
        <PseudoSidebar
          :menuItems="menuItems"
          :activeItem="activeTab"
          @update:activeItem="setActiveTab"
        />
      </div>

      <!-- Right section: Scrollable content -->
      <div class="content">
        <div v-if="activeTab === 'stats'" class="card">
          <!-- ProfileStats :json="jsonFile" -->
          <ProfileStats />
        </div>
        <div v-if="activeTab === 'history'" class="card">
          <ProfileHistory />
        </div>
        <div v-if="activeTab === 'friends'" class="card">
          <ProfileFriends />
        </div>
      </div>
    </div>

    <FooterOrganism />
  </div>
</template>

<script>
import API from '@/api.js';
import PseudoSidebar from "@/components/profile/PseudoSidebar.vue";
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import ProfileStats from "@/components/profile/Stats.vue";
import ProfileHistory from "@/components/profile/History.vue";
import ProfileFriends from "@/components/profile/Friends.vue";
import AvatarComponent from "@/components/atoms/Avatar.vue";

export default {
  components: {
    PseudoSidebar,
    HeaderOrganism,
    FooterOrganism,
    ProfileStats,
    ProfileHistory,
    ProfileFriends,
    AvatarComponent,
  },
  data() {
    return {
      menuItems: [
        { key: "stats", label: this.$t('stats'), route: "#stats" },
        { key: "history", label: this.$t('history'), route: "#history" },
        { key: "friends", label: this.$t('friends'), route: "#friends" },
      ],
      activeTab: "stats", // Default tab
      username: '',
      cover_photo: '',
    };
  },
  created() {
    this.getProfile();
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab;
    },
    async getProfile() {
      try {
        // add a variable at the end of profile (username)
        const response = await API.get('/api/profile/');
        this.username = response.data.username;
        this.cover_photo = response.data.cover_photo;
        // console.log(this.username);
        // console.log(this.cover_photo);
      } catch (error) {
        console.error("Error fetching username:", error);
      }
    },
  },
};
</script>


<style scoped>
/* General layout */
.profile-page {
  display: flex;
  position: sticky; 
  top: 0; 
  height: auto;
  min-height: 80vh;
  overflow: hidden;
}

/* Left section: Avatar + Sidebar */
.left-section {
  width: 20%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.avatar-container {
  margin-bottom: 20px;
}

.avatar-container {
  color: var(--text-color);
  font-size: 1.3rem;
  font-weight: bold;
}

/* Pseudo Sidebar */
.pseudo-sidebar {
  display: flex;
  justify-content: center;
  width: 100%;
}

.pseudo-sidebar > * {
  margin: 0 10px;
}

/* Right section: Scrollable content */
.content {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto;
  margin-right: 20px;
}

.card {
  background-color: var(--card-color);
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
  margin-right: 15px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .profile-page {
    flex-direction: column;
    position: relative; 
  }

  .card {
    margin-left: 20px;
    width: 90%;
  }

  .left-section {
    width: 100%;
    flex-direction: column;
    align-items: center;
    padding: 10px;
  }

  .content {
    padding: 10px;
    margin-right: 0;
  }
  .pseudo-sidebar {
    margin-right: 15px;
  }
}
</style>