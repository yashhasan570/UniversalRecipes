export default defineNuxtRouteMiddleware(() => {
  const { user } = useUniversalRecipesAuth();
  // If the user is not an admin redirect to the home page
  if (!user.value?.admin) {
    return navigateTo("/");
  }
});
