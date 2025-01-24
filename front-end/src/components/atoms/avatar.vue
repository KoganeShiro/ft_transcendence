<template>
    <div class="avatar" :class="{ 'pseudo-top': pseudoPosition === 'top' }">
      <div class="avatar-image">
        <img :src="avatarImage" :alt="pseudo" />
      </div>
      <span v-if="showPseudo" class="pseudo">{{ pseudo }}</span>
    </div>
  </template>
  
  <script>
  import defaultAvatar from '@/assets/profile.png';
  
  export default {
    name: 'AvatarAtom',
    props: {
      imageUrl: {
        type: String,
        default: ''
      },
      pseudo: {
        type: String,
        default: ''
      },
      showPseudo: {
        type: Boolean,
        default: true
      },
      pseudoPosition: {
        type: String,
        default: 'bottom',
        validator: (value) => ['top', 'bottom'].includes(value)
      }
    },
    computed: {
      avatarImage() {
        return (this.imageUrl || defaultAvatar);
      }
    }
  }
  </script>
  
  <style scoped>
  .avatar {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .avatar-image {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    overflow: hidden;
  }
  
  .avatar-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
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
  </style>
  