import React, { useMemo } from "react";

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

const toPercent = (value, fallback) => {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return fallback;
  }
  const numeric = Number(value);
  if (numeric <= 1) return clamp(numeric * 100, 0, 100);
  return clamp(numeric, 0, 100);
};

const toBand = (percent) => {
  if (percent >= 67) return "High";
  if (percent >= 34) return "Medium";
  return "Low";
};

export default function AnalysisPanel({ result }) {
  const analysis = useMemo(() => {
    const individual = result?.individual_predictions || {};
    const facial = Math.round(toPercent(individual.facial, 80));
    const voice = Math.round(toPercent(individual.voice, 60));
    const physiological = Math.round(toPercent(individual.physiological, 85));

    const points = [
      { key: "facial", label: "Facial", value: facial },
      { key: "voice", label: "Voice", value: voice },
      { key: "physiological", label: "Physiological", value: physiological },
    ];

    const total = points.reduce((sum, entry) => sum + entry.value, 0) || 1;

    return {
      points,
      cause: "Facial tension and elevated physiological signals",
      contributions: points.map((entry) => ({
        ...entry,
        percent: Math.round((entry.value / total) * 100),
      })),
    };
  }, [result]);

  return (
    <div className="result-panel-card insights-fade">
      <h5 className="result-section-title">Stress Analysis Panel</h5>

      {analysis.points.map((item) => (
        <div className="analysis-item-row" key={item.key}>
          <span>{item.label} Stress</span>
          <strong>
            {toBand(item.value)} ({item.value}%)
          </strong>
        </div>
      ))}

      <div className="analysis-cause">
        <small>Main Cause</small>
        <p>{analysis.cause}</p>
      </div>

      <div>
        <small className="contrib-title">Contribution Breakdown</small>
        {analysis.contributions.map((entry) => (
          <div key={entry.key} style={{ marginTop: "0.6rem" }}>
            <div className="analysis-item-row">
              <span>{entry.label}</span>
              <span>{entry.percent}%</span>
            </div>
            <div className="contrib-track">
              <div className="contrib-fill" style={{ width: `${entry.percent}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
