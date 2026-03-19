import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Python From Zero to Hero',
  tagline: 'Master Python from fundamentals to advanced concepts with interactive exercises',
  favicon: 'img/favicon.ico',

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
      en: {label: 'English', direction: 'ltr'},
      'pt-BR': {label: 'Português', direction: 'ltr'},
      es: {label: 'Español', direction: 'ltr'},
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/EmersonBraun/python-excercices/blob/master',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/logo.png',
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
        {type: 'localeDropdown', position: 'right'},
        {href: 'https://github.com/EmersonBraun/python-excercices', label: 'GitHub', position: 'right'},
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
  } satisfies Preset.ThemeConfig,
};

export default config;
