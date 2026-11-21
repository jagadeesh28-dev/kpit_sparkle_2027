import { describe, it, expect } from 'vitest';
import type { ScenarioPreset, SemanticCandidate, SelectedTest } from '../api';

describe('Frontend API Contract & Types', () => {
  it('validates scenario preset schema structure', () => {
    const samplePreset: ScenarioPreset = {
      id: 'scenario_braking_calibration',
      name: 'Scenario 1: Braking Threshold Calibration',
      category: 'Structural Traversal',
      subsystem: 'ADAS',
      ecu: 'VCU',
      artifact_id: 'REQ_AEB_001',
      artifact_type: 'Requirement',
      change_type: 'MODIFICATION',
      after_content: 'void test() {}',
      change_semantics: 'Braking calibration update',
      purpose: 'Demonstrate deterministic impact',
      expected_behavior: 'Structural propagation complete',
      force_semantic: false,
      filter_subsystem: true,
    };

    expect(samplePreset.id).toBe('scenario_braking_calibration');
    expect(samplePreset.subsystem).toBe('ADAS');
    expect(samplePreset.force_semantic).toBe(false);
  });

  it('validates semantic candidate status and rejection reason', () => {
    const candidate: SemanticCandidate = {
      artifact_id: 'INFOTAINMENT_SERVICE',
      artifact_type: 'SoftwareComponent',
      subsystem: 'INFOTAINMENT',
      ecu: 'COCKPIT',
      similarity_score: 0.72,
      context_score: 0.0,
      status: 'REJECT',
      rejection_reason: 'REJECT_SUBSYSTEM_MISMATCH',
      source_file: 'infotainment.c',
    };

    expect(candidate.status).toBe('REJECT');
    expect(candidate.rejection_reason).toContain('REJECT_SUBSYSTEM_MISMATCH');
    expect(candidate.similarity_score).toBeGreaterThan(0.7);
  });

  it('validates selected test structure and safety classification', () => {
    const testItem: SelectedTest = {
      test_id: 'TC-SAF-0007',
      description: 'Safe state emergency deceleration',
      safety_class: 'ASIL-D',
      subsystem: 'ADAS',
      mapped_from_artifact: 'SWC_AccController',
      mapping_source: 'MANDATORY_SAFETY_GATE',
    };

    expect(testItem.safety_class).toBe('ASIL-D');
    expect(testItem.mapping_source).toBe('MANDATORY_SAFETY_GATE');
  });
});

describe('Domain Formatting & ASIL Normalization', () => {
  function normalizeAsil(level: string): string {
    if (!level) return 'QM';
    return level.replace('ASIL_', 'ASIL-');
  }

  it('normalizes various ASIL string formats', () => {
    expect(normalizeAsil('ASIL_D')).toBe('ASIL-D');
    expect(normalizeAsil('ASIL-D')).toBe('ASIL-D');
    expect(normalizeAsil('ASIL_C')).toBe('ASIL-C');
    expect(normalizeAsil('')).toBe('QM');
  });
});
