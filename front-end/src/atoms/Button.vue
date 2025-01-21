<template>
    <button :class="buttonClass" @click="onClick">
      <slot />
    </button>
  </template>
  
  <script>
  export default {
    props: {
      variant: {
        type: String,
        default: "primary", // Options: primary, secondary, etc.
      },
    },
    computed: {
      buttonClass() {
        return `btn-${this.variant}`;
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
  .btn-primary {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
  .btn-secondary {
    background-color: #6f42c1;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
  .btn-ghost {
    background-color: transparent;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
  }
  </style>
  