import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import Testimonials from '@site/src/components/Testimonials';

import styles from './index.module.css';

// Premium background elements component
function PremiumBackground() {
  return (
    <div className={styles.premiumBackground} aria-hidden="true" />
  );
}

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)} role="banner">
      <PremiumBackground />
      <div className={clsx('container', styles.heroContainer)}>
        <div className="row"> {/* Use row layout for text on left, visual on right */}
          <div className="col col--6"> {/* Left column for text */}
            <div className={styles.heroTextContainer}>
              <div className={styles.heroBadge}>
                <span>🤖 AI-Powered Learning</span>
              </div>
              <h1 className={styles.heroTitle}>
                Physical AI and Humanoid Robotics
              </h1>
              <p className={styles.heroSubtitle}>
                Master the future of robotics with cutting-edge AI concepts, hands-on projects, and interactive learning
              </p>
              <div className={styles.heroButtons}>
                <Link
                  className={styles.glassButtonPrimary}
                  to="/docs/intro">
                  Start Learning
                </Link>
                <Link
                  className={styles.glassButtonSecondary}
                  to="/docs/course-summary">
                  Explore Course
                </Link>
              </div>
            </div>
          </div>
          <div className="col col--6"> {/* Right column for visual elements */}
            <div className={styles.heroVisual} aria-hidden="true">
              <div className={styles.heroVisualContainer}>
                {/* Premium animated visual elements */}
                <div className={styles.floatingElement1}></div>
                <div className={styles.floatingElement2}></div>
                <div className={styles.floatingElement3}></div>
                <div className={styles.orbitingCircle1}></div>
                <div className={styles.orbitingCircle2}></div>
                <div className={styles.centralOrb}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

// Stats Component for premium look
function StatsSection() {
  const stats = [
    { value: '50K+', label: 'Active Learners' },
    { value: '200+', label: 'AI Concepts' },
    { value: '50+', label: 'Hands-on Projects' },
    { value: '24/7', label: 'AI Support' },
  ];

  return (
    <section className={styles.statsSection} aria-labelledby="stats-heading">
      <div className="container">
        <div className="row">
          {stats.map((stat, index) => (
            <div key={index} className="col col--3 text--center">
              <div className={styles.statItem}>
                <div className={styles.statValue}>{stat.value}</div>
                <div className={styles.statLabel}>{stat.label}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`AI Book - ${siteConfig.title}`}
      description="Physical AI and Humanoid Robotics - An AI powered learning platform">
      <PremiumBackground />
      <HomepageHeader />
      <main>
        <StatsSection />
        <HomepageFeatures />
        <Testimonials />
      </main>
    </Layout>
  );
}
