import React from 'react';
import { render, screen } from '@testing-library/react';
import { vi, describe, it, expect } from 'vitest';
import JsCourseCard from '../../src/components/JsCourseCard/index';

vi.mock('@docusaurus/Link', () => ({
  default: ({ href, children, ...props }: any) => (
    <a href={href} {...props}>{children}</a>
  ),
}));

vi.mock('../../src/components/JsCourseCard/styles.module.css', () => ({
  default: {},
}));

describe('JsCourseCard', () => {
  it('renders the component without crashing', () => {
    render(<JsCourseCard />);
    expect(screen.getByRole('link', { name: /view js course/i })).toBeInTheDocument();
  });

  it('contains link to js-from-zero-to-hero', () => {
    render(<JsCourseCard />);
    const link = screen.getByRole('link', { name: /view js course/i });
    expect(link).toHaveAttribute('href', 'https://emersonbraun.github.io/js-from-zero-to-hero/');
  });

  it('displays the card title', () => {
    render(<JsCourseCard />);
    expect(screen.getByText(/javascript from zero to hero/i)).toBeInTheDocument();
  });

  it('opens link in a new tab', () => {
    render(<JsCourseCard />);
    const link = screen.getByRole('link', { name: /view js course/i });
    expect(link).toHaveAttribute('target', '_blank');
  });
});
