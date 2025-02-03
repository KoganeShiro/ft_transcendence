<template>
    <div :class="wrapperClass">
      <label v-if="label" :for="id" :class="labelClass">{{ label }}</label>
      <input
        :id="id"
        :placeholder="placeholder"
        :class="inputClass"
        :style="inputStyle"
        @input="$emit('input', $event.target.value)"
      />
    </div>
  </template>
  
  <script>
  export default {
    props: {
      id: {
        type: String,
        default: "",
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
        default: "10px",
      },
      borderRadius: {
        type: String,
        default: "10px",
      },
      borderColor: {
        type: String,
        default: "#403F3F",
      },
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
        };
      },
    },
  };
  </script>
  
  <style scoped>
  .input-wrapper {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    line-height: 2.5;
    margin-bottom: 15px;
  }

  .input-label {
    font-size: 16px;
    font-weight: bold;
  }
  
  .input-field {
    font-size: 14px;
  }

  </style>
  