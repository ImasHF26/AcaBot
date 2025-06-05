<template>
  <div class="stats-view-container">
    <h2>Statistiques d'Ingestion</h2>
    <button @click="fetchStats" :disabled="isLoading" class="refresh-button">
      {{ isLoading ? 'Chargement...' : 'Rafraîchir les statistiques' }}
    </button>
    <div v-if="isLoading" class="loading-indicator">Chargement des statistiques...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="stats && !isLoading" class="stats-layout">
      <!-- Section des cartes de statistiques -->
      <div class="stats-cards-grid">
        <div class="stat-card">
          <h3>Total Documents Ingérés</h3>
          <p class="stat-value">{{ stats.total_documents }}</p>
        </div>
        <div class="stat-card" v-if="stats.ingested_today !== undefined">
          <h3>Ingestions Aujourd'hui</h3>
          <p class="stat-value">{{ stats.ingested_today }}</p>
        </div>
        <div class="stat-card" v-if="stats.ingested_this_week !== undefined">
          <h3>Ingestions cette Semaine</h3>
          <p class="stat-value">{{ stats.ingested_this_week }}</p>
        </div>
        <div class="stat-card" v-if="stats.ingested_this_month !== undefined">
          <h3>Ingestions ce Mois</h3>
          <p class="stat-value">{{ stats.ingested_this_month }}</p>
        </div>
      </div>

      <!-- Section des graphiques -->
      <div class="charts-grid">
        <div class="chart-container card" v-if="departementChartData.datasets[0]?.data.length > 0">
          <h4>Documents par Département</h4>
          <BarChart :chartData="departementChartData" :chartOptions="barChartOptions" />
        </div>
        
        <div class="chart-container card" v-if="activiteChartData.datasets[0]?.data.length > 0">
          <h4>Documents par Activité</h4>
          <PieChart :chartData="activiteChartData" :chartOptions="pieChartOptions" />
        </div>

        <!-- NOUVEAU: Graphique pour Filières -->
        <div class="chart-container card" v-if="filiereChartData.datasets[0]?.data.length > 0">
          <h4>Documents par Filière</h4>
          <BarChart :chartData="filiereChartData" :chartOptions="barChartOptionsFiliere" />
        </div>

        <!-- NOUVEAU: Graphique pour Modules -->
        <div class="chart-container card" v-if="moduleChartData.datasets[0]?.data.length > 0">
          <h4>Documents par Module</h4>
          <BarChart :chartData="moduleChartData" :chartOptions="barChartOptionsModule" />
        </div>
      </div>
      
      <!-- Section des listes de statistiques (peut être combinée ou stylisée différemment) -->
      <div class="stats-lists-grid">
        <div v-if="stats.documents_par_departement && stats.documents_par_departement.length > 0" class="stats-section card">
          <h4>Détail par Département</h4>
          <ul class="stats-list">
            <li v-for="depStat in stats.documents_par_departement" :key="depStat.departement" class="list-item">
              {{ depStat.departement }}: <span class="count">{{ depStat.count }}</span>
            </li>
          </ul>
        </div>

        <div v-if="stats.documents_par_filiere && stats.documents_par_filiere.length > 0" class="stats-section card">
          <h4>Détail par Filière</h4>
          <ul class="stats-list">
            <li v-for="filStat in stats.documents_par_filiere" :key="filStat.filiere" class="list-item">
              {{ filStat.filiere }}: <span class="count">{{ filStat.count }}</span>
            </li>
          </ul>
        </div>

        <div v-if="stats.documents_par_module && stats.documents_par_module.length > 0" class="stats-section card">
          <h4>Détail par Module</h4>
          <ul class="stats-list">
            <li v-for="modStat in stats.documents_par_module" :key="modStat.module" class="list-item">
              {{ modStat.module }}: <span class="count">{{ modStat.count }}</span>
            </li>
          </ul>
        </div>

        <div v-if="stats.documents_par_activite && stats.documents_par_activite.length > 0" class="stats-section card">
          <h4>Détail par Activité</h4>
          <ul class="stats-list">
            <li v-for="actStat in stats.documents_par_activite" :key="actStat.activite" class="list-item">
              {{ actStat.activite }}: <span class="count">{{ actStat.count }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
     <div v-if="!isLoading && !stats && !error" class="no-stats">
      Aucune statistique disponible.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/services/api';
import BarChart from '@/components/Charts/BarChart.vue';
import PieChart from '@/components/Charts/PieChart.vue';

const stats = ref(null);
const isLoading = ref(false);
const error = ref(null);

const fetchStats = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    const response = await api.getStats();
    stats.value = response.data;
  } catch (err) {
    error.value = "Impossible de charger les statistiques. " + (err.response?.data?.detail || err.message);
    stats.value = null;
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchStats();
});

// Options communes pour les graphiques à barres
const commonBarChartOptions = (displayLegend = false) => ({
  responsive: true,
  maintainAspectRatio: false,
  scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
  plugins: { legend: { display: displayLegend } }
});

const barChartOptions = ref(commonBarChartOptions(false)); // Pour Département
const barChartOptionsFiliere = ref(commonBarChartOptions(false)); // Pour Filière
const barChartOptionsModule = ref(commonBarChartOptions(false)); // Pour Module


const pieChartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'bottom' } }
});

