<template>
  <button :class="buttonClass" :style="buttonStyle" @click="onClick">
    <slot />
  </button>
</template>

<script>
export default {
  props: {
    variant: {
      type: String,
      default: "primary",
    },
    width: {
      type: String,
      default: null,
    },
    fontSize: {
      type: String,
      default: null,
    },
  },
  computed: {
    buttonClass() {
      return `btn-${this.variant}`;
    },
    buttonStyle() {
      const style = {};
      if (this.width && this.variant !== 'menu') {
        style.width = this.width;
      }
      if (this.fontSize) {
        style.fontSize = this.fontSize;
      }
      return style;
    },
  },
  methods: {
    onClick() {
      this.$emit("click");
    },
  },
};
</script>

<style scoped>
.btn-primary, .btn-secondary, .btn-ghost, .btn-menu {
  transition: all 0.3s ease;
}

.btn-primary:hover, .btn-secondary:hover, .btn-ghost:hover {
  opacity: 0.8;
}

.btn-menu:hover {
  background-color: #252424;
}

.btn-primary, .btn-secondary, .btn-ghost {
  width: auto;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  padding: auto;
  border-radius: 25px;
  cursor: pointer;
}

.btn-secondary {
  background-color: #6f42c1;
  color: white;
  border: none;
  padding: auto;
  border-radius: 25px;
  cursor: pointer;
}

.btn-ghost {
  background-color: transparent;
  color: white;
  border: none;
  padding: auto;
  border-radius: 10px;
  cursor: pointer;
}

.btn-menu {
  background-color: #3a3a3a;
  color: white;
  border: none;
  width: 100%;
  padding: auto;
  border-radius: 7px;
  cursor: pointer;
}
</style>