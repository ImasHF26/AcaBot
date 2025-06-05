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
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ChartDataLabels);

defineProps({
  chartData: { type: Object, required: true },
  chartOptions: {
    type: Object,
    default: () => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: true },
        datalabels: {
          anchor: 'end',
          align: 'top',
          color: '#34495e',
          font: { weight: 'bold', size: 14 },
          formatter: Math.round,
        },
      },
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0 } }
      }
    }),
  },
});
</script>