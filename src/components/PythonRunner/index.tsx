import React, {useState, useRef, useCallback} from 'react';
import styles from './styles.module.css';

interface TestCase {
  input: string;
  expected: string;
  description: string;
}

interface TestResult {
  passed: boolean;
  description: string;
  expected: string;
  actual: string;
}

interface PythonRunnerProps {
  initialCode?: string;
  testCases?: TestCase[];
  title?: string;
  difficulty?: 'easy' | 'medium' | 'hard';
}

// Shared Pyodide instance across all PythonRunner components
let pyodidePromise: Promise<any> | null = null;

function loadPyodideScript(): Promise<void> {
  return new Promise((resolve, reject) => {
    if ((window as any).loadPyodide) {
      resolve();
      return;
    }
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/pyodide/v0.27.0/full/pyodide.js';
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Failed to load Pyodide script'));
    document.head.appendChild(script);
  });
}

async function getPyodide() {
  if (!pyodidePromise) {
    pyodidePromise = (async () => {
      await loadPyodideScript();
      const pyodide = await (window as any).loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.0/full/',
      });
      return pyodide;
    })();
  }
  return pyodidePromise;
}

export default function PythonRunner({
  initialCode = '',
  testCases,
  title,
  difficulty,
}: PythonRunnerProps): React.ReactElement {
  const [code, setCode] = useState(initialCode);
  const [output, setOutput] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [testResults, setTestResults] = useState<TestResult[] | null>(null);
  const [copied, setCopied] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const runCode = useCallback(async () => {
    setIsRunning(true);
    setOutput('');
    setError('');
    setTestResults(null);

    try {
      setIsLoading(true);
      const pyodide = await getPyodide();
      setIsLoading(false);

      // Capture stdout and stderr
      pyodide.runPython(`
import sys
import io
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
`);

      // Run user code with a timeout
      const runWithTimeout = async (): Promise<void> => {
        return new Promise<void>((resolve, reject) => {
          const timer = setTimeout(() => {
            reject(new Error('Execution timed out (5 second limit). Possible infinite loop?'));
          }, 5000);

          try {
            pyodide.runPython(code);
            clearTimeout(timer);
            resolve();
          } catch (err) {
            clearTimeout(timer);
            reject(err);
          }
        });
      };

      await runWithTimeout();

      const stdout = pyodide.runPython('sys.stdout.getvalue()');
      const stderr = pyodide.runPython('sys.stderr.getvalue()');

      setOutput(stdout || '');
      if (stderr) {
        setError(stderr);
      }

      // Run test cases if provided
      if (testCases && testCases.length > 0) {
        const results: TestResult[] = [];
        for (const tc of testCases) {
          try {
            const result = pyodide.runPython(`str(${tc.input})`);
            const actual = String(result);
            results.push({
              passed: actual === tc.expected,
              description: tc.description,
              expected: tc.expected,
              actual,
            });
          } catch (err: any) {
            results.push({
              passed: false,
              description: tc.description,
              expected: tc.expected,
              actual: `Error: ${err.message}`,
            });
          }
        }
        setTestResults(results);
      }
    } catch (err: any) {
      setIsLoading(false);
      const msg = err.message || String(err);
      // Clean up Pyodide traceback noise
      const cleanMsg = msg.includes('PythonError')
        ? msg.split('\n').filter((line: string) => !line.includes('at new PythonError') && !line.includes('at Object.callKwargs')).join('\n').trim()
        : msg;
      setError(cleanMsg);
    } finally {
      setIsRunning(false);
    }
  }, [code, testCases]);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
      const textarea = document.createElement('textarea');
      textarea.value = code;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [code]);

  const handleReset = useCallback(() => {
    setCode(initialCode);
    setOutput('');
    setError('');
    setTestResults(null);
  }, [initialCode]);

  const handleClear = useCallback(() => {
    setOutput('');
    setError('');
    setTestResults(null);
  }, []);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      // Tab support
      if (e.key === 'Tab') {
        e.preventDefault();
        const target = e.target as HTMLTextAreaElement;
        const start = target.selectionStart;
        const end = target.selectionEnd;
        const newCode = code.substring(0, start) + '    ' + code.substring(end);
        setCode(newCode);
        // Restore cursor
        requestAnimationFrame(() => {
          target.selectionStart = target.selectionEnd = start + 4;
        });
      }
      // Ctrl/Cmd + Enter to run
      if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        runCode();
      }
    },
    [code, runCode],
  );

  const difficultyLabel = difficulty
    ? {easy: 'Easy', medium: 'Medium', hard: 'Hard'}[difficulty]
    : null;

  const difficultyClass = difficulty
    ? {easy: styles.badgeEasy, medium: styles.badgeMedium, hard: styles.badgeHard}[difficulty]
    : '';

  return (
    <div className={styles.container}>
      {/* Header */}
      {(title || difficulty) && (
        <div className={styles.header}>
          <div className={styles.titleGroup}>
            {title && <span className={styles.title}>{title}</span>}
            {difficultyLabel && (
              <span className={`${styles.badge} ${difficultyClass}`}>{difficultyLabel}</span>
            )}
          </div>
        </div>
      )}

      {/* Editor */}
      <textarea
        ref={textareaRef}
        className={styles.editor}
        value={code}
        onChange={(e) => setCode(e.target.value)}
        onKeyDown={handleKeyDown}
        spellCheck={false}
        placeholder="# Write your Python code here..."
      />

      {/* Toolbar */}
      <div className={styles.toolbar}>
        <button
          className={`${styles.btn} ${styles.btnRun}`}
          onClick={runCode}
          disabled={isRunning}
        >
          {isRunning ? (isLoading ? 'Loading Python...' : 'Running...') : 'Run'}
        </button>
        <button className={`${styles.btn} ${styles.btnCopy}`} onClick={handleCopy}>
          {copied ? 'Copied!' : 'Copy'}
        </button>
        <button className={`${styles.btn} ${styles.btnReset}`} onClick={handleReset}>
          Reset
        </button>
        <button className={`${styles.btn} ${styles.btnClear}`} onClick={handleClear}>
          Clear Output
        </button>
      </div>

      {/* Loading indicator */}
      {isLoading && (
        <div className={styles.loading}>
          <span className={styles.spinner} />
          Loading Python environment...
        </div>
      )}

      {/* Output */}
      {(output || error) && (
        <div className={styles.outputSection}>
          <div className={styles.outputHeader}>Output</div>
          <div className={styles.outputBody}>
            {output && <span>{output}</span>}
            {error && <span className={styles.errorText}>{error}</span>}
          </div>
        </div>
      )}

      {/* Test Results */}
      {testResults && testResults.length > 0 && (
        <div className={styles.testSection}>
          <div className={styles.testHeader}>
            Test Results ({testResults.filter((t) => t.passed).length}/{testResults.length} passed)
          </div>
          <ul className={styles.testList}>
            {testResults.map((result, i) => (
              <li key={i} className={styles.testItem}>
                <span className={result.passed ? styles.testPass : styles.testFail}>
                  {result.passed ? '\u2713' : '\u2717'}
                </span>
                <div className={styles.testDetails}>
                  <span className={styles.testDescription}>{result.description}</span>
                  {!result.passed && (
                    <span className={styles.testExpected}>
                      Expected: {result.expected} | Got: {result.actual}
                    </span>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
