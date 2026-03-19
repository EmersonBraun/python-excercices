import React from 'react';
import { render, screen } from '@testing-library/react';
import { vi, describe, it, expect } from 'vitest';
import EbookCta from '../../src/components/EbookCta/index';

// Mock @docusaurus/Link as a simple anchor
vi.mock('@docusaurus/Link', () => ({
  default: ({ href, children, ...props }: any) => (
    <a href={href} {...props}>{children}</a>
  ),
}));

vi.mock('../../src/components/EbookCta/styles.module.css', () => ({
  default: {},
}));

describe('EbookCta', () => {
  it('renders the component without crashing', () => {
    render(<EbookCta />);
    expect(screen.getByRole('link', { name: /get the ebook/i })).toBeInTheDocument();
  });

  it('contains link to ebook.emersonbraun.dev', () => {
    render(<EbookCta />);
    const link = screen.getByRole('link', { name: /get the ebook/i });
    expect(link).toHaveAttribute('href', 'https://ebook.emersonbraun.dev');
  });

  it('displays the ebook title', () => {
    render(<EbookCta />);
    expect(screen.getByText(/cracking the technical interview/i)).toBeInTheDocument();
  });

  it('opens link in a new tab', () => {
    render(<EbookCta />);
    const link = screen.getByRole('link', { name: /get the ebook/i });
    expect(link).toHaveAttribute('target', '_blank');
  });
});
