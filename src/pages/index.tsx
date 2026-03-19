import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import {type ReactElement} from 'react';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link className="button button--secondary button--lg" to="/docs/">
            Start Learning
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactElement {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="Master Python from fundamentals to advanced concepts with interactive exercises">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--8 col--offset-2">
                <div className="text--center padding-horiz--md">
                  <div className={styles.introSection}>
                    <h2>What is this course?</h2>
                    <p>
                      Python From Zero to Hero is a comprehensive, hands-on Python course that takes
                      you from absolute beginner to advanced developer. Each module combines theory
                      with interactive exercises you can run locally, plus real-world
                      projects to build your portfolio.
                    </p>
                    <div className={styles.buttons}>
                      <Link
                        className="button button--primary button--lg"
                        to="/docs/">
                        Explore the Course
                      </Link>
                    </div>
                  </div>

                  <h2>What you will learn</h2>
                  <ul>
                    <li>Python fundamentals from scratch</li>
                    <li>Functions, modules, and OOP</li>
                    <li>Decorators, generators, and async patterns</li>
                    <li>Real-world projects and exercises</li>
                    <li>Testing, debugging, and best practices</li>
                    <li>Design patterns and performance optimization</li>
                  </ul>

                  <h2>Help Improve This Course</h2>
                  <p>
                    This project thrives on community contributions. Whether you are learning
                    Python or are an experienced developer, your insights are valuable!
                  </p>

                  <div className={styles.buttons} style={{marginBottom: '4rem'}}>
                    <Link
                      className="button button--secondary button--lg"
                      href="https://github.com/EmersonBraun/python-excercices">
                      Contribute to the Project
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
