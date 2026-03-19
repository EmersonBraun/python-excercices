import Link from '@docusaurus/Link';
import {translate} from '@docusaurus/Translate';
import {type ReactElement} from 'react';

import styles from './styles.module.css';

export default function AwsCheatsheetCard(): ReactElement {
  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <span className={styles.icon} aria-hidden="true">
          AWS
        </span>
        <h3 className={styles.title}>
          {translate({id: 'awsCheatsheetCard.title', message: 'AWS Cheatsheet'})}
        </h3>
      </div>
      <p className={styles.description}>
        {translate({
          id: 'awsCheatsheetCard.description',
          message:
            'Quick-reference guide for the most important AWS services, CLI commands, and cloud architecture patterns. Bookmark it, use it daily.',
        })}
      </p>
      <Link
        className="button button--secondary button--sm"
        href="https://emersonbraun.github.io/aws-cheatsheet/"
        target="_blank"
        rel="noopener noreferrer">
        {translate({id: 'View AWS Cheatsheet', message: 'View AWS Cheatsheet →'})}
      </Link>
    </div>
  );
}
