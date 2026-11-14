export default defineI18nLocale(async () => {
  const { cs: $vuetify } = await import("vuetify/locale");
  const { default: csCZ } = await import("../messages/cs-CZ.json");
  const { default: unitNames } = await import(
    "../../../../universalrecipes/repos/seed/resources/units/locales/cs-CZ.json",
  );
  return {
    ...csCZ,
    "unit-names": unitNames,
    $vuetify,
  };
});
