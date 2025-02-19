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
          :menuItems="translatedMenuItems"
          :activeItem="activeTab"
          @update:activeItem="setActiveTab"
        />
      </div>

      <!-- Right section: Scrollable content -->
      <div class="content">
        <div v-if="activeTab === 'stats'" class="card">
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
import { useTheme } from '../components/useTheme';
import { useLanguage } from '../components/useLanguage';
import { useStore } from 'vuex';

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
      activeTab: localStorage.getItem('activeTab') || "stats",
      username: '',
      cover_photo: '',
    };
  },
  setup() {
    const store = useStore();
    const { changeTheme } = useTheme();
    const { changeLanguage } = useLanguage();

    return {
      store,
      changeTheme,
      changeLanguage,
    };
  },
  watch: {
    activeTab(newTab) {
      if (newTab === 'friends') {
        // this.fetchFriends();
        this.fetchFriendsInterval = setInterval(this.fetchFriends, 30000);
      } else {
        clearInterval(this.fetchFriendsInterval);
        this.fetchFriendsInterval = null;
      }
    }
  },
  computed: {
    translatedMenuItems() {
      return [
        { key: "stats", label: this.$t('stats'), route: "#stats" },
        { key: "history", label: this.$t('history'), route: "#history" },
        { key: "friends", label: this.$t('friends'), route: "#friends" },
      ];
    }
  },
  created() {
    this.getProfile();
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab || "stats";
      localStorage.setItem('activeTab', tab);
    },
    async getProfile() {
      try {
        const response = await API.get('/api/profile/');
        this.username = response.data.username;
        this.cover_photo = response.data.cover_photo;
        this.changeTheme(response.data.theme.toLowerCase());
        console.log('Theme:', response.data.theme.toLowerCase());
        const { changeLanguage } = useLanguage();
        changeLanguage(response.data.lang);
        console.log('Language:', response.data.lang);
      } catch (error) {
        console.error("Error fetching username:", error);
      }
    },
    async fetchFriends() {
      this.isLoading = true;
      await API.get('/api/friends/user_friends/')
        .then(response => {
          // Map the API response to your local friend structure.
          this.friends = response.data.map((friend, index) => ({
            id: index,
            name: friend.username,
            online: friend.online_status,
            blocked: friend.is_blocked,
          }));
        })
        .catch(error => {
          console.error("Error fetching friends:", error);
        })
        .finally(() => {
          this.isLoading = false;
        });
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