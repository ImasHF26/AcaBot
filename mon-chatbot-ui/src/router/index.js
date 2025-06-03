import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; // Assurez-vous que Pinia est initialisé avant le routeur

// Importation des vues
import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';
//import ChangePasswordForm from '@/views/ChangePasswordForm.vue'; 
import DashboardLayout from '@/views/DashboardLayout.vue';
import ChatView from '@/views/ChatView.vue';
import IngestView from '@/views/IngestView.vue';
import DocumentsView from '@/views/DocumentsView.vue';
import StatsView from '@/views/StatsView.vue';
import AdminView from '@/views/AdminView.vue';
import AdminDepartements from '@/components/admin/AdminDepartements.vue';
import AdminFilieres from '@/components/admin/AdminFilieres.vue';
import AdminModules from '@/components/admin/AdminModules.vue';
import AdminActivites from '@/components/admin/AdminActivites.vue';

const routes = [
  {
    path: '/chat',
    name: 'Chat', // Assurez-vous que ce nom est utilisé dans les redirections
    component: ChatView,
    beforeEnter: (to, from, next) => {
    const authStore = useAuthStore()
    // Autoriser l'accès si authentifié OU en mode invité
    if (authStore.isAuthenticated || authStore.isInviteMode) {
      next()
    } else {
      next('/login')
    }
  }
  },
  {
    path: '/login',
    name: 'Login', // Assurez-vous que ce nom est utilisé dans les redirections
    component: LoginView,
    meta: { requiresGuest: true }
  },
  
  {
    path: '/',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Chat', // Nom de la route par défaut
        component: ChatView,
      },
      {
        path: 'ingest',
        name: 'Ingest',
        component: IngestView,
      },
      {
        path: 'documents',
        name: 'Documents',
        component: DocumentsView,
      },
      {
        path: 'stats',
        name: 'Stats',
        component: StatsView,
      },
      {
        path: 'admin', // Changé de /admin à admin pour être relatif au parent '/'
        component: AdminView,
        meta: { requiresAdmin: true }, // requiresAuth est hérité du parent
        children: [
          { path: '', name: 'AdminDashboard', redirect: { name: 'AdminDepartements' } }, // Redirection par défaut
          { path: 'departements', name: 'AdminDepartements', component: AdminDepartements },
          { path: 'filieres', name: 'AdminFilieres', component: AdminFilieres },
          { path: 'modules', name: 'AdminModules', component: AdminModules },
          { path: 'activites', name: 'AdminActivites', component: AdminActivites },
          { path: 'register', name: 'Register', component: RegisterView },
        ]
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound', // Donnez un nom à cette route
    redirect: () => {
      // Il est préférable d'initialiser le store ici si ce n'est pas déjà fait
      // car Pinia pourrait ne pas être prêt au moment de la définition des routes.
      const authStore = useAuthStore();
      return authStore.isAuthenticated ? { name: 'Chat' } : { name: 'Login' };
    }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Garde de navigation globale
router.beforeEach(async (to, from, next) => { // Ajout de async si loadUserFromStorage est asynchrone
  const authStore = useAuthStore();
  if (to.name === 'Chat') {
    console.log("Router Guard: Accessing public chat page.");
    next();
    return;
  }
  // Assurez-vous que l'état de l'utilisateur est chargé (surtout après un rechargement de page)
  // Cela devrait être fait avant les vérifications d'authentification
  if (!authStore.user && localStorage.getItem('userToken')) { // Vérifiez le token ou un indicateur d'utilisateur
    // Si loadUserFromStorage est asynchrone, attendez sa complétion
    await authStore.loadUserFromStorage(); // Assurez-vous que cette méthode existe et fonctionne
  }

  const isAuthenticated = authStore.isAuthenticated;
  // Assurez-vous que authStore.user est défini avant d'accéder à authStore.user.id
  const isAdmin = isAuthenticated && authStore.user && authStore.user.profile_id === 1; // ou authStore.user.role === 'admin'

  // Logique pour les routes nécessitant d'être invité (non connecté)
  if (to.meta.requiresGuest && isAuthenticated) {
    console.log("Router Guard: User is authenticated, redirecting from guest page to Chat.");
    next({ name: 'Chat' });
    return; // Important: sortir après next() pour éviter d'autres appels
  }

  // Logique pour les routes nécessitant une authentification
  if (to.meta.requiresAuth && !isAuthenticated) {
    console.log("Router Guard: Route requires auth, user not authenticated, redirecting to Login.");
    next({ name: 'Login' });
    return; // Important
  }

  // Logique pour les routes nécessitant un rôle admin
  // Cette vérification doit venir APRÈS la vérification requiresAuth
  if (to.meta.requiresAdmin && !isAdmin) {
    console.warn("Router Guard: User is not admin, redirecting from admin page to Chat.");
    // Rediriger vers la page d'accueil ou une page "Non autorisé"
    next({ name: 'Chat' }); // Ou une page 'Unauthorized' si vous en avez une
    return; // Important
  }

  // Si aucune des conditions ci-dessus n'a entraîné une redirection, autoriser la navigation
  console.log("Router Guard: Allowing navigation to", to.name || to.path);
  next();
});

export default router;