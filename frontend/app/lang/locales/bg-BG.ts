export default defineI18nLocale(async () => {
  const { bg: $vuetify } = await import("vuetify/locale");
  const { default: bgBG } = await import("../messages/bg-BG.json");
  const { default: unitNames } = await import(
    "../../../../universalrecipes/repos/seed/resources/units/locales/bg-BG.json",
  );
  return {
    ...bgBG,
    "unit-names": unitNames,
    $vuetify,
  };
});
