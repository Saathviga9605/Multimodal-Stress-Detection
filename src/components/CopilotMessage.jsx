import React from "react";

export default function CopilotMessage({ stressLevel, explainability }) {
  const message =
    stressLevel === "High"
      ? "You seem a bit overwhelmed. Let's bring it down together."
      : stressLevel === "Moderate"
      ? "You are carrying moderate stress. A quick reset can help."
      : "You are in a stable state. Keep this calm rhythm going.";

  const topDrivers = Array.isArray(explainability?.top_drivers)
    ? explainability.top_drivers.slice(0, 3)
    : [];

  return (
    <div className="copilot-bubble slide-in-right">
      <strong>AI Insights</strong>
      <p>{message}</p>
      {explainability?.engine === "shap" && (
        <div style={{ marginTop: "0.35rem" }}>
          <small style={{ opacity: 0.9 }}>
            Explainability: SHAP {explainability?.available ? "enabled" : "unavailable"}
          </small>
        </div>
      )}

      {topDrivers.length > 0 && (
        <div style={{ marginTop: "0.5rem" }}>
          <small style={{ display: "block", marginBottom: "0.25rem" }}>Top stress drivers</small>
          {topDrivers.map((driver, idx) => (
            <div key={`${driver.modality}-${driver.feature_index}-${idx}`} style={{ fontSize: "0.85rem" }}>
              {driver.modality} / {driver.feature}: {driver.direction} ({driver.shap_value.toFixed(4)})
            </div>
          ))}
        </div>
      )}

      {explainability?.message && (
        <div style={{ marginTop: "0.35rem", fontSize: "0.85rem" }}>
          {explainability.message}
        </div>
      )}
    </div>
  );
}
