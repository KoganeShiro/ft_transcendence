<template>
    <div class="editable-avatar">
      <div class="avatar" :class="{ 'pseudo-top': pseudoPosition === 'top' }">
        <template v-if="link">
          <a :href="link" target="_blank" rel="noopener noreferrer">
            <div class="avatar-image" @click="triggerFileInput">
              <img :src="currentImage" :alt="pseudo" />
              <div class="overlay">
                <span>Click to modify</span>
              </div>
            </div>
            <span v-if="showPseudo" class="pseudo">{{ pseudo }}</span>
          </a>
        </template>
        <template v-else>
          <div class="avatar-image" @click="triggerFileInput">
            <img :src="currentImage" :alt="pseudo" />
            <div class="overlay">
              <span>Click to modify</span>
            </div>
          </div>
          <span v-if="showPseudo" class="pseudo">{{ pseudo }}</span>
        </template>
      </div>
      <!-- Hidden file input that is triggered when the avatar image is clicked -->
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        @change="onFileChange"
        style="display: none;"
      />
    </div>
  </template>
  
  <script>
  import defaultAvatar from '@/assets/profile.png';
  
  export default {
    name: 'EditableAvatar',
    props: {
      imageUrl: {
        type: String,
        default: ''
      },
      pseudo: {
        type: String,
        default: 'Username42'
      },
      showPseudo: {
        type: Boolean,
        default: true
      },
      pseudoPosition: {
        type: String,
        default: 'bottom',
        validator: (value) => ['top', 'bottom', 'right'].includes(value)
      },
      link: {
        type: String,
        default: ''
      }
    },
    data() {
      return {
        // Initially, use the provided imageUrl or fallback to the default avatar.
        currentImage: this.imageUrl || defaultAvatar
      };
    },
    methods: {
      triggerFileInput() {
        // Programmatically open the file selection dialog.
        this.$refs.fileInput.click();
      },
      onFileChange(event) {
        const file = event.target.files[0];
        if (file) {
          // Use FileReader to load the image file and create a preview.
          const reader = new FileReader();
          reader.onload = (e) => {
            this.currentImage = e.target.result;
            // Emit an event with the file object so the parent component
            // can handle uploading or further processing.
            this.$emit('image-changed', file);
          };
          reader.readAsDataURL(file);
        }
      }
    },
    watch: {
      // If the imageUrl prop changes from the parent, update the displayed image.
      imageUrl(newUrl) {
        this.currentImage = newUrl || defaultAvatar;
      }
    }
  };
  </script>
  
  <style scoped>
  .avatar {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
  }
  
  .avatar a {
    text-decoration: none;
    color: inherit;
    display: flex;
    flex-direction: inherit;
    align-items: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .avatar a:hover {
    transform: translateY(-10px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .avatar-image {
    position: relative;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    overflow: hidden;
    transition: transform 0.3s ease;
  }
  
  .avatar-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .overlay {
    position: absolute;
    bottom: 30px;
    width: 100%;
    background: rgba(0, 0, 0, 0.6);
    color: white;
    padding: 5px 0;
    font-size: 0.9rem;
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  @media (hover: hover) {
    .avatar-image:hover .overlay {
      opacity: 1;
    }
  }
  
    @media (max-width: 600px) {
    .overlay {
      opacity: 1;
    }
    .avatar-image:hover .overlay {
      opacity: 1;
    }
  }
  
  .pseudo {
    margin-top: 10px;
    font-weight: bold;
  }
  
  .pseudo-top {
    flex-direction: column-reverse;
  }
  
  .pseudo-top .pseudo {
    margin-top: 0;
    margin-bottom: 10px;
  }
  
  .pseudo-right {
    flex-direction: row;
  }
  </style>
  