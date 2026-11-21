import axios from 'axios';

const API_URL = 'http://localhost:8000';

export interface AnalysisRequest {
  artifact_id: string;
  artifact_type: string;
  subsystem: string;
  ecu: string;
  change_type: string;
  after_content: string;
  change_semantics: string;
  force_semantic?: boolean;
  filter_subsystem?: boolean;
  threshold_override?: number;
}

export interface ScenarioPreset {
  id: string;
  name: string;
  category: string;
  subsystem: string;
  ecu: string;
  artifact_id: string;
  artifact_type: string;
  change_type: string;
  after_content: string;
  change_semantics: string;
  purpose: string;
  expected_behavior: string;
  force_semantic: boolean;
  filter_subsystem: boolean;
}

export interface SemanticCandidate {
  artifact_id: string;
  artifact_type: string;
  subsystem: string;
  ecu: string;
  similarity_score: number;
  context_score: number;
  status: 'ACCEPT' | 'REJECT' | 'REVIEW_REQUIRED';
  rejection_reason: string;
  source_file: string;
}

export interface SelectedTest {
  test_id: string;
  description: string;
  safety_class: string;
  subsystem: string;
  mapped_from_artifact: string;
  mapping_source: string;
  source_file?: string;
}

export interface SafetyGateStatus {
  status: string;
  retained_count: number;
  invariant_asserted: boolean;
  fail_closed_policy: string;
}

export interface BenchmarkFigure {
  id: string;
  name: string;
  file: string;
  url: string;
}

export interface BenchmarkData {
  status: string;
  summary_table: Array<Record<string, string>>;
  datasets: {
    dronology: Array<Record<string, string>>;
    defects4j: Array<Record<string, string>>;
    autoware: Array<Record<string, string>>;
    alexandria: Array<Record<string, string>>;
  };
  figures: BenchmarkFigure[];
  evidence_provenance: {
    evaluation_timestamp?: string;
    git_commit?: string;
    sha256?: string;
  };
  limitations: string[];
}

export interface DiffUploadResult {
  status: string;
  parsed_summary: {
    changed_files: string[];
    detected_identifiers: string[];
    mapped_artifact_id: string;
    inferred_type: string;
    subsystem: string;
    ecu: string;
  };
  suggested_request: AnalysisRequest;
}

// ----------------------------------------------------------------------------
// API CALLS
// ----------------------------------------------------------------------------

export const checkHealth = async () => {
  const response = await axios.get(`${API_URL}/health`, { timeout: 3000 });
  return response.data;
};

export const fetchScenarios = async (): Promise<ScenarioPreset[]> => {
  const response = await axios.get(`${API_URL}/scenarios`, { timeout: 4000 });
  return response.data.scenarios;
};

export const runAnalysis = async (request: AnalysisRequest) => {
  const response = await axios.post(`${API_URL}/analyze`, request, { timeout: 15000 });
  return response.data;
};

export const fetchBenchmarks = async (): Promise<BenchmarkData> => {
  const response = await axios.get(`${API_URL}/benchmarks`, { timeout: 5000 });
  return response.data;
};

export const uploadDiff = async (diff_content: string, subsystem: string = 'ADAS', ecu: string = 'VCU'): Promise<DiffUploadResult> => {
  const response = await axios.post(`${API_URL}/upload-diff`, {
    diff_content,
    subsystem,
    ecu
  }, { timeout: 5000 });
  return response.data;
};

export const fetchAnalysisById = async (analysisId: string) => {
  const response = await axios.get(`${API_URL}/analysis/${analysisId}`, { timeout: 4000 });
  return response.data;
};
