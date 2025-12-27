import React from 'react';
import styles from './styles.module.css';
import Heading from '@theme/Heading';

const TestimonialList = [
  {
    quote: "This is the best book I've ever read about Physical AI!",
    author: 'John Doe, AI Enthusiast',
  },
  {
    quote: 'A must-read for anyone interested in humanoid robotics.',
    author: 'Jane Smith, Robotics Engineer',
  },
  {
    quote: 'The interactive chatbot is a game-changer for learning.',
    author: 'Peter Jones, Student',
  },
];

function Testimonial({quote, author}) {
  return (
    <div className={styles.testimonial}>
      <p className={styles.testimonialQuote}>"{quote}"</p>
      <p className={styles.testimonialAuthor}>- {author}</p>
    </div>
  );
}

export default function Testimonials() {
  return (
    <section className={styles.testimonialsSection}>
      <div className="container">
        <Heading as="h2" className="text--center">
          What Our Readers Are Saying
        </Heading>
        <div className={styles.testimonials}>
          {TestimonialList.map((props, idx) => (
            <Testimonial key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
