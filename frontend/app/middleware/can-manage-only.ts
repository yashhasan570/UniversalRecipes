export default defineNuxtRouteMiddleware(() => {
  const { user } = useUniversalRecipesAuth();
  // If the user is not allowed to manage group settings redirect to the home page
  if (!user.value?.canManage) {
    console.warn("User is not allowed to manage group settings");
    return navigateTo("/");
  }
});
