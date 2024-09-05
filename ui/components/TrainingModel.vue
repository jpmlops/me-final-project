<template>
    <div v-if="isOpen" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full">
        <h2 class="text-2xl font-semibold mb-4">{{ title }}</h2>
        <p class="mb-4">{{ content }}</p>
        <button @click="close" class="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600">
          Close
        </button>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  const props = defineProps({
    isOpen: Boolean,
    title: {
      type: String,
      default: 'Modal Title',
    },
    content: {
      type: String,
      default: 'This is the modal content.',
    },
  })
  
  const emit = defineEmits(['update:isOpen'])
  
  function close() {
    emit('update:isOpen', false)
  }
  </script>
  