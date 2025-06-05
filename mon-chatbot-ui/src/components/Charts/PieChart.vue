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
  CategoryScale,
} from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, ChartDataLabels);

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
        legend: { position: 'bottom' },
        datalabels: {
          color: '#fff',
          font: { weight: 'bold', size: 14 },
          borderRadius: 4,
          backgroundColor: 'rgba(44, 62, 80, 0.7)',
          padding: 6,
          formatter: (value, context) => {
            // Récupère toutes les valeurs du dataset
            const data = context.chart.data.datasets[0].data;
            // Calcule le total
            const total = data.reduce((a, b) => a + b, 0);
            if (!total) return '0 (0%)';
            // Calcule le pourcentage
            const percentage = (value / total) * 100;
            // Retourne valeur + pourcentage
            return `${value} (${percentage.toFixed(1)}%)`;
          },
        },
      },
    }),
  },
});
</script>