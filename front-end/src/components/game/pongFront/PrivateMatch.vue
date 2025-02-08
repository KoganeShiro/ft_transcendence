<template>
  <div class="modal-overlay">
    <Card class="modal-card">
      <h2 class="modal-title">{{ $t('game-withfriend') }}</h2>
      <p class="modal-text">
        {{ $t('join-create-match') }}
      </p>
      
      <!-- Display generated code after creation -->
      <div v-if="generatedCode" class="created-match-code">
        <p>{{ $t('match-id') }}</p>
        <div class="code-display">
          <input 
            :value="generatedCode" 
            type="text" 
            readonly
            class="generated-code-input"
          />
          <button class="copy-btn" :class="{ copied: isCopied }" @click="copyToClipboard">{{ $t('copy') }}</button>
        </div>
      </div>

      <Button class="btn" variant="secondary" @click="createMatch">{{ $t('create-game') }}</Button>
      
      <div class="form-group">
        <input 
          v-model="matchCode" 
          type="text" 
          placeholder="Enter match code" 
          class="match-code-input"
        />
      </div>
      
      <Button class="btn" variant="primary" @click="joinMatch">{{ $t('join-game') }}</Button>
    </Card>
  </div>
</template>


<script>
import Card from "@/components/atoms/Card.vue";
import Button from "@/components/atoms/Button.vue";

export default {
  name: "MatchPopup",
  components: {
    Card,
    Button
  },
  data() {
    return {
      matchCode: "",
      generatedCode: "code-abcd-12345",
      isCopied: false, // Add this property to manage the copied state
    };
  },
  methods: {
    async createMatch() {
      try {
        // Simulate API call to create match
        const response = await fetch('/api/create-match', {
          method: 'POST'
        });
        const data = await response.json();
        
        // Store the generated code from backend
        this.generatedCode = data.code;
        console.log("Match created with code:", this.generatedCode);
        
        // Emit event with generated code
        this.$emit("match-selected", { 
          action: "create", 
          code: this.generatedCode 
        });
        //should go back to PongWithFriend.vue

      } catch (error) {
        console.error("Error creating match:", error);
        this.generatedCode = "";
      }
    },
    joinMatch() {
      if (!this.matchCode.trim()) {
        alert("Please enter a match code!");
        return;
      }
      //should send it to the back to see if the code is valid
      this.$emit("match-selected", { 
        action: "join", 
        code: this.matchCode 
      });
    },
    copyToClipboard() {
      const el = document.createElement('textarea');
      el.value = this.generatedCode;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);

      this.isCopied = true;
      setTimeout(() => {
        this.isCopied = false;
      }, 1000);
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.397);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}

.modal-card {
  width: 90%;
  max-width: 400px;
  padding: 20px;
  border-radius: 10px;
  color: #fff;
  text-align: center;
}

.modal-title {
  font-size: 1.8rem;
  margin-bottom: 10px;
}

.modal-text {
  font-size: 1rem;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.match-code-input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  margin-top: 25px;
}

.btn {
  padding: 10px;
  margin-bottom: 15px;
}

.created-match-code {
margin: 15px 0;
padding: 10px;
background-color: var(--background-light);
border-radius: 8px;
}

.code-display {
display: flex;
gap: 10px;
margin-top: 10px;
}

.generated-code-input {
flex: 1;
padding: 8px;
border: 1px solid #cccccc94;
border-radius: 4px;
background-color: var(--card-color);
color: white;
}

.copy-btn {
padding: 8px 15px;
background-color: #4CAF50;
color: white;
border: none;
border-radius: 4px;
cursor: pointer;
}

.copy-btn:hover {
background-color: #45a049;
}


.copy-btn.copied {
  animation: copied-animation 0.5s ease-in-out;
}

@keyframes copied-animation {
  0% { background-color: #4CAF50;}
  50% { background-color: #45a049; scale: 0.95;}
  100% { background-color: #4CAF50; }
}

@media (max-width: 768px) {
  .modal-card {
    height: 65%;
    width: 78%;
  }
}


</style>
