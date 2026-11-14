export default defineI18nLocale(async () => {
  const { en: $vuetify } = await import("vuetify/locale");
  const { default: enGB } = await import("../messages/en-GB.json");
  const { default: unitNames } = await import(
    "../../../../universalrecipes/repos/seed/resources/units/locales/en-GB.json",
  );
  return {
    ...enGB,
    "unit-names": unitNames,
    $vuetify,
  };
});
