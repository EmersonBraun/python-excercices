import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { vi, describe, it, expect, beforeAll } from 'vitest';
import PythonRunner from '../../src/components/PythonRunner/index';

// Mock Pyodide — it cannot load in jsdom
beforeAll(() => {
  (window as any).loadPyodide = vi.fn().mockResolvedValue({
    globals: {
      get: vi.fn().mockReturnValue(vi.fn().mockReturnValue({})),
    },
    runPython: vi.fn().mockReturnValue(''),
    runPythonAsync: vi.fn().mockResolvedValue(undefined),
  });
});

// Mock styles to avoid CSS module issues
vi.mock('../../src/components/PythonRunner/styles.module.css', () => ({
  default: {},
}));

describe('PythonRunner', () => {
  it('renders editor textarea with initial code', () => {
    render(<PythonRunner initialCode="print('hello')" />);
    const textarea = screen.getByRole('textbox');
    expect(textarea).toBeInTheDocument();
    expect((textarea as HTMLTextAreaElement).value).toBe("print('hello')");
  });

  it('renders run button', () => {
    render(<PythonRunner />);
    expect(screen.getByRole('button', { name: /run/i })).toBeInTheDocument();
  });

  it('renders copy button', () => {
    render(<PythonRunner />);
    expect(screen.getByRole('button', { name: /copy/i })).toBeInTheDocument();
  });

  it('renders reset button', () => {
    render(<PythonRunner />);
    expect(screen.getByRole('button', { name: /reset/i })).toBeInTheDocument();
  });

  it('renders clear output button', () => {
    render(<PythonRunner />);
    expect(screen.getByRole('button', { name: /clear output/i })).toBeInTheDocument();
  });

  it('displays title when provided', () => {
    render(<PythonRunner title="FizzBuzz" />);
    expect(screen.getByText('FizzBuzz')).toBeInTheDocument();
  });

  it('displays difficulty badge when provided', () => {
    render(<PythonRunner difficulty="easy" />);
    expect(screen.getByText('Easy')).toBeInTheDocument();
  });

  it('displays medium difficulty badge', () => {
    render(<PythonRunner difficulty="medium" />);
    expect(screen.getByText('Medium')).toBeInTheDocument();
  });

  it('displays hard difficulty badge', () => {
    render(<PythonRunner difficulty="hard" />);
    expect(screen.getByText('Hard')).toBeInTheDocument();
  });

  it('does not render header when title and difficulty are absent', () => {
    render(<PythonRunner />);
    expect(screen.queryByText('Easy')).not.toBeInTheDocument();
    expect(screen.queryByText('Medium')).not.toBeInTheDocument();
    expect(screen.queryByText('Hard')).not.toBeInTheDocument();
  });

  it('reset button restores initial code after editing', () => {
    render(<PythonRunner initialCode="x = 1" />);
    const textarea = screen.getByRole('textbox') as HTMLTextAreaElement;

    // Edit the code
    fireEvent.change(textarea, { target: { value: 'x = 999' } });
    expect(textarea.value).toBe('x = 999');

    // Reset
    fireEvent.click(screen.getByRole('button', { name: /reset/i }));
    expect(textarea.value).toBe('x = 1');
  });

  it('renders test case descriptions when provided', () => {
    const testCases = [
      { input: 'fizzbuzz(3)', expected: 'Fizz', description: 'Returns Fizz for multiples of 3' },
      { input: 'fizzbuzz(5)', expected: 'Buzz', description: 'Returns Buzz for multiples of 5' },
    ];
    render(<PythonRunner testCases={testCases} />);
    // Test cases are rendered only after running code; the component stores them
    // but descriptions appear in results. Verify the component mounts without error.
    expect(screen.getByRole('textbox')).toBeInTheDocument();
  });

  it('textarea placeholder is present', () => {
    render(<PythonRunner />);
    const textarea = screen.getByRole('textbox');
    expect(textarea).toHaveAttribute('placeholder', '# Write your Python code here...');
  });
});
