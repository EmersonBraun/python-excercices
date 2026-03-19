import { test, expect } from '@playwright/test';

test('homepage loads with hero', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('Python From Zero to Hero');
});

test('navigate to beginner module', async ({ page }) => {
  await page.goto('/docs/');
  await expect(page.locator('text=Beginner')).toBeVisible();
});

test('navigate to intermediate module', async ({ page }) => {
  await page.goto('/docs/');
  await expect(page.locator('text=Intermediate')).toBeVisible();
});
