<template>
  <div class="logout-container">
    <Card class="logout-card">
      <h3 class="logout-title">Oh no 🥺</h3>
      <h3 class="logout-title">
        {{ $t("logout-msg") }}
      </h3>
      <Button variant="attention" class="logout-button" @click="onlogout">{{ $t("logout-confirm") }}</Button>
      <Button variant="42" class="logout-button" @click="ongoback">{{ $t("logout-cancel") }}</Button>
    </Card>
  </div>
</template>

<script>
import axios from 'axios';
import Card from "@/components/atoms/Card.vue";
import Button from "@/components/atoms/Button.vue";
import ButtonGroup from "@/components/atoms/ButtonGroup.vue";
import InputGroup from "@/components/atoms/TextFieldGroup.vue";

export default {
  components: {
    Card,
    Button,
    InputGroup,
    ButtonGroup,
  },
  methods: {
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    },
    async onlogout() {
      try {
        const refreshToken = this.getCookie('refresh');
        if (!refreshToken) {
          throw new Error('Refresh token not found');
        }

        // Call the API to remove the refresh cookie
        await axios.post('/api/logout/', { refresh: refreshToken }, {
          withCredentials: true,
        });

        // Clear the cookies
        document.cookie = 'access=; Max-Age=0; path=/';
        document.cookie = 'refresh=; Max-Age=0; path=/';

        // Redirect to the home page after successful logout
        this.$router.push("/");
      } catch (error) {
        console.error("Error during logout:", error);
        alert("Logout failed. Please try again.");
      }
    },
    ongoback() {
      this.$router.push("/profile");
    },
  },
};
</script>
  
  <style scoped>
  .logout-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .logout-card {
    width: 500px;
    border-radius: 12px;
    background-color: #252525;
    color: var(--text-color);
  }
  
  .logout-title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    line-height: 1;
  }
  
  .logout-button {
    margin-top: 3%;
    width: 100%;
    font-size: 20px;
    padding: 15px 0;
    border-radius: 8px;
  }
  
  .input-group {
    width: 95%;
    margin-bottom: 10%;
  }
  
  @media (max-width: 700px) {
    .logout-card {
      max-width: 60%;
    }
  
    .logout-title {
      font-size: 24px;
    }
  }
  </style>
  