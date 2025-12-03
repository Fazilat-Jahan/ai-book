import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'AI Book',
  tagline: 'An AI-powered learning platform for the Physical AI & Humanoid Robotics program.',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://aidriven-book.vercel.app/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/ai-book/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Fazilat-Jahan', // Usually your GitHub org/user name.
  projectName: 'ai-book', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/GIAIC/ai-book/tree/main/',
                },
                                blog: {
                                  showReadingTime: true,
                                  feedOptions: {
                                    type: ['rss', 'atom'],
                                    xslt: true,
                                  },
                                  // Please change this to your repo.
                                  // Remove this to remove the "edit this page" links.
                                  editUrl:
                                    'https://github.com/GIAIC/ai-book/tree/main/',
                                  // Useful options to enforce blogging best practices
                                  onInlineTags: 'warn',
                                  onInlineAuthors: 'warn',
                                  onUntruncatedBlogPosts: 'warn',
                                },
                                theme: {
                                  customCss: './src/css/custom.css',
                                },
                              } satisfies Preset.Options,
                            ],
                          ],  plugins: [
    // Add this custom Webpack plugin for proxy configuration
    function customWebpackDevServerProxyPlugin() {
      return {
        name: 'custom-webpack-dev-server-proxy-plugin',
        configureWebpack() {
          return {
            devServer: {
              proxy: [
                {
                  context: ['/api'], // The paths to proxy
                  target: 'http://localhost:8000', // Your backend API server
                  changeOrigin: true,
                  pathRewrite: { '^/api': '' }, // Rewrite the path to remove /api prefix
                },
              ],
            },
          };
        },
      };
    },
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'AI Book',
      logo: {
        alt: 'AI Book Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/GIAIC/ai-book',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Book',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus',
            },
            {
              label: 'X',
              href: 'https://x.com/docusaurus',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/GIAIC/ai-book',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} GIAIC. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
