<template>
    <div class="overflow-x-auto w-full">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-[#F0F3F4]">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Video</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Frames</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Delete</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(item, index) in data" :key="index">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.Video }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.Frames }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.Delete }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  const data = [
    { Video: 'mlops.mp4', Frames: 'List', Delete: 'Delete' },
  ];
  </script>
  