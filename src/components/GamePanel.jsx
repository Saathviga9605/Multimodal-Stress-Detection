import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import BreathingExercise from "./BreathingExercise";

export default function GamePanel({
  stressLevel,
  isGameActive,
  setIsGameActive,
  selectedActivity,
  setSelectedActivity,
  onActivityComplete,
}) {
  const [tapCount, setTapCount] = useState(0);
  const [calmSecondsLeft, setCalmSecondsLeft] = useState(120);
  const [isCalmRunning, setIsCalmRunning] = useState(false);
  const [playCalmSound, setPlayCalmSound] = useState(false);
  const [gratitudeText, setGratitudeText] = useState("");
  const [postureChecks, setPostureChecks] = useState({
    shoulders: false,
    jaw: false,
    breathing: false,
  });
  const audioRef = useRef(null);
  const tapTarget = 8;

  const shouldShowGames = stressLevel === "High" || stressLevel === "Moderate";

  const activityTitle = useMemo(() => {
    if (selectedActivity === "breathing") return "Breathing Game";
    if (selectedActivity === "focus") return "Focus Tap Game";
    if (selectedActivity === "calm") return "Calm Mode";
    if (selectedActivity === "gratitude") return "Gratitude Game";
    if (selectedActivity === "posture") return "Posture Reset Game";
    return "";
  }, [selectedActivity]);

  const panelTitle =
    stressLevel === "High" ? "Choose a quick reset activity" : "Try a quick reset activity";

  const panelDescription =
    stressLevel === "High"
      ? "Select one mini-experience to regulate stress and recover focus."
      : "A short guided activity can lower moderate stress and improve focus.";

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
      .toString()
      .padStart(2, "0");
    const secs = (seconds % 60).toString().padStart(2, "0");
    return `${mins}:${secs}`;
  };

  const stopCalmAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
  };

  const startCalmAudio = () => {
    if (audioRef.current) {
      audioRef.current.volume = 0.35;
      audioRef.current.play().catch(() => {
        // Browser autoplay policy may block playback until user interaction.
      });
    }
  };

  const completeActivity = useCallback((activityName, reducedBy = 28, scoreBoost = 13, streakBoost = 2) => {
    if (onActivityComplete) {
      onActivityComplete({
        activityName,
        reducedBy,
        scoreBoost,
        streakBoost,
      });
    }
    setSelectedActivity(null);
    setTapCount(0);
    setCalmSecondsLeft(120);
    setIsCalmRunning(false);
    setPlayCalmSound(false);
    setGratitudeText("");
    setPostureChecks({ shoulders: false, jaw: false, breathing: false });
    stopCalmAudio();
  }, [onActivityComplete, setSelectedActivity]);

  useEffect(() => {
    if (selectedActivity !== "calm") {
      setIsCalmRunning(false);
      setCalmSecondsLeft(120);
      setPlayCalmSound(false);
      stopCalmAudio();
      return;
    }

    return () => stopCalmAudio();
  }, [selectedActivity]);

  useEffect(() => {
    if (!isCalmRunning || selectedActivity !== "calm") return;

    const timer = setInterval(() => {
      setCalmSecondsLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          setIsCalmRunning(false);
          setPlayCalmSound(false);
          stopCalmAudio();
          completeActivity("Calm Mode", 24, 12, 2);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isCalmRunning, selectedActivity, completeActivity]);

  useEffect(() => {
    if (selectedActivity !== "calm") return;

    if (isCalmRunning && playCalmSound) {
      startCalmAudio();
    } else {
      stopCalmAudio();
    }
  }, [isCalmRunning, playCalmSound, selectedActivity]);

  useEffect(() => {
    return () => stopCalmAudio();
  }, []);

  if (!shouldShowGames) return null;

  return (
    <div className="intervention-panel fade-in-up">
      <h5 style={{ marginBottom: "0.5rem" }}>{panelTitle}</h5>
      <p style={{ marginBottom: "1rem" }}>
        {panelDescription}
      </p>

      {!isGameActive && (
        <button className="btn btn-neon" onClick={() => setIsGameActive(true)}>
          Open Reset Activities
        </button>
      )}

      {isGameActive && (
        <>
          <div className="intervention-actions">
            <button className="btn btn-neon" onClick={() => setSelectedActivity("breathing")}>
              Breathing Game
            </button>
            <button className="btn btn-outline-neon" onClick={() => setSelectedActivity("focus")}>
              Focus Tap Game
            </button>
            <button className="btn btn-outline-neon" onClick={() => setSelectedActivity("calm")}>
              Calm Mode
            </button>
            <button className="btn btn-outline-neon" onClick={() => setSelectedActivity("gratitude")}>
              Gratitude Game
            </button>
            <button className="btn btn-outline-neon" onClick={() => setSelectedActivity("posture")}>
              Posture Reset
            </button>
            <button
              className="btn btn-outline-neon"
              onClick={() => {
                setSelectedActivity(null);
                setTapCount(0);
                setCalmSecondsLeft(120);
                setIsCalmRunning(false);
                setPlayCalmSound(false);
                setGratitudeText("");
                setPostureChecks({ shoulders: false, jaw: false, breathing: false });
                stopCalmAudio();
                setIsGameActive(false);
              }}
            >
              Dismiss
            </button>
          </div>

          {selectedActivity && <p className="activity-label">Active: {activityTitle}</p>}

          {selectedActivity === "breathing" && (
            <BreathingExercise
              isActive
              totalCycles={5}
              onComplete={() => completeActivity("Breathing Game")}
            />
          )}

          {selectedActivity === "focus" && (
            <div className="focus-tap-panel">
              <p>Tap slowly to match your breathing.</p>
              <button
                className="focus-dot"
                onClick={() => {
                  setTapCount((prev) => {
                    const next = prev + 1;
                    if (next >= tapTarget) {
                      completeActivity("Focus Tap Game", 22, 10, 1);
                      return tapTarget;
                    }
                    return next;
                  });
                }}
              >
                Tap
              </button>
              <small>{tapCount}/{tapTarget} taps completed</small>
            </div>
          )}

          {selectedActivity === "calm" && (
            <div className="calm-mode-surface">
              <p>Relax your shoulders. Unclench your jaw.</p>
              <p className="calm-timer">Timer: {formatTime(calmSecondsLeft)}</p>
              <div className="intervention-actions" style={{ marginTop: "0.5rem" }}>
                {!isCalmRunning ? (
                  <button className="btn btn-neon" onClick={() => setIsCalmRunning(true)}>
                    Start 2-Min Calm Session
                  </button>
                ) : (
                  <button className="btn btn-outline-neon" onClick={() => setIsCalmRunning(false)}>
                    Pause Session
                  </button>
                )}
                <button
                  className="btn btn-outline-neon"
                  onClick={() => {
                    setCalmSecondsLeft(120);
                    setIsCalmRunning(false);
                    setPlayCalmSound(false);
                    stopCalmAudio();
                  }}
                >
                  Reset Timer
                </button>
              </div>
              <label className="calm-sound-toggle">
                <input
                  type="checkbox"
                  checked={playCalmSound}
                  onChange={(e) => setPlayCalmSound(e.target.checked)}
                />
                Play calming_audio.mp3 during session
              </label>
              <audio ref={audioRef} src="/calming_audio.mp3" loop preload="auto" />
            </div>
          )}

          {selectedActivity === "gratitude" && (
            <div className="calm-mode-surface">
              <p>Write one thing that helped you today.</p>
              <textarea
                className="form-control"
                rows="3"
                placeholder="Type your gratitude note..."
                value={gratitudeText}
                onChange={(e) => setGratitudeText(e.target.value)}
              />
              <div className="intervention-actions" style={{ marginTop: "0.7rem" }}>
                <button
                  className="btn btn-neon"
                  disabled={gratitudeText.trim().length < 20}
                  onClick={() => completeActivity("Gratitude Game", 16, 7, 1)}
                >
                  Complete Gratitude Reflection
                </button>
              </div>
              <small>Minimum 20 characters to complete.</small>
            </div>
          )}

          {selectedActivity === "posture" && (
            <div className="calm-mode-surface">
              <p>Check off each reset step slowly.</p>
              <label className="calm-sound-toggle">
                <input
                  type="checkbox"
                  checked={postureChecks.shoulders}
                  onChange={(e) =>
                    setPostureChecks((prev) => ({ ...prev, shoulders: e.target.checked }))
                  }
                />
                Drop your shoulders
              </label>
              <label className="calm-sound-toggle">
                <input
                  type="checkbox"
                  checked={postureChecks.jaw}
                  onChange={(e) => setPostureChecks((prev) => ({ ...prev, jaw: e.target.checked }))}
                />
                Unclench your jaw
              </label>
              <label className="calm-sound-toggle">
                <input
                  type="checkbox"
                  checked={postureChecks.breathing}
                  onChange={(e) =>
                    setPostureChecks((prev) => ({ ...prev, breathing: e.target.checked }))
                  }
                />
                Take one slow breath
              </label>
              <div className="intervention-actions" style={{ marginTop: "0.7rem" }}>
                <button
                  className="btn btn-neon"
                  disabled={!(postureChecks.shoulders && postureChecks.jaw && postureChecks.breathing)}
                  onClick={() => completeActivity("Posture Reset", 14, 6, 1)}
                >
                  Complete Posture Reset
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
