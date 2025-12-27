import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className={clsx('container', styles.heroContainer)}>
        <div className={styles.heroText}>
                      <Heading as="h1" className="hero__title">
                        Physical AI and Humanoid Robotics
                      </Heading>
                      <p className="hero__subtitle">An AI powered learning platform</p>          <div className={styles.buttons}>
            <Link
              className="button button--secondary button--lg"
              to="/docs/intro">
              Start Reading 🤖
            </Link>
          </div>
        </div>
        <div className={styles.heroVisual}>
          {/* Placeholder for a visual element. 
              Using a simple gradient for now. 
              Will be updated in the stylesheet. */}
              <img src="/img/hero.png" alt="Hero Visual" />
        </div>
      </div>
    </header>
  );
}

import Testimonials from '@site/src/components/Testimonials';


export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <Testimonials />
              </main>
    </Layout>
  );
}
