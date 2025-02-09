<template>
  <div class="account-card" v-if="!loading">
    <div class="header">
      <h1>{{ $t("account") }}</h1>
    </div>
    <div class="avatar-section">
      <EditableAvatar 
        :imageUrl="user.cover_photo" 
        :pseudo="user.name" 
        :showPseudo="false" 
        @image-changed="onAvatarChanged"
      />

    </div>
    <div class="form-section">
      <div class="field">
        <label>{{ $t("username") }}</label>
        <EditableTextField 
          v-model="user.name" 
          :modifiable="true" 
          placeholder="Enter your-new-username"
          @save="saveProfile"
        />
      </div>
      <div class="field">
        <label>{{ $t("password") }}</label>
        <EditableTextField 
          v-model="user.password" 
          :modifiable="true" 
          placeholder="Enter your-new-password" 
          @save="saveProfile"
        />
      </div>
    </div>
    <div class="button-section">
      <ButtonAtom 
        variant="attention" 
        @click="removeAccount"
        :width="'80%'"
        :fontSize="'1.2rem'"
      >
        {{ $t("delete-account") }}
      </ButtonAtom>
    </div>
  </div>
  <div v-else class="loading">
    <p>{{ $t("loading") }}...</p>
  </div>
</template>


<script>
import API from '@/api.js';
import EditableAvatar from "@/components/settings/ModifyAvatar.vue";
import EditableTextField from "@/components/atoms/ModifyInformations.vue";
import ButtonAtom from "@/components/atoms/Button.vue";

export default {
  name: "AccountCard",
  components: {
    EditableAvatar,
    EditableTextField,
    ButtonAtom,
  },
  data() {
    return {
      user: {
        name: "",
        password: "",
        avatar: "",
        cover_photo: "",
      },
      loading: false,
      is42: false,
      avatarFile: null,
    };
  },
  methods: {
    initAccount() {
      this.loading = true;
      API.get("/api/profile/")
        .then(response => {
          const data = response.data;
          this.user.name = data.username;
          this.user.cover_photo = data.cover_photo;
          this.user.password = "*************";
          this.is42 = data.is42;
        })
        .catch(error => {
          console.error("Error fetching account data:", error);
        })
        .finally(() => {
          this.loading = false;
        });
    },

    onAvatarChanged(file) {
      this.avatarFile = file;
      const temporaryURL = URL.createObjectURL(file);
      this.user.cover_photo = temporaryURL;
      this.saveProfile();
    },

    saveProfile() {
      if (this.is42) {
        alert(this.$t("42-account-cannot-be-modified"));
        return;
      }
      
      let request;
      
      if (this.avatarFile) {
        const formData = new FormData();
  
        formData.append("cover_photo", this.avatarFile);

        request = API.patch("/api/profile_update/", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        });
      } else {
        const payload = { username: this.user.name };
        
        if (this.user.password !== "*************") {
          const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?;&=.<>:|\-\/+()#])[A-Za-z\d@$!%*?;&=.<>:|\-\/+()#]{8,}$/;
          if (!regex.test(this.user.password)) {
            alert("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.");
            this.initAccount();
            return;
          }
          payload.password = this.user.password;
        }
        
        request = API.patch("/api/profile_update/", payload);
      }
      
      request.then(response => {
          console.log("Profile saved successfully:", response.data);
          this.initAccount();
          this.avatarFile = null;
      })
      .catch(error => {
          console.error("Error saving profile:", error);
          alert(this.$t("error_saving_profile"));
      });
    },



    removeAccount() {
      if (confirm(this.$t("delete-account-msg"))) {
        API.get("/api/delete_account")
          .then(response => {
            alert(this.$t("account-deleted-successfully"));
            this.$router.push("/");
          })
          .catch(error => {
            console.error("Error deleting account:", error);
            alert(this.$t("error-deleting-account"));
          });
      }
    },
  },
  mounted() {
    this.initAccount();
  },
};
</script>


<style scoped>
.account-card {
  max-width: 500px;
  margin: 40px auto;
  background: var(--card-color);
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.header h1 {
  margin-bottom: 20px;
  font-size: 2rem;
  border-bottom: 1px solid #44444434;
  padding-bottom: 10px;
  color: var(--text-color);
}

.avatar-section {
  display: flex;
  justify-content: center;
  margin-bottom: 25px;
}

.form-section {
  margin-bottom: 30px;
}

.field {
  margin-bottom: 20px;
  text-align: left;
}

.field label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: var(--text-color);
  font-size: 0.9rem;
}

.button-section {
  display: flex;
  flex-direction: column;
  padding: 10px;
  gap: 15px;
  align-items: center;
}

.loading {
  text-align: center;
  color: var(--text-color);
  font-size: 1.5rem;
  margin-top: 100px;
}
</style>
