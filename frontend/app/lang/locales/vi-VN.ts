export default defineI18nLocale(async () => {
  const { vi: $vuetify } = await import("vuetify/locale");
  const { default: viVN } = await import("../messages/vi-VN.json");
  const { default: unitNames } = await import(
    "../../../../universalrecipes/repos/seed/resources/units/locales/vi-VN.json",
  );
  return {
    ...viVN,
    "unit-names": unitNames,
    $vuetify,
  };
});
