export default defineNuxtRouteMiddleware((to) => {
  const { loggedIn } = useUniversalRecipesAuth();
  // If the user is not logged in redirect to the login page, then back here once they are
  if (!loggedIn.value) {
    return navigateTo({ path: "/login", query: { redirect: to.fullPath } });
  }
});
