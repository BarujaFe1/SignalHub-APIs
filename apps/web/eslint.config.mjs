import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  {
    rules: {
      // Client data-fetch pages intentionally set state after mount / filter changes.
      "react-hooks/set-state-in-effect": "off",
      // Relative time labels use Date.now(); acceptable for ops dashboard freshness UI.
      "react-hooks/purity": "off",
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
  globalIgnores([
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
  ]),
]);

export default eslintConfig;
