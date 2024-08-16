<template>
  <div>
    <div class="flex items-center justify-center h-screen bg-black">
      <div
        class="text-center text-white p-6 border-2 border-white w-full max-w-md"
      >
        <h1 class="text-2xl mb-3">Upload Video</h1>

        <form @submit.prevent="uploadVideo" class="flex flex-col">
          <label class="mb-4 text-left text-stone-400">
            Video
            <input
              type="file"
              accept="video/*"
              @change="onFileChange"
              class="bg-gray-800 text-white w-full px-3 py-2 mt-2"
            />
          </label>

          <label class="mb-4 text-left text-stone-400">
            Interval
            <input
              v-model="interval"
              type="text"
              class="bg-gray-800 text-white w-full px-3 py-2 mt-2"
            />
          </label>

          <button type="submit" class="bg-white text-black px-6 py-2 mt-4">
            {{ isLoading ? "Loading..." : "Submit" }}
          </button>
          <p v-if="uploading" class="pt-3">Uploading...</p>
          <p v-if="uploadResponse" class="pt-3">{{ uploadResponse }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
definePageMeta({ layout: "default" });
const file = ref(null);
const interval = ref(0);
const isLoading = ref(false);
const uploading = ref(false);
const uploadResponse = ref("");

function onFileChange(event: any) {
  file.value = event.target.files[0];
}
async function uploadVideo() {
  if (!file.value) {
    uploadResponse.value = "Please select a file first.";
    return;
  }
  if (!interval?.value) {
    uploadResponse.value = "Please enter a valid integer value";
    return;
  }

  const formData = new FormData();
  formData.append("file", file.value);
  formData.append("interval", interval.value);

  uploading.value = true;
  uploadResponse.value = "";

  try {
    const response = await fetch(`http://localhost:8020/extract_frames`, {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    uploadResponse.value = result.message || "Upload successful!";
  } catch (error) {
    uploadResponse.value = "Upload failed!";
  } finally {
    uploading.value = false;
  }
}
</script>
