import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; // Assurez-vous que Pinia est initialisé avant le routeur

// Importation des vues
import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';
//import ChangePasswordForm from '@//ChangePasswordForm.vue'; 
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
import NonAutorisePage from '@/views/NonAutorisePage.vue';

const routes = [
  {
    path: '/login',
    name: 'Login', // Assurez-vous que ce nom est utilisé dans les redirections
    component: LoginView,
        meta: {
            requiresAuth: false,
          }
  },
  
  {
    path: '/',
    component: DashboardLayout,
    children: [
      {
        path: '',
        name: 'Chat', // Nom de la route par défaut
        component: ChatView,
        meta: {
            requiresAuth: true,
            roles: [1, 2,3,4,5] // Accessible par Admin (1) ou Prof (2)
                     // (la hiérarchie est gérée par permissionsParProfil)
          }
      },
      {
        path: 'ingest',
        name: 'Ingest',
        component: IngestView,
        meta: {
            requiresAuth: true,
            roles: [1] // Accessible par Admin (1) ou Prof (2)
                     // (la hiérarchie est gérée par permissionsParProfil)
          }
      },
      {
        path: 'documents',
        name: 'Documents',
        component: DocumentsView,
        meta: {
            requiresAuth: true,
            roles: [1, 2,3,4,5] // Accessible par Admin (1) ou Prof (2)
                     // (la hiérarchie est gérée par permissionsParProfil)
          }
      },
      {
        path: 'stats',
        name: 'Stats',
        component: StatsView,
        meta: {
            requiresAuth: true,
            roles: [1, 2,3,4,5] // Accessible par Admin (1) ou Prof (2)
                     // (la hiérarchie est gérée par permissionsParProfil)
          }
      },
      {
        path: 'admin', // Changé de /admin à admin pour être relatif au parent '/'
        component: AdminView,
        meta: {
            requiresAuth: true,
            roles: [1, 2,3,4,5] // Accessible par Admin (1) ou Prof (2)
                     // (la hiérarchie est gérée par permissionsParProfil)
        },
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
  },
  {
    path: '/non-autorise',
    name: 'NonAutorise', // Ce nom est utilisé dans next({ name: 'NonAutorise' })
    component: NonAutorisePage
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // ou juste createWebHistory()
  routes
});

const permissionsParProfil = {
  1: [1, 2, 3, 5],
  2: [2, 3, 5],
  3: [3, 5],
  5: [5]
};

router.beforeEach((to, from, next) => {
  const necessiteAuthentification = to.matched.some(record => record.meta.requiresAuth);
  const rolesRequisPourRoute = to.meta.roles; // Doit être un tableau de profile_id, ex: [1] ou [2, 3]
  const authStore = useAuthStore();
  const utilisateurActuel = authStore.user;
  console.log("Connected user",utilisateurActuel );

  if (necessiteAuthentification) {
    if (!utilisateurActuel) {
      // Utilisateur non connecté et la route nécessite une authentification
      console.log(`Accès refusé à ${to.path} (non connecté), redirection vers Login.`);
      next({ name: 'Login', query: { redirect: to.fullPath } }); // Optionnel: rediriger vers la page voulue après login
    } else {
      // Utilisateur connecté
      if (rolesRequisPourRoute && rolesRequisPourRoute.length > 0) {
        const profileIdUtilisateur = utilisateurActuel.profile_id;

        if (typeof profileIdUtilisateur === 'undefined') {
          console.error("L'objet utilisateur n'a pas de propriété 'profile_id':", utilisateurActuel);
          next({ name: 'Erreur' });
          return;
        }

        const rolesAccessiblesParUtilisateur = permissionsParProfil[profileIdUtilisateur];

        if (!rolesAccessiblesParUtilisateur) {
          console.warn(`Aucune permission définie dans 'permissionsParProfil' pour le profile_id: ${profileIdUtilisateur}. Accès refusé à ${to.path}.`);
          next({ name: 'NonAutorise' });
          return;
        }

        // Vérifier si l'utilisateur a la permission pour au moins un des rôles requis par la route,
        // en se basant sur les rôles auxquels son propre profil lui donne accès (hiérarchie).
        const aLaPermission = rolesRequisPourRoute.some(roleRoute =>
          rolesAccessiblesParUtilisateur.includes(roleRoute)
        );

        if (aLaPermission) {
          console.log(`Accès autorisé à ${to.path} pour l'utilisateur avec profile_id ${profileIdUtilisateur}.`);
          next();
        } else {
          console.log(`Accès refusé à ${to.path} pour l'utilisateur avec profile_id ${profileIdUtilisateur} (rôle insuffisant). Redirection vers NonAutorise.`);
          next({ name: 'NonAutorise' });
        }
      } else {
        // La route nécessite une authentification mais pas de rôle spécifique, donc on autorise
        console.log(`Accès autorisé à ${to.path} (authentification requise, pas de rôle spécifique).`);
        next();
      }
    }
  } else if (to.meta.requiresGuest && utilisateurActuel) {
    // Si la route est pour les invités (ex: page de login) et que l'utilisateur est déjà connecté
    console.log(`Utilisateur connecté essayant d'accéder à une route 'invité' (${to.path}). Redirection vers Accueil.`);
    next({ name: 'Accueil' });
  } else {
    // La route ne nécessite pas d'authentification (page publique) ou aucune condition spéciale non remplie
    console.log(`Accès autorisé à ${to.path} (route publique ou sans conditions spécifiques).`);
    next();
  }
});

export default router;