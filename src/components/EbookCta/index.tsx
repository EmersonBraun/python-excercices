import Link from '@docusaurus/Link';
import {type ReactElement} from 'react';

import styles from './styles.module.css';

export default function EbookCta(): ReactElement {
  return (
    <div className={styles.banner}>
      <div className={styles.iconWrapper} aria-hidden="true">
        📘
      </div>
      <div className={styles.content}>
        <h3 className={styles.title}>Cracking the Technical Interview</h3>
        <p className={styles.description}>
          Ace your next tech interview with proven strategies, real questions, and
          expert tips. Get the ebook and land the job you deserve.
        </p>
      </div>
      <Link
        className="button button--primary"
        href="https://ebook.emersonbraun.dev"
        target="_blank"
        rel="noopener noreferrer">
        Get the Ebook
      </Link>
    </div>
  );
}
