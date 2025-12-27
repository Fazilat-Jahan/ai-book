import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  imageUrl: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Foundations of Physical AI',
    imageUrl: '/img/physical_ai.jpg',
    description: (
      <>
        Explore the core concepts of Physical AI, including sensors, actuators, and advanced control systems.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics',
    imageUrl: '/img/humanoid_robot.jpg',
    description: (
      <>
        Dive into the world of humanoid robotics, covering locomotion, balance, manipulation, and human-robot interaction.
      </>
    ),
  },
  {
    title: 'AI + Robotics Applications',
    imageUrl: '/img/robotics_application.jpg',
    description: (
      <>
        Discover real-world applications of AI in robotics through hands-on labs, projects, and case studies.
      </>
    ),
  },
];

function Feature({title, imageUrl, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4', styles.featureCard)}>
      <div
        className={styles.featureCardImage}
        style={{backgroundImage: `url(${imageUrl})`}}
      />
      <div className={styles.featureCardContent}>
        <Heading as="h3" className={styles.featureCardTitle}>
          {title}
        </Heading>
        <p className={styles.featureCardDescription}>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
