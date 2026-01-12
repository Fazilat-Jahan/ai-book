import React from 'react';
import styles from './styles.module.css';
import Heading from '@theme/Heading';

const TestimonialList = [
  {
    quote: "This is the best book I've ever read about Physical AI! The interactive chatbot makes learning so much easier.",
    author: 'John Doe',
    role: 'AI Enthusiast',
    rating: 5,
    avatar: 'JD'
  },
  {
    quote: 'A must-read for anyone interested in humanoid robotics. The practical examples are incredibly valuable.',
    author: 'Jane Smith',
    role: 'Robotics Engineer',
    rating: 5,
    avatar: 'JS'
  },
  {
    quote: 'The interactive chatbot is a game-changer for learning. I can ask questions and get immediate, accurate responses.',
    author: 'Peter Jones',
    role: 'Student',
    rating: 5,
    avatar: 'PJ'
  },
  {
    quote: 'The hands-on projects helped me understand complex concepts that were difficult to grasp from traditional textbooks.',
    author: 'Sarah Wilson',
    role: 'Researcher',
    rating: 5,
    avatar: 'SW'
  }
];

function Testimonial({quote, author, role, rating, avatar}) {
  const renderStars = () => {
    return Array.from({length: rating}).map((_, i) => (
      <span key={i} aria-hidden="true">★</span>
    ));
  };

  return (
    <div className={styles.testimonial} role="region" aria-labelledby={`testimonial-quote-${author.replace(/\s+/g, '-').toLowerCase()}`}>
      <div className={styles.testimonialAvatar} aria-label={`${author}'s avatar`}>
        {avatar}
      </div>
      <div className={styles.testimonialRating} aria-label={`Rating: ${rating} stars`}>
        {renderStars()}
      </div>
      <p className={styles.testimonialQuote} id={`testimonial-quote-${author.replace(/\s+/g, '-').toLowerCase()}`}>"{quote}"</p>
      <p className={styles.testimonialAuthor} id={`testimonial-author-${author.replace(/\s+/g, '-').toLowerCase()}`}>
        - {author}, {role}
      </p>
    </div>
  );
}

export default function Testimonials() {
  return (
    <section className={styles.testimonialsSection} aria-labelledby="testimonials-heading">
      <div className="container">
        <Heading as="h2" className="text--center" id="testimonials-heading">
          What Our Readers Are Saying
        </Heading>
        <div className={styles.testimonials} role="list" aria-label="Testimonials from readers">
          {TestimonialList.map((props, idx) => (
            <div role="listitem" key={idx}>
              <Testimonial {...props} />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}