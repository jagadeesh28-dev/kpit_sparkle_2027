import { useState } from "react";
import {
  Shield, Play, Upload, RotateCcw,
  AlertCircle, ChevronDown, FileCode, X
} from "lucide-react";
import { uploadDiff } from "../api";
import type { ScenarioPreset } from "../api";

interface CommandBarProps {
  scenarios: ScenarioPreset[];
  selectedScenario: ScenarioPreset | null;
  onSelectScenario: (s: ScenarioPreset) => void;
  onRunAnalysis: () => void;
  onReset: () => void;
  isLoading: boolean;
  isBackendConnected: boolean;
  onDiffUploaded: (suggestedRequest: any) => void;
}

export default function CommandBar({
  scenarios,
  selectedScenario,
  onSelectScenario,
  onRunAnalysis,
  onReset,
  isLoading,
  isBackendConnected,
  onDiffUploaded
}: CommandBarProps) {
  const [showDiffModal, setShowDiffModal] = useState(false);
  const [diffText, setDiffText] = useState("");
  const [diffSubsystem, setDiffSubsystem] = useState("ADAS");
  const [diffEcu, setDiffEcu] = useState("VCU");
  const [diffError, setDiffError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleUploadDiffSubmit = async () => {
    if (!diffText.trim()) {
      setDiffError("Please paste a valid unified diff or C/C++ function patch.");
      return;
    }
    setDiffError(null);
    setIsUploading(true);
    try {
      const res = await uploadDiff(diffText, diffSubsystem, diffEcu);
      setShowDiffModal(false);
      setDiffText("");
      onDiffUploaded(res.suggested_request);
    } catch (err: any) {
      setDiffError(err?.response?.data?.detail || "Failed to parse diff.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <>
      <div className="h-14 bg-[#0b3d54] text-white flex items-center px-4 justify-between select-none shrink-0 z-40 shadow-md border-b border-[#144f6d]">
        {/* Left: Branding & Scenario Selector */}
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-teal-500/20 border border-teal-400 flex items-center justify-center">
              <Shield className="w-5 h-5 text-teal-400" />
            </div>
            <div className="flex flex-col leading-none">
              <span className="text-sm font-bold tracking-wider">AURA-Impact</span>
              <span className="text-[10px] text-teal-300/80 font-medium tracking-wide">Automotive Change Intelligence</span>
            </div>
          </div>

          <div className="h-6 w-px bg-white/20"></div>

          {/* Scenario Presets Selector */}
          <div className="flex items-center space-x-2">
            <span className="text-xs text-gray-300 font-medium">Scenario:</span>
            <div className="relative">
              <select
                value={selectedScenario?.id || ""}
                onChange={(e) => {
                  const found = scenarios.find((s) => s.id === e.target.value);
                  if (found) onSelectScenario(found);
                }}
                className="bg-[#124d68] hover:bg-[#165a78] border border-teal-400/30 text-white text-xs rounded px-2.5 py-1.5 pr-8 appearance-none focus:outline-none focus:ring-1 focus:ring-teal-400 cursor-pointer font-medium"
              >
                {scenarios.map((s) => (
                  <option key={s.id} value={s.id} className="bg-[#0b3d54] text-white">
                    {s.name} ({s.subsystem})
                  </option>
                ))}
              </select>
              <ChevronDown className="w-3.5 h-3.5 text-teal-300 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>
          </div>

          {/* Active Artifact Indicator */}
          {selectedScenario && (
            <div className="hidden lg:flex items-center space-x-2 bg-black/20 border border-white/10 rounded px-2.5 py-1 text-xs">
              <span className="text-gray-400">Target:</span>
              <span className="font-mono text-teal-300 font-bold">{selectedScenario.artifact_id}</span>
              <span className="text-gray-400">|</span>
              <span className="text-gray-300">{selectedScenario.subsystem} / {selectedScenario.ecu}</span>
            </div>
          )}
        </div>

        {/* Right: Actions & Connection Badge */}
        <div className="flex items-center space-x-3">
          {/* Connection Status Pill */}
          <div
            className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold border ${
              isBackendConnected
                ? "bg-emerald-950/60 border-emerald-500/50 text-emerald-400"
                : "bg-amber-950/60 border-amber-500/50 text-amber-300"
            }`}
            title={isBackendConnected ? "Connected to FastAPI port 8000" : "Operating in Offline Demonstration mode"}
          >
            <div
              className={`w-2 h-2 rounded-full ${
                isBackendConnected ? "bg-emerald-400 animate-pulse" : "bg-amber-400"
              }`}
            ></div>
            <span>{isBackendConnected ? "LIVE BACKEND" : "OFFLINE DEMO"}</span>
          </div>

          {/* Upload Git Diff Button */}
          <button
            onClick={() => setShowDiffModal(true)}
            className="flex items-center space-x-1.5 bg-[#144f6d] hover:bg-[#195e82] border border-white/20 text-white text-xs px-3 py-1.5 rounded transition font-medium"
            title="Upload arbitrary Git unified diff or C/C++ patch"
          >
            <Upload className="w-3.5 h-3.5 text-teal-300" />
            <span>Upload Diff</span>
          </button>

          {/* Reset Button */}
          <button
            onClick={onReset}
            className="flex items-center space-x-1 bg-white/10 hover:bg-white/20 text-gray-300 hover:text-white text-xs px-2.5 py-1.5 rounded transition"
            title="Reset scenario state"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>

          {/* Run Analysis Button */}
          <button
            onClick={onRunAnalysis}
            disabled={isLoading}
            className="flex items-center space-x-2 bg-teal-600 hover:bg-teal-500 active:bg-teal-700 disabled:opacity-50 text-white text-xs font-semibold px-4 py-1.5 rounded shadow-sm transition cursor-pointer"
          >
            {isLoading ? (
              <>
                <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Run Analysis</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Upload Git Diff Modal */}
      {showDiffModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-[#0f2e3d] border border-teal-500/40 rounded-lg shadow-2xl max-w-2xl w-full p-5 text-white flex flex-col space-y-4">
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <div className="flex items-center space-x-2">
                <FileCode className="w-5 h-5 text-teal-400" />
                <h3 className="text-sm font-bold tracking-wide">Upload Unified Git Diff / Patch</h3>
              </div>
              <button
                onClick={() => setShowDiffModal(false)}
                className="text-gray-400 hover:text-white transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-gray-300 leading-relaxed">
              Paste a unified Git diff or modified C/C++ function. The backend will safely parse changed identifiers, map them to repository graph nodes, and construct a targeted change impact query.
            </p>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div>
                <label className="text-gray-300 block mb-1">Subsystem:</label>
                <select
                  value={diffSubsystem}
                  onChange={(e) => setDiffSubsystem(e.target.value)}
                  className="w-full bg-[#08222d] border border-white/20 rounded px-2 py-1.5 text-white"
                >
                  <option value="ADAS">ADAS (Advanced Driver Assistance)</option>
                  <option value="POWERTRAIN">POWERTRAIN (BMS / Inverter)</option>
                  <option value="CHASSIS">CHASSIS (Braking / Steering)</option>
                  <option value="BODY">BODY (Lighting / Comfort)</option>
                </select>
              </div>
              <div>
                <label className="text-gray-300 block mb-1">ECU:</label>
                <input
                  type="text"
                  value={diffEcu}
                  onChange={(e) => setDiffEcu(e.target.value)}
                  className="w-full bg-[#08222d] border border-white/20 rounded px-2 py-1.5 text-white"
                />
              </div>
            </div>

            <div>
              <label className="text-gray-300 block mb-1 text-xs">Diff / Patch Content:</label>
              <textarea
                value={diffText}
                onChange={(e) => setDiffText(e.target.value)}
                placeholder={`--- a/src/aeb_controller.c\n+++ b/src/aeb_controller.c\n@@ -12,4 +12,6 @@\n void calibrate_aeb_threshold() {\n+    aeb_decel_threshold = 8.5;\n }`}
                rows={8}
                className="w-full bg-[#08222d] border border-white/20 rounded p-2.5 font-mono text-xs text-gray-100 placeholder-gray-500 focus:outline-none focus:border-teal-400"
              />
            </div>

            {diffError && (
              <div className="flex items-center space-x-2 text-xs text-red-300 bg-red-950/60 border border-red-500/40 p-2.5 rounded">
                <AlertCircle className="w-4 h-4 shrink-0 text-red-400" />
                <span>{diffError}</span>
              </div>
            )}

            <div className="flex justify-end space-x-3 pt-2">
              <button
                onClick={() => setShowDiffModal(false)}
                className="px-4 py-1.5 bg-white/10 hover:bg-white/20 text-gray-200 text-xs rounded transition"
              >
                Cancel
              </button>
              <button
                onClick={handleUploadDiffSubmit}
                disabled={isUploading}
                className="px-4 py-1.5 bg-teal-600 hover:bg-teal-500 text-white text-xs font-semibold rounded shadow transition disabled:opacity-50"
              >
                {isUploading ? "Parsing..." : "Parse & Load Change"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
