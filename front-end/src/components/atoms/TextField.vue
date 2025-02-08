<template>
  <div :class="wrapperClass">
    <label v-if="label" :for="id" :class="labelClass">{{ label }}</label>
    <div class="input-container">
      <input
        :id="id"
        :placeholder="placeholder"
        :class="inputClass"
        :style="inputStyle"
        :type="inputType"
        :value="modelValue" 
        @input="$emit('update:modelValue', $event.target.value)"
        maxlength="25"
      />
      <!-- Show the toggle icon if this is a password field -->
      <span 
        v-if="type === 'password'" 
        class="toggle-icon" 
        @click="toggleVisibility"
      >
        {{ visible ? '🐵' : '🙈'}}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    modelValue: {
      type: String,
      default: ""
    },
    id: {
      type: String,
      default: ""
    },
    type: {
      type: String,
      default: "text",
    },
    placeholder: {
      type: String,
      default: "Enter text...",
    },
    label: {
      type: String,
      default: "",
    },
    width: {
      type: String,
      default: "100%",
    },
    padding: {
      type: String,
      default: "12px",
    },
    borderRadius: {
      type: String,
      default: "8px",
    },
    borderColor: {
      type: String,
      default: "#ccc",
    },
  },
  data() {
    return {
      visible: false
    };
  },
  computed: {
    wrapperClass() {
      return "input-wrapper";
    },
    labelClass() {
      return "input-label";
    },
    inputClass() {
      return "input-field";
    },
    inputStyle() {
      return {
        width: this.width,
        padding: this.padding,
        borderRadius: this.borderRadius,
        borderWidth: "1px",
        borderStyle: "solid",
        borderColor: this.borderColor,
      };
    },
    inputType() {
      return this.type === "password" ? (this.visible ? "text" : "password") : this.type;
    }
  },
  methods: {
    toggleVisibility() {
      this.visible = !this.visible;
    }
  }
};
</script>

<style scoped>
.input-wrapper {
  display: flex;
  flex-direction: column;
  line-height: 2;
}

.input-label {
  font-size: 14px;
  font-weight: 600;
  text-align: left;
  margin-left: 15px;
  margin-bottom: 8px;
}

.input-container {
  position: relative;
  width: 100%;
  margin-bottom: 18px;
}

.input-field {
  width: 100%;
  padding: 12px 40px 12px 12px;
  font-size: 16px;
  border: 1px solid var(--border-color, #ccc);
  border-radius: var(--border-radius, 8px);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  outline: none;
  background-color: #fff;
}

.input-field:focus {
  border-color: var(--primary-color, #36A2EB);
  box-shadow: 0 0 5px rgba(54, 162, 235, 0.5);
}

.toggle-icon {
  position: absolute;
  top: 50%;
  right: 0px;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 1.4em;
  user-select: none;
}

@media (max-width: 700px) {
  .input-field {
    margin-right: 15px;
    margin-left: -5px;
  }
}

</style>
