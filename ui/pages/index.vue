<template>  
  <div class="py-[60px] bg-yellow-900 h-[100%] w-full">
    <div
      class="container w-100 mx-auto px-6 py-3 flex justify-between items-center flex-col"
    >
      <div
        class="flex py-[30px] justify-between flex-row text-[#ffffff] w-full"
      >
        <h1 class="text-[20px]">Video list</h1>
        <button class="border-2 p-3 hover:bg-[#ffffff] hover:text-yellow-900">
          Add Video +
        </button>
      </div>

      <DataTable />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import DataTable from "~/components/DataTable.vue";

definePageMeta({ layout: "default" });
const isOpen = ref<boolean>(false);

useHead({
  title: "M.E. Final Year - CSE",
  meta: [{ name: "description", content: "M.E. Final Year - CSE" }],
});
</script>
