// Standard Node Playwright spec for TaskFlow Pro existing suite
const { test, expect } = require('@playwright/test');

const BASE_URL = process.env.TARGET_APP_URL || 'http://127.0.0.1:4173';

test('initial board renders 3 tasks and 21 velocity pts', async ({ page }) => {
  await page.goto(BASE_URL);
  await expect(page.locator('#active-count')).toHaveText('3');
  await expect(page.locator('#velocity-pts')).toHaveText('21');
  await expect(page.locator('.task-card')).toHaveCount(3);
});

test('adding a new task increments active task count and velocity', async ({ page }) => {
  await page.goto(BASE_URL);
  await page.fill('#new-task-title', 'Deploy canary build');
  await page.fill('#new-task-pts', '5');
  await page.click('#btn-add-task');
  await expect(page.locator('.task-card')).toHaveCount(4);
  await expect(page.locator('#active-count')).toHaveText('4');
  await expect(page.locator('#velocity-pts')).toHaveText('26');
});

test('estimate calculation without percentage symbol succeeds', async ({ page }) => {
  await page.goto(BASE_URL);
  await page.fill('#est-hours', '10');
  await page.fill('#est-rate', '100');
  await page.fill('#est-discount', '0');
  await page.click('#btn-calc-estimate');
  await expect(page.locator('#estimate-total')).toHaveText('$1,000.00');
});
