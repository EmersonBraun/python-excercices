import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Python From Zero to Hero',
  tagline: 'Master Python from fundamentals to advanced concepts with interactive exercises',

  future: {
    v4: true,
  },

  url: 'https://emersonbraun.github.io',
  baseUrl: '/python-from-zero-to-hero/',

  organizationName: 'EmersonBraun',
  projectName: 'python-from-zero-to-hero',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'pt-BR', 'es'],
    localeConfigs: {
      en: { label: 'English' },
      'pt-BR': { label: 'Português (BR)' },
      es: { label: 'Español' },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/EmersonBraun/python-from-zero-to-hero/edit/feat/curriculum-exercises/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/logo.svg',
    metadata: [
      {name: 'keywords', content: 'python, course, tutorial, beginner, advanced, learn, exercises, projects'},
    ],
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Home',
      logo: {alt: 'Python From Zero to Hero Logo', src: 'img/logo.svg'},
      items: [
        {type: 'docSidebar', sidebarId: 'courseSidebar', position: 'left', label: 'Course'},
        {href: 'https://github.com/EmersonBraun/python-from-zero-to-hero', label: 'GitHub', position: 'right'},
        {type: 'localeDropdown', position: 'right'},
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [{label: 'Course', to: '/docs/'}],
        },
        {
          title: 'Connect',
          items: [
            {label: 'Website', href: 'https://emersonbraun.dev/'},
            {label: 'LinkedIn', href: 'https://www.linkedin.com/in/emerson-braun/'},
            {label: 'X / Twitter', href: 'https://x.com/EmersonfBraun'},
            {label: 'Instagram', href: 'https://www.instagram.com/emerson.braun.dev/'},
            {label: 'YouTube', href: 'https://www.youtube.com/@emerson.braun_dev'},
          ],
        },
      ],
      copyright: `Python From Zero to Hero. Created by <a href="https://www.linkedin.com/in/emerson-braun/" target="_blank">Emerson Braun</a>`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'json', 'yaml', 'sql', 'python'],
    },
    algolia: {
      appId: process.env.ALGOLIA_APP_ID || 'placeholder',
      apiKey: process.env.ALGOLIA_API_KEY || 'placeholder',
      indexName: process.env.ALGOLIA_INDEX_NAME || 'python-from-zero-to-hero',
      contextualSearch: true,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
