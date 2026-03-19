import React from 'react';
import { render, screen } from '@testing-library/react';
import { vi, describe, it, expect } from 'vitest';
import AwsCheatsheetCard from '../../src/components/AwsCheatsheetCard/index';

vi.mock('@docusaurus/Link', () => ({
  default: ({ href, children, ...props }: any) => (
    <a href={href} {...props}>{children}</a>
  ),
}));

vi.mock('../../src/components/AwsCheatsheetCard/styles.module.css', () => ({
  default: {},
}));

describe('AwsCheatsheetCard', () => {
  it('renders the component without crashing', () => {
    render(<AwsCheatsheetCard />);
    expect(screen.getByRole('link', { name: /view aws cheatsheet/i })).toBeInTheDocument();
  });

  it('contains link to aws-cheatsheet', () => {
    render(<AwsCheatsheetCard />);
    const link = screen.getByRole('link', { name: /view aws cheatsheet/i });
    expect(link).toHaveAttribute('href', 'https://emersonbraun.github.io/aws-cheatsheet/');
  });

  it('displays the card title', () => {
    render(<AwsCheatsheetCard />);
    expect(screen.getByRole('heading', { name: /aws cheatsheet/i })).toBeInTheDocument();
  });

  it('opens link in a new tab', () => {
    render(<AwsCheatsheetCard />);
    const link = screen.getByRole('link', { name: /view aws cheatsheet/i });
    expect(link).toHaveAttribute('target', '_blank');
  });
});
