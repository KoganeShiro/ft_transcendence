<template>
  <div class="editable-text-field">
    <!-- Gray Overlay (Shown when not editing) -->
    <div class="overlay" v-if="!isEditing">
      <div class="field-content">
        <img v-if="imageUrl" :src="imageUrl" alt="Avatar" class="avatar" />
        <span class="text-value">{{ modelValue }}</span>
      </div>
      <button v-if="modifiable" class="edit-btn" @click="enableEditing">Modify</button>
    </div>

    <!-- Editable Input Field (Shown when editing) -->
    <input
      v-if="isEditing"
      v-model="editableValue"
      :placeholder="placeholder"
      class="input-field"
      @blur="saveChanges"
      @keyup.enter="saveChanges"
      ref="inputField"
    />
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
      this.$emit("update:modelValue", this.editableValue);
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

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 96%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 8px;
  background: var(--overlay-color);
}

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

.edit-btn {
  background: none;
  color: var(--link-color);
  border: none;
  cursor: pointer;
  font-style: italic;
  margin-right: 10px;
}

.input-field {
  width: 100%;
  height: 100%;
  padding: 10px;
  /* background: #333; */
  background: var(--input-field-color);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  outline: none;
}
</style>
