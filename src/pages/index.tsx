import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import {type ReactElement} from 'react';

import AwsCheatsheetCard from '../components/AwsCheatsheetCard';
import EbookCta from '../components/EbookCta';
import JsCourseCard from '../components/JsCourseCard';
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
            <Translate id="Start Learning">Start Learning</Translate>
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
      description={translate({
        id: 'homepage.metaDescription',
        message: 'Master Python from fundamentals to advanced concepts with interactive exercises',
      })}>
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--8 col--offset-2">
                <div className="text--center padding-horiz--md">
                  <div className={styles.introSection}>
                    <h2>
                      <Translate id="What is this course?">What is this course?</Translate>
                    </h2>
                    <p>
                      <Translate id="Python From Zero to Hero is a comprehensive, hands-on Python course that takes you from absolute beginner to advanced developer. Each module combines theory with interactive exercises you can run locally, plus real-world projects to build your portfolio.">
                        Python From Zero to Hero is a comprehensive, hands-on Python course that takes
                        you from absolute beginner to advanced developer. Each module combines theory
                        with interactive exercises you can run locally, plus real-world
                        projects to build your portfolio.
                      </Translate>
                    </p>
                    <div className={styles.buttons}>
                      <Link
                        className="button button--primary button--lg"
                        to="/docs/">
                        <Translate id="Explore the Course">Explore the Course</Translate>
                      </Link>
                    </div>
                  </div>

                  <h2>
                    <Translate id="What you will learn">What you will learn</Translate>
                  </h2>
                  <ul>
                    <li><Translate id="Python fundamentals from scratch">Python fundamentals from scratch</Translate></li>
                    <li><Translate id="Functions, modules, and OOP">Functions, modules, and OOP</Translate></li>
                    <li><Translate id="Decorators, generators, and async patterns">Decorators, generators, and async patterns</Translate></li>
                    <li><Translate id="Real-world projects and exercises">Real-world projects and exercises</Translate></li>
                    <li><Translate id="Testing, debugging, and best practices">Testing, debugging, and best practices</Translate></li>
                    <li><Translate id="Design patterns and performance optimization">Design patterns and performance optimization</Translate></li>
                  </ul>

                  <h2>
                    <Translate id="Help Improve This Course">Help Improve This Course</Translate>
                  </h2>
                  <p>
                    <Translate id="This project thrives on community contributions. Whether you are learning Python or are an experienced developer, your insights are valuable!">
                      This project thrives on community contributions. Whether you are learning
                      Python or are an experienced developer, your insights are valuable!
                    </Translate>
                  </p>

                  <div className={styles.buttons} style={{marginBottom: '4rem'}}>
                    <Link
                      className="button button--secondary button--lg"
                      href="https://github.com/EmersonBraun/python-from-zero-to-hero">
                      <Translate id="Contribute to the Project">Contribute to the Project</Translate>
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.moreResources}>
          <div className="container">
            <div className="row">
              <div className="col col--8 col--offset-2">
                <h2 className="text--center" style={{marginBottom: '1.5rem'}}>
                  <Translate id="More Resources">More Resources</Translate>
                </h2>
                <EbookCta />
                <div className={styles.cardsRow}>
                  <div className={styles.cardCol}>
                    <JsCourseCard />
                  </div>
                  <div className={styles.cardCol}>
                    <AwsCheatsheetCard />
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
