<template>
  <div class="twofa-component">
    <h3>{{ $t('twoFactorAuthentication') }}</h3>
    
    <div v-if="loading" class="loading">
      <p>{{ $t('loading') }}...</p>
    </div>
    
    <div v-else>
      <!-- When 2FA is enabled, show disable button with toggle -->
      <div v-if="is2faEnabled">
        <p>{{ $t('2faEnabled') }}</p>
        <div class="buttons-row">
          <TextField
            id="otp"
            v-model="otp"
            :label="$t('otp')"
            :placeholder="$t('enter-otp')"
          />
          <ButtonAtom 
            variant="primary" 
            @click="disable2FA"
            :width="'50%'">
            {{ $t('disable2fa') }}
          </ButtonAtom>
        </div>
        <!-- <div class="qr-section">
          <img :src="qrCode" alt="2FA QR Code" class="qr-code-image" />
        </div> -->
      </div>

      <!-- When 2FA is not enabled, show the activate button and enable flow -->
      <div v-else>
        <div v-if="qrCode">
          <p>{{ $t('scanQrCode') }}</p>
          <img :src="qrCode" alt="2FA QR Code" class="qr-code-image" />
          <TextField
            id="otp"
            v-model="otp"
            :label="$t('otp')"
            :placeholder="$t('enter-otp')"
          />
          <ButtonAtom 
            variant="primary" 
            @click="enable2FA"
            :width="'100%'">
            {{ $t('confirm') }}
          </ButtonAtom>
          <ButtonAtom 
            variant="secondary" 
            @click="resetSetup"
            :width="'100%'">
            {{ $t('cancel') }}
          </ButtonAtom>
        </div>
        <div v-else>
          <ButtonAtom 
            variant="primary" 
            @click="setup2FA"
            :width="'100%'">
            {{ $t('activate') }}
          </ButtonAtom>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import API from '@/api.js';
import TextField from "@/components/atoms/TextField.vue";
import ButtonAtom from "@/components/atoms/Button.vue";

export default {
  name: "2fa",
  components: {
    TextField,
    ButtonAtom
  },
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      qrCode: null,
      otp: "",
      loading: false,
      showQR: false
    };
  },
  computed: {
    is2faEnabled() {
      if (!this.user) return;
      // console.log("is2faEnabled:", this.user && this.user.mfa_enabled);
      return this.user && this.user.mfa_enabled;
    }
  },
  methods: {
    async setup2FA() {
      if (this.loading) return;
      this.loading = true;
      try {
        const response = await API.get("/api/setup_2fa/", { responseType: 'blob' });
        const reader = new FileReader();
        reader.onloadend = () => {
          this.qrCode = reader.result;
        };
        reader.readAsDataURL(response.data);
      } catch (error) {
        console.error("Error setting up 2FA:", error);
        alert(this.$t('error_setting_up_2fa'));
      } finally {
        this.loading = false;
      }
    },
    toggleQR() {
      if (this.loading) return;
      if (!this.showQR && !this.qrCode) {
        this.setup2FA();
      }
      this.showQR = !this.showQR;
      console.log("showQR:", this.showQR);
      return this.showQR;
    },
    async enable2FA() {
      if (!this.otp) {
        alert(this.$t('enter-otp'));
        return;
      }
      if (this.loading) return;
      this.loading = true;
      try {
        await API.post("/api/enable_2fa/", { otp: this.otp });
        console.log("2FA enabled successfully:", this.otp);
        this.$emit('update:mfa_enable', true);
        this.qrCode = null;
        this.otp = "";
        this.showQR = false;
        this.user.mfa_enabled = true;
      } catch (error) {
        console.error("Error enabling 2FA:", error);
        alert(this.$t('error_enabling_2fa'));
      } finally {
        this.loading = false;
      }
    },
    async disable2FA() {
      if (this.loading) return;
      this.loading = true;
      try {
        await API.post("/api/disable_2fa/", { otp: this.otp });
        this.$emit('update:mfa_enable', false);
        this.user.mfa_enabled = false;
      } catch (error) {
        console.error("Error disabling 2FA:", error);
        alert(this.$t('error_disabling_2fa'));
      } finally {
        this.loading = false;
      }
    },
    resetSetup() {
      this.qrCode = null;
      this.otp = "";
      this.showQR = false;
    }
  },
  mounted() {
    if (this.is2faEnabled) {
      this.setup2FA();
    }
  }
};
</script>

<style scoped>
.twofa-component {
  border-radius: 8px;
  margin: 30px 0;
  padding: 25px;
  font-family: 'Arial', sans-serif;
}

.twofa-title {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
}

.twofa-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
}

.button-container {
  width: 100%;
  max-width: 300px;
  margin-bottom: 20px;
}

.qr-section {
  border-radius: 8px;
  padding: 20px;
}

.qr-code-image {
  display: block;
  margin: 0 auto;
  max-width: 200px;
  border-radius: 4px;
  margin-bottom: 30px;
}

.setup-flow {
  width: 100%;
  max-width: 300px;
}

.instruction {
  font-size: 16px;
  color: #555;
  margin-bottom: 15px;
  text-align: center;
}

.otp-input {
  margin-bottom: 15px;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.activate-button {
  width: 100%;
  max-width: 300px;
}

@media (max-width: 480px) {
  .twofa-component {
    padding: 20px;
  }

  .twofa-title {
    font-size: 20px;
  }

  .qr-code-image {
    max-width: 150px;
  }
}
</style>
