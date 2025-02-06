<template>
  <button
    :class="['btn', buttonClass]"
    :style="buttonStyle"
    @click="onClick"
  >
    <slot />
  </button>
</template>

<script>
export default {
  props: {
    variant: {
      type: String,
      default: "primary", // Default button style
    },
    width: {
      type: String,
      default: null, // Optional custom width
    },
    fontSize: {
      type: String,
      default: null, // Optional custom font size
    },
    borderRadius: {
      type: String,
      default: "7px", // Default border radius
    },
  },
  computed: {
    buttonClass() {
      return `btn-${this.variant}`;
    },
    buttonStyle() {
      const style = {
        padding: this.padding,
        borderRadius: this.borderRadius,
        width: this.width || "auto",
        fontSize: this.fontSize || "inherit",
      };
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
/* Base Button Styles */
.btn {
  font-weight: bold;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

/* Primary Button */
.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

/* Secondary Button */
.btn-secondary {
  background-color: #6f42c1;
  color: white;
}

.btn-secondary:hover {
  background-color: #543294;
}

/* Ghost Button */
.btn-ghost {
  background-color: transparent;
  width: 150%;
}

.btn-ghost:hover {
  /* background-color: rgba(255, 255, 255, 0.1); */
  background-color: var(--sidebar-hoover-color);
}

/* Menu Button */
.btn-menu {
  background-color: var(--burger-btn-color);
  color: var(--text-color);
  width: 100%;
}

.btn-menu:hover {
  background-color: var(--burger-btn-hover-color);
  width: 100%;
}

.btn-sidebar {
  background-color: var(--pseudo-sidebar-color);
  color: var(--text-color);
}

.btn-sidebar:hover {
  background-color: var(--pseudo-sidebar-hoover-color);
  width: 100%;
  transform: scale(1.05);
}

/* 42 Theme Button */
.btn-42 {
  background-color: #131313;
  color: white;
}

.btn-42:hover {
  background-color: #000000;
}

/* Attention Button */
.btn-attention {
  background-color: var(--attention-btn);
  padding: 10px;
  color: white;
}

.btn-attention:hover {
  background-color: #313030c4;
}

.btn-lang {
  background-color: transparent;
  color: white;
  width: 520px;
}

.btn-lang:hover {
  /* background-color: #7e7e7e81; */
  background-color: var(--sidebar-hoover-color);
  transform: scale(1.05);
}

/* Disabled State */
.btn:disabled {
  background-color: #cccccc;
  color: #666666;
  cursor: not-allowed;
}
</style>