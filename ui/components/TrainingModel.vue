<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full">
      <h2 class="text-2xl font-semibold mb-4">{{ title }}</h2>
      <p class="mb-4">{{ content }}</p>
      <div class="w-64">
        <label for="options" class="block text-sm font-medium text-gray-700"
          >Choose a model</label
        >
        <select
          id="options"
          name="options"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-white"
        >
          <option v-for="ml in mlModel" :key="ml" :value="ml">{{ ml }}</option>
        </select>
      </div>
      <button
        @click="close"
        class="bg-red-500 text-white py-2 px-4 mt-3 rounded hover:bg-red-600"
      >
        Close
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const mlModel = ref<string[]>([]);
const props = defineProps({
  isOpen: Boolean,
  title: {
    type: String,
    default: "Modal Title",
  },
  content: {
    type: String,
    default: "This is the modal content.",
  },
});

const emit = defineEmits(["update:isOpen"]);

function close() {
  emit("update:isOpen", false);
}

const fetchImages = async (): Promise<void> => {
  try {
    const response = await fetch(`http://localhost:8020/ml-model-list/`, {
      method: "GET",
    });
    const res = await response.json();
    const newImages: string[] = res.frames;
    console.log(newImages);
    mlModel.value.push(...newImages);
    console.log("img", mlModel.value[0]);
    // skip.value += limit;
  } catch (error) {
    console.error("Error fetching images:", error);
  }
};

onMounted(() => {
  fetchImages();
});
</script>
