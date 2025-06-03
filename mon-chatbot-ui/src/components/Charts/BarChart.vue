<template>
  <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

defineProps({
  chartData: {
    type: Object,
    required: true,
  },
  chartOptions: {
    type: Object,
    default: () => ({
      responsive: true,
      maintainAspectRatio: false, // Important pour contrôler la taille via CSS
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            // Assurer que les ticks sont des entiers si les comptes sont toujours des entiers
            precision: 0 
          }
        }
      },
      plugins: {
        legend: {
          display: true, // Vous pouvez le cacher si le titre du graphique est suffisant
        },
      },
    }),
  },
});
</script>