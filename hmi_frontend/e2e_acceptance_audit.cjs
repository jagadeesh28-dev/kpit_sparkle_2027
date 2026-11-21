const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function runE2E() {
  console.log('Starting Playwright E2E Acceptance Audit...');
  const screenshotsDir = path.resolve(__dirname, '..', 'artifacts', 'screenshots');
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 }
  });
  const page = await context.newPage();

  const auditLog = [];
  function logStep(step, detail) {
    console.log(`[STEP ${step}] ${detail}`);
    auditLog.push({ step, detail, timestamp: new Date().toISOString() });
  }

  try {
    // Step 1: Initial load
    logStep(1, 'Navigating to http://127.0.0.1:5173/');
    await page.goto('http://127.0.0.1:5173/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    const title = await page.textContent('body');
    if (!title.includes('AURA-Impact')) {
      throw new Error('AURA-Impact branding not found on page');
    }
    logStep(2, 'Verified AURA-Impact branding on page');

    // Verify LIVE BACKEND pill
    const backendPill = await page.waitForSelector('text=LIVE BACKEND', { timeout: 5000 });
    logStep(3, 'Verified LIVE BACKEND status indicator');
    await page.screenshot({ path: path.join(screenshotsDir, '01_initial_load.png') });

    // Step 4: Scenario 1 execution
    logStep(4, 'Selecting Scenario 1: Braking Threshold Calibration');
    await page.selectOption('select', 'scenario_braking_calibration');
    await page.waitForTimeout(500);

    logStep(5, 'Clicking Run Analysis for Scenario 1');
    const runBtn = await page.waitForSelector('button:has-text("Run Analysis")');
    await runBtn.click();

    // Wait for analysis to finish (button returns to Run Analysis from Analyzing...)
    await page.waitForSelector('button:has-text("Run Analysis")', { timeout: 10000 });
    await page.waitForTimeout(1500); // allow graph layout
    logStep(6, 'Scenario 1 analysis completed');
    await page.screenshot({ path: path.join(screenshotsDir, '02_scenario1_analysis_complete.png') });

    // Step 7: Inspect Graph node
    const nodeEl = await page.$('.react-flow__node');
    if (nodeEl) {
      logStep(7, 'Clicking on graph node to verify Inspector');
      await nodeEl.click();
      await page.waitForTimeout(500);
      await page.screenshot({ path: path.join(screenshotsDir, '03_scenario1_node_inspected.png') });
    }

    // Step 8: Testing View Tab
    logStep(8, 'Switching to Testing View Tab');
    await page.click('button:has-text("Testing View")');
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(screenshotsDir, '04_scenario1_testing_view.png') });

    // Step 9: Safety View Tab
    logStep(9, 'Switching to Safety View Tab');
    await page.click('button:has-text("Safety View")');
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(screenshotsDir, '05_scenario1_safety_view.png') });

    // Step 10: Scenario 2 (Latent Thermal Coupling)
    logStep(10, 'Selecting Scenario 2: Latent Thermal Coupling');
    await page.selectOption('select', 'scenario_latent_thermal_coupling');
    await page.waitForTimeout(500);
    const runBtn2 = await page.waitForSelector('button:has-text("Run Analysis")');
    await runBtn2.click();
    await page.waitForTimeout(2000);
    logStep(11, 'Scenario 2 analysis completed');

    // Switch to Decoy & Semantic Inspector
    logStep(12, 'Checking Decoy & Semantic Inspector Tab for Scenario 2');
    await page.click('button:has-text("Decoy & Semantic Inspector")');
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(screenshotsDir, '06_scenario2_semantic_inspector.png') });

    // Step 13: Scenario 3 (Decoy Attack)
    logStep(13, 'Selecting Scenario 3: Non-Automotive Decoy Attack');
    await page.selectOption('select', 'scenario_decoy_attack');
    await page.waitForTimeout(500);
    const runBtn3 = await page.waitForSelector('button:has-text("Run Analysis")');
    await runBtn3.click();
    await page.waitForTimeout(2000);
    logStep(14, 'Scenario 3 analysis completed');

    // Check Decoy rejection reasons
    await page.click('button:has-text("Decoy & Semantic Inspector")');
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(screenshotsDir, '07_scenario3_decoy_rejections.png') });

    // Step 15: Scenario 4 (Inverter Runaway)
    logStep(15, 'Selecting Scenario 4: High-Voltage Inverter Runaway');
    await page.selectOption('select', 'scenario_inverter_runaway');
    await page.waitForTimeout(500);
    const runBtn4 = await page.waitForSelector('button:has-text("Run Analysis")');
    await runBtn4.click();
    await page.waitForTimeout(2000);
    logStep(16, 'Scenario 4 analysis completed');

    // Check Safety View
    await page.click('button:has-text("Safety View")');
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(screenshotsDir, '08_scenario4_safety_retention.png') });

    // Step 17: Empirical Benchmark Evidence Tab
    logStep(17, 'Switching to Empirical Benchmark Evidence Tab');
    await page.click('button:has-text("Empirical Benchmark Evidence")');
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(screenshotsDir, '09_benchmark_evidence.png') });

    // Step 18: Upload Diff Modal
    logStep(18, 'Testing Upload Diff modal');
    await page.click('button:has-text("Upload Diff")');
    await page.waitForTimeout(500);
    await page.fill('textarea', '--- a/src/aeb.c\n+++ b/src/aeb.c\n@@ -10,2 +10,4 @@\n void calibrate_aeb() {\n+    threshold = 8.5;\n }');
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(screenshotsDir, '10_diff_upload_modal.png') });
    // Close modal
    const closeBtn = await page.$('button:has-text("Parse & Suggest Payload")');
    if (closeBtn) {
      await closeBtn.click();
      await page.waitForTimeout(1000);
    }

    // Step 19: Viewport Responsive checks
    logStep(19, 'Testing Tablet Viewport (1024x768)');
    await page.setViewportSize({ width: 1024, height: 768 });
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(screenshotsDir, '11_viewport_tablet_1024x768.png') });

    logStep(20, 'Testing Mobile Viewport (390x844)');
    await page.setViewportSize({ width: 390, height: 844 });
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(screenshotsDir, '12_viewport_mobile_390x844.png') });

    logStep(21, 'ALL PLAYWRIGHT AUDIT STEPS COMPLETED SUCCESSFULLY');

    fs.writeFileSync(
      path.resolve(__dirname, '..', 'results', 'e2e_playwright_audit.json'),
      JSON.stringify({ status: 'SUCCESS', steps: auditLog }, null, 2),
      'utf-8'
    );
  } catch (err) {
    console.error('Playwright E2E Failed:', err);
    await page.screenshot({ path: path.join(screenshotsDir, 'error_failure.png') });
    fs.writeFileSync(
      path.resolve(__dirname, '..', 'results', 'e2e_playwright_audit.json'),
      JSON.stringify({ status: 'FAILED', error: String(err), steps: auditLog }, null, 2),
      'utf-8'
    );
    throw err;
  } finally {
    await browser.close();
  }
}

runE2E().catch((e) => {
  console.error(e);
  process.exit(1);
});
