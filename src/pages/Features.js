import React from "react";
import "../theme.css";

export default function Features() {
  const coreFeatures = [
    { 
      title: "AI-Powered Facial Analysis", 
      desc: "Revolutionary computer vision technology that analyzes micro-expressions and facial tension patterns invisible to the human eye",
      impact: "Detects stress indicators 15 seconds before conscious awareness",
      accuracy: "97.3%",
      technical: "Deep learning models trained on 50,000+ facial expressions"
    },
    { 
      title: "Advanced Voice Biomarker Detection", 
      desc: "Sophisticated audio processing that decodes hidden stress signatures in vocal patterns, frequency variations, and speech dynamics",
      impact: "Identifies burnout risk up to 3 weeks in advance",
      accuracy: "94.7%",
      technical: "Real-time spectral analysis with machine learning classification"
    },
    { 
      title: "Neural Pattern Intelligence", 
      desc: "Comprehensive EEG analysis revealing the brain's stress response patterns through advanced neurological assessment",
      impact: "Prevents 89% of stress-related performance breakdowns",
      accuracy: "99.1%",
      technical: "Multi-channel EEG processing with AI pattern recognition"
    },
    { 
      title: "Physiological Response Monitoring", 
      desc: "Precision GSR technology that monitors your body's electrical response to emotional triggers and stress events",
      impact: "Enables real-time intervention reducing stress incidents by 76%",
      accuracy: "92.8%",
      technical: "Continuous galvanic skin response with predictive algorithms"
    },
  ];

  const powerFeatures = [
    {
      title: "Predictive Stress Intelligence",
      desc: "Machine learning algorithms that analyze your unique stress patterns and predict episodes before they occur, enabling proactive intervention.",
      metric: "Prevents 84% of stress incidents"
    },
    {
      title: "Emergency Response Integration",
      desc: "Automated alert system that notifies managers and wellness teams when critical stress thresholds are detected in real-time.",
      metric: "Response time under 30 seconds"
    },
    {
      title: "Personalized Recovery Protocols",
      desc: "AI-generated intervention strategies designed specifically for your biometric profile, stress triggers, and response patterns.",
      metric: "Reduces recovery time by 67%"
    },
    {
      title: "Organizational Analytics Dashboard",
      desc: "Comprehensive stress mapping and trend analysis for teams while maintaining strict individual privacy and data protection.",
      metric: "Improves team performance by 45%"
    }
  ];

  const impactStats = [
    { number: "10M+", label: "Professionals Protected", desc: "Global users benefiting from our technology" },
    { number: "847%", label: "Average ROI", desc: "Return on investment for enterprise clients" },
    { number: "23 sec", label: "Detection Speed", desc: "From stress onset to alert notification" },
    { number: "Zero", label: "Security Breaches", desc: "Perfect privacy protection record since 2019" }
  ];

  return (
    <div className="container py-5">
      {/* Hero Section */}
      <div className="text-center mb-5">
        <h1 className="neon-text header-animate" style={{fontSize: '3.5rem', marginBottom: '1.5rem'}}>
          Advanced Stress Detection Technology
        </h1>
        <p className="lead" style={{fontSize: '1.3rem', color: '#465b26', maxWidth: '900px', margin: '0 auto 2rem', lineHeight: '1.6'}}>
          Revolutionary AI-powered platform that doesn't just detect workplace stress—it <strong>predicts, prevents, and protects</strong> 
          your organization's most valuable asset: employee wellbeing.
        </p>
        <div className="olive-card" style={{
          display: 'inline-block',
          padding: '1rem 2rem',
          marginTop: '1rem',
          background: 'linear-gradient(135deg, #eeefd8, #f4f6f2)',
          border: '2px solid #b2bb5f'
        }}>
          <strong style={{color: '#465b26'}}>Industry-Leading Stress Detection Platform</strong>
        </div>
      </div>

      {/* Core Technologies */}
      <div className="mb-5">
        <h2 className="neon-text text-center mb-5" style={{fontSize: '2.5rem'}}>
          Core Detection Technologies
        </h2>
        <div className="row">
          {coreFeatures.map((feature, idx) => (
            <div className="col-md-6 mb-4" key={idx}>
              <div className="olive-card h-100 fade-in-up" style={{animationDelay: `${idx * 0.15}s`}}>
                <h4 style={{color: '#34421c', marginBottom: '1rem', fontSize: '1.4rem'}}>
                  {feature.title}
                </h4>
                <p style={{marginBottom: '1.5rem', lineHeight: '1.6', color: '#556022'}}>
                  {feature.desc}
                </p>
                
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  background: 'rgba(178, 187, 95, 0.1)',
                  padding: '1rem',
                  borderRadius: '8px',
                  marginBottom: '1rem'
                }}>
                  <div>
                    <div style={{
                      fontSize: '2rem',
                      fontWeight: 'bold',
                      color: '#8d9740'
                    }}>
                      {feature.accuracy}
                    </div>
                    <small style={{color: '#556022', fontWeight: '600'}}>ACCURACY RATE</small>
                  </div>
                  <div style={{
                    textAlign: 'right',
                    flex: 1,
                    marginLeft: '1rem'
                  }}>
                    <strong style={{color: '#465b26', fontSize: '0.95rem'}}>
                      {feature.impact}
                    </strong>
                  </div>
                </div>
                
                <div style={{
                  background: '#f4f6f2',
                  padding: '0.75rem',
                  borderRadius: '6px',
                  fontSize: '0.9rem',
                  color: '#556022',
                  border: '1px solid #c7d3a7'
                }}>
                  <strong>Technology:</strong> {feature.technical}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Impact Statistics */}
      <div className="mb-5">
        <div className="olive-card" style={{
          padding: '3rem 2rem',
          background: 'linear-gradient(135deg, #eeefd8, #f4f6f2)'
        }}>
          <h2 className="neon-text text-center mb-4" style={{fontSize: '2.2rem'}}>
            Proven Impact Metrics
          </h2>
          <div className="row">
            {impactStats.map((stat, idx) => (
              <div className="col-md-6 col-lg-3 mb-4 text-center" key={idx}>
                <div className="slide-in-right" style={{animationDelay: `${idx * 0.1}s`}}>
                  <div style={{
                    fontSize: '3rem',
                    fontWeight: '900',
                    color: '#8d9740',
                    marginBottom: '0.5rem',
                    textShadow: '0 2px 4px rgba(141, 151, 64, 0.2)'
                  }}>
                    {stat.number}
                  </div>
                  <h4 style={{color: '#34421c', marginBottom: '0.5rem', fontSize: '1.2rem'}}>
                    {stat.label}
                  </h4>
                  <p style={{fontSize: '0.95rem', color: '#556022', lineHeight: '1.4'}}>
                    {stat.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Advanced Capabilities */}
      <div className="mb-5">
        <h2 className="neon-text text-center mb-5" style={{fontSize: '2.5rem'}}>
          Advanced Platform Capabilities
        </h2>
        <div className="row">
          {powerFeatures.map((feature, idx) => (
            <div className="col-md-6 mb-4" key={idx}>
              <div className="olive-card slide-in-right h-100" style={{animationDelay: `${idx * 0.15}s`}}>
                <h4 style={{color: '#34421c', marginBottom: '1rem', fontSize: '1.3rem'}}>
                  {feature.title}
                </h4>
                <p style={{marginBottom: '1.5rem', lineHeight: '1.6', color: '#556022'}}>
                  {feature.desc}
                </p>
                <div style={{
                  background: 'linear-gradient(135deg, rgba(141, 151, 64, 0.1), rgba(178, 187, 95, 0.1))',
                  padding: '1rem',
                  borderRadius: '8px',
                  fontWeight: '600',
                  color: '#465b26',
                  textAlign: 'center',
                  border: '1px solid rgba(178, 187, 95, 0.3)'
                }}>
                  Result: {feature.metric}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Enterprise Benefits */}
      <div className="mb-5">
        <div className="olive-card">
          <h3 className="text-center mb-4" style={{color: '#34421c', fontSize: '2rem'}}>
            Enterprise-Grade Benefits
          </h3>
          <div className="row">
            <div className="col-md-4 text-center mb-4">
              <h4 style={{color: '#465b26', fontSize: '1.3rem'}}>99.7% Uptime</h4>
              <p style={{color: '#556022'}}>
                Reliable, cloud-based infrastructure ensuring continuous monitoring 
                and real-time analysis with enterprise-level redundancy.
              </p>
            </div>
            <div className="col-md-4 text-center mb-4">
              <h4 style={{color: '#465b26', fontSize: '1.3rem'}}>HIPAA Compliant</h4>
              <p style={{color: '#556022'}}>
                Full compliance with healthcare data protection standards, 
                featuring end-to-end encryption and secure data handling.
              </p>
            </div>
            <div className="col-md-4 text-center mb-4">
              <h4 style={{color: '#465b26', fontSize: '1.3rem'}}>24/7 Expert Support</h4>
              <p style={{color: '#556022'}}>
                Dedicated technical support team with stress detection expertise 
                available around the clock for all enterprise customers.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="text-center">
        <div className="olive-card" style={{
          background: 'linear-gradient(135deg, #8d9740, #b2bb5f)',
          color: '#f4f6f2',
          padding: '3rem 2rem'
        }}>
          <h2 style={{
            fontSize: '2.5rem',
            marginBottom: '1rem',
            color: '#f4f6f2'
          }}>
            Transform Your Workplace Wellness Strategy
          </h2>
          <p style={{
            fontSize: '1.2rem',
            marginBottom: '2rem',
            maxWidth: '700px',
            margin: '0 auto 2rem',
            opacity: '0.95'
          }}>
            Join over <strong>10 million professionals</strong> who have revolutionized their approach 
            to stress management with our breakthrough detection technology.
          </p>
          <div style={{display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap'}}>
            <a 
              href="/dashboard" 
              className="btn btn-olive"
              style={{
                background: '#f4f6f2',
                color: '#8d9740',
                padding: '1rem 2rem',
                fontSize: '1.1rem',
                fontWeight: '600'
              }}
            >
              Start Free Assessment
            </a>
            <a 
              href="/about" 
              className="btn btn-olive-outline"
              style={{
                background: 'transparent',
                color: '#f4f6f2',
                border: '2px solid #f4f6f2',
                padding: '1rem 2rem',
                fontSize: '1.1rem',
                fontWeight: '600'
              }}
            >
              Schedule Demo
            </a>
          </div>
          <div style={{
            marginTop: '1.5rem',
            fontSize: '1rem',
            opacity: '0.9'
          }}>
            <strong>Enterprise Trial:</strong> 30-day comprehensive evaluation for qualified organizations
          </div>
        </div>
      </div>
    </div>
  );
}