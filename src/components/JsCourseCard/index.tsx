import Link from '@docusaurus/Link';
import {translate} from '@docusaurus/Translate';
import {type ReactElement} from 'react';

import styles from './styles.module.css';

export default function JsCourseCard(): ReactElement {
  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <span className={styles.icon} aria-hidden="true">
          JS
        </span>
        <h3 className={styles.title}>
          {translate({id: 'jsCourseCard.title', message: 'JavaScript From Zero to Hero'})}
        </h3>
      </div>
      <p className={styles.description}>
        {translate({
          id: 'jsCourseCard.description',
          message:
            'Learn JavaScript from the ground up — variables, DOM, async/await, and modern ES2024+ features. Companion course to your Python journey.',
        })}
      </p>
      <Link
        className="button button--secondary button--sm"
        href="https://emersonbraun.github.io/js-from-zero-to-hero/"
        target="_blank"
        rel="noopener noreferrer">
        {translate({id: 'View JS Course', message: 'View JS Course →'})}
      </Link>
    </div>
  );
}