// Données calculées pour les graphiques
const departementChartData = computed(() => {
  if (!stats.value || !stats.value.documents_par_departement) {
    return { labels: [], datasets: [{ data: [] }] }; // Assurer que datasets existe
  }
  const labels = stats.value.documents_par_departement.map(item => item.departement);
  const data = stats.value.documents_par_departement.map(item => item.count);
  return {
    labels,
    datasets: [
      {
        label: 'Documents par Département',
        backgroundColor: '#42A5F5',
        borderColor: '#1E88E5',
        borderWidth: 1,
        data,
      },
    ],
  };
});

const activiteChartData = computed(() => {
  if (!stats.value || !stats.value.documents_par_activite) {
    return { labels: [], datasets: [{ data: [] }] }; // Assurer que datasets existe
  }
  const labels = stats.value.documents_par_activite.map(item => item.activite);
  const data = stats.value.documents_par_activite.map(item => item.count);
  return {
    labels,
    datasets: [
      {
        label: 'Documents par Activité',
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#E7E9ED', '#8A2BE2', '#A52A2A', '#DEB887', '#5F9EA0', '#7FFF00'],
        data,
      },
    ],
  };
});

// NOUVEAU: Données pour le graphique Filière
const filiereChartData = computed(() => {
  if (!stats.value || !stats.value.documents_par_filiere) {
    return { labels: [], datasets: [{ data: [] }] }; // Assurer que datasets existe
  }
  const labels = stats.value.documents_par_filiere.map(item => item.filiere);
  const data = stats.value.documents_par_filiere.map(item => item.count);
  return {
    labels,
    datasets: [
      {
        label: 'Documents par Filière',
        backgroundColor: '#66BB6A', // Couleur verte
        borderColor: '#388E3C',
        borderWidth: 1,
        data,
      },
    ],
  };
});

// NOUVEAU: Données pour le graphique Module
const moduleChartData = computed(() => {
  if (!stats.value || !stats.value.documents_par_module) {
    return { labels: [], datasets: [{ data: [] }] }; // Assurer que datasets existe
  }
  const labels = stats.value.documents_par_module.map(item => item.module);
  const data = stats.value.documents_par_module.map(item => item.count);
  return {
    labels,
    datasets: [
      {
        label: 'Documents par Module',
        backgroundColor: '#FFA726', // Couleur orange
        borderColor: '#F57C00',
        borderWidth: 1,
        data,
      },
    ],
  };
});

</script>

<style scoped>
/* Vos styles existants sont bons.
   La grille .charts-grid s'adaptera automatiquement pour afficher plus de graphiques.
   Vous pourriez vouloir ajuster minmax dans grid-template-columns si vous avez beaucoup de graphiques
   ou si vous voulez qu'ils soient plus petits.
   Exemple: grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
*/

.stats-view-container {
  padding: 20px;
  max-width: 1200px;
  margin: auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
  font-size: 2em;
}
.refresh-button {
  display: block;
  margin: 0 auto 30px auto;
  padding: 12px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
  font-size: 1em;
}
.refresh-button:hover {
  background-color: #2980b9;
}
.refresh-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.loading-indicator, .no-stats {
  text-align: center;
  padding: 30px;
  font-size: 1.2em;
  color: #7f8c8d;
}
.error-message {
  color: #c0392b;
  background-color: #fdecea;
  border: 1px solid #e74c3c;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 20px;
  text-align: center;
}

.stats-layout {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.stats-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.charts-grid {
  display: grid;
  /* Ajustez minmax si vous avez beaucoup de graphiques ou si vous voulez qu'ils soient plus petits */
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
  gap: 20px;
}

.stats-lists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.card {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  border: 1px solid #ecf0f1;
}
.card h4 {
  margin-top: 0;
  border-bottom: 1px solid #ecf0f1;
  padding-bottom: 10px;
  margin-bottom: 15px;
  font-size: 1.25em;
  color: #34495e;
}

.stat-card {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  text-align: center;
  border: 1px solid #ecf0f1;
}
.stat-card h3 {
  margin-top: 0;
  font-size: 1.1em;
  color: #34495e;
  margin-bottom: 10px;
}
.stat-value {
  font-size: 2.5em;
  font-weight: 600;
  color: #3498db;
  margin: 10px 0 0 0;
}

.chart-container {
  height: 400px;
  position: relative;
  padding: 20px 10px 10px 10px;
  background: #f8fafc;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(52,152,219,0.07);
}

.chart-container canvas {
  position: relative;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.stats-list {
  list-style-type: none;
  padding: 0;
  max-height: 250px;
  overflow-y: auto;
}
.list-item {
  padding: 10px 5px;
  border-bottom: 1px solid #f7f9f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95em;
}
.list-item:last-child {
  border-bottom: none;
}
.count {
  font-weight: 600;
  background-color: #eaf2f8;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.9em;
  color: #2c3e50;
}

.card, .stat-card {
  transition: box-shadow 0.2s;
}
.card:hover, .stat-card:hover {
  box-shadow: 0 8px 24px rgba(52, 152, 219, 0.15);
  border-color: #b2dffc;
}
h2, h3, h4 {
  font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif;
  letter-spacing: 0.5px;
}
.stat-value {
  color: #1abc9c;
  text-shadow: 0 2px 8px #e0f7fa;
}
.refresh-button {
  font-family: 'Montserrat', Arial, sans-serif;
  font-weight: 600;
  letter-spacing: 1px;
}
</style>