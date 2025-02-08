<template>
  <div class="editable-text-field">
    <!-- Display Mode: Shows the current text and the "modify" button -->
    <div class="display-mode" v-if="!isEditing">
      <div class="field-content">
        <img v-if="imageUrl" :src="imageUrl" alt="Avatar" class="avatar" />
        <span class="text-value">{{ truncatedValue }}</span>
      </div>
      <button v-if="modifiable" class="edit-btn" @click="enableEditing">
        {{ $t("modify") }}
      </button>
    </div>

    <!-- Editing Mode: Shows the input field and a "save" button -->
    <div class="editing-mode" v-else>
      <input
        v-model="editableValue"
        :placeholder="placeholder"
        class="input-field"
        ref="inputField"
        maxlength="25"
        @keyup.enter="saveChanges"
      />
      <button class="save-btn" @click="saveChanges">
        {{ $t("save") }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "EditableTextField",
  props: {
    modelValue: String,
    placeholder: {
      type: String,
      default: ""
    },
    modifiable: {
      type: Boolean,
      default: false
    },
    imageUrl: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      isEditing: false,
      editableValue: this.modelValue
    };
  },
  computed: {
    // Truncate the displayed text to a maximum of 25 characters,
    // appending an ellipsis if necessary.
    truncatedValue() {
      if (this.modelValue && this.modelValue.length > 25) {
        return this.modelValue.substring(0, 25) + '...';
      }
      return this.modelValue;
    }
  },
  methods: {
    enableEditing() {
      if (this.modifiable) {
        this.isEditing = true;
        this.$nextTick(() => {
          this.$refs.inputField.focus();
        });
      }
    },
    saveChanges() {
      this.isEditing = false;
      // Update the v-model value
      this.$emit("update:modelValue", this.editableValue);
      // Emit an event to indicate that saving should occur
      this.$emit("save");
    }
  },
  watch: {
    modelValue(newValue) {
      this.editableValue = newValue;
    }
  }
};
</script>


<style scoped>
.editable-text-field {
  position: relative;
  width: 100%;
  min-height: 40px;
}

/* Display Mode Styles */
.display-mode {
  position: relative;
  width: 96%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 8px;
  background: var(--overlay-color);
}

/* Editing Mode Styles */
.editing-mode {
  display: flex;
  align-items: center;
}

/* Common Styles */
.field-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}

.text-value {
  font-style: italic;
  color: var(--text-color);
  font-size: 18px;
  padding: 10px;
}

.edit-btn,
.save-btn {
  background: none;
  color: var(--link-color);
  border: none;
  cursor: pointer;
  font-style: italic;
  margin-right: 10px;
}

.edit-btn:hover,
.save-btn:hover {
  text-decoration: underline;
}

.input-field {
  width: 100%;
  height: 100%;
  padding: 10px;
  background: var(--text-box-color);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  outline: none;
}
</style>
