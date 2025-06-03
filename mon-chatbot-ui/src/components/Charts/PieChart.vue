<template>
  <Pie v-if="chartData" :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Pie } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale, // Bien que ce soit un Pie, CategoryScale est souvent enregistré
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

defineProps({
  chartData: {
    type: Object,
    required: true,
  },
  chartOptions: {
    type: Object,
    default: () => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top', // Ou 'bottom', 'left', 'right'
        },
      },
    }),
  },
});
</script>