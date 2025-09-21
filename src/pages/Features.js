import React from "react";
import "../theme.css";

export default function Features() {
  const coreFeatures = [
    { 
      title: "AI-Powered Facial Recognition", 
      desc: "Revolutionary computer vision that reads micro-expressions invisible to the human eye",
      impact: "Detects stress 15 seconds before conscious awareness",
      accuracy: "97.3%",
      icon: "🧠",
      gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    },
    { 
      title: "Voice Biomarker Analysis", 
      desc: "Decode hidden stress signatures in vocal patterns and speech dynamics",
      impact: "Identifies burnout risk 3 weeks in advance",
      accuracy: "94.7%",
      icon: "🎵",
      gradient: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
    },
    { 
      title: "Neural Pattern Intelligence", 
      desc: "Deep EEG analysis revealing the brain's stress response at the cellular level",
      impact: "Prevents 89% of stress-related breakdowns",
      accuracy: "99.1%",
      icon: "⚡",
      gradient: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
    },
    { 
      title: "Biometric Stress Mapping", 
      desc: "GSR technology that monitors your body's electrical response to emotional triggers",
      impact: "Real-time intervention reduces incidents by 76%",
      accuracy: "92.8%",
      icon: "💫",
      gradient: "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
    },
  ];

  const powerFeatures = [
    {
      title: "Predictive Stress Intelligence",
      desc: "AI that learns your unique stress patterns and predicts episodes before they happen",
      icon: "🔮",
      stats: "Prevents 84% of stress incidents"
    },
    {
      title: "Emergency Response System",
      desc: "Instant alerts to managers and wellness teams when critical stress levels are detected",
      icon: "🚨",
      stats: "Response time under 30 seconds"
    },
    {
      title: "Personalized Recovery Plans",
      desc: "Custom interventions designed by AI based on your biometric profile and stress triggers",
      icon: "🎯",
      stats: "Recovery time reduced by 67%"
    },
    {
      title: "Team Stress Heatmaps",
      desc: "Visual dashboards showing organizational stress patterns and high-risk areas",
      icon: "🗺️",
      stats: "Improves team performance by 45%"
    }
  ];

  const impactStats = [
    { number: "10M+", label: "Lives Protected", desc: "Professionals worldwide using our technology" },
    { number: "847%", label: "ROI Average", desc: "Return on investment for enterprise clients" },
    { number: "23 Sec", label: "Detection Speed", desc: "From stress onset to alert notification" },
    { number: "Zero", label: "Privacy Breaches", desc: "Perfect security record since 2019" }
  ];

  return (
    <div className="container py-5">
      {/* Hero Section */}
      <div className="text-center mb-5">
        <h1 className="neon-text header-animate" style={{fontSize: '4rem', marginBottom: '1rem'}}>
          The Future of Stress Detection
        </h1>
        <p className="lead" style={{fontSize: '1.5rem', color: '#465b26', maxWidth: '800px', margin: '0 auto 2rem'}}>
          Revolutionary AI technology that doesn't just detect stress—it <strong>predicts, prevents, and protects</strong> 
          your mental wellbeing before crisis strikes.
        </p>
        <div style={{
          background: 'linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #f9ca24)',
          padding: '3px',
          borderRadius: '50px',
          display: 'inline-block',
          margin: '1rem 0'
        }}>
          <div style={{
            background: '#f4f6f2',
            padding: '1rem 2rem',
            borderRadius: '47px',
            fontWeight: 'bold',
            color: '#29351d'
          }}>
            🚀 <strong>World's Most Advanced Stress Detection Platform</strong>
          </div>
        </div>
      </div>

      {/* Core Technologies */}
      <div className="mb-5">
        <h2 className="neon-text text-center mb-5" style={{fontSize: '2.8rem'}}>
          🧬 Revolutionary Detection Technologies
        </h2>
        <div className="row">
          {coreFeatures.map((feature, idx) => (
            <div className="col-md-6 col-lg-3 mb-4" key={idx}>
              <div 
                className="olive-card text-center h-100 fade-in-up"
                style={{
                  animationDelay: `${idx * 0.2}s`,
                  position: 'relative',
                  overflow: 'hidden',
                  border: '3px solid transparent',
                  background: feature.gradient,
                  backgroundClip: 'padding-box'
                }}
              >
                <div style={{
                  background: '#f4f6f2',
                  margin: '3px',
                  padding: '2rem 1.5rem',
                  borderRadius: '15px',
                  height: 'calc(100% - 6px)'
                }}>
                  <div style={{
                    fontSize: '4rem',
                    marginBottom: '1rem',
                    filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.1))'
                  }}>
                    {feature.icon}
                  </div>
                  <h4 style={{color: '#34421c', marginBottom: '1rem', fontSize: '1.3rem'}}>
                    {feature.title}
                  </h4>
                  <p style={{marginBottom: '1.5rem', lineHeight: '1.6'}}>
                    {feature.desc}
                  </p>
                  
                  <div style={{
                    background: 'rgba(178, 187, 95, 0.1)',
                    padding: '1rem',
                    borderRadius: '10px',
                    marginBottom: '1rem',
                    border: '2px solid rgba(178, 187, 95, 0.3)'
                  }}>
                    <div style={{
                      fontSize: '2rem',
                      fontWeight: 'bold',
                      color: '#8d9740',
                      marginBottom: '0.5rem'
                    }}>
                      {feature.accuracy}
                    </div>
                    <small style={{color: '#556022', fontWeight: 'bold'}}>ACCURACY RATE</small>
                  </div>
                  
                  <div style={{
                    background: 'linear-gradient(45deg, rgba(178, 187, 95, 0.1), rgba(178, 187, 95, 0.05))',
                    padding: '0.75rem',
                    borderRadius: '8px',
                    fontSize: '0.9rem',
                    fontWeight: 'bold',
                    color: '#465b26'
                  }}>
                    ⚡ {feature.impact}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Impact Statistics */}
      <div className="mb-5" style={{
        background: 'linear-gradient(135deg, rgba(178, 187, 95, 0.1), rgba(178, 187, 95, 0.05))',
        padding: '3rem 2rem',
        borderRadius: '20px',
        border: '2px solid rgba(178, 187, 95, 0.2)'
      }}>
        <h2 className="neon-text text-center mb-4" style={{fontSize: '2.5rem'}}>
          🏆 Unprecedented Impact Metrics
        </h2>
        <div className="row">
          {impactStats.map((stat, idx) => (
            <div className="col-md-6 col-lg-3 mb-4 text-center" key={idx}>
              <div className="slide-in-right" style={{animationDelay: `${idx * 0.1}s`}}>
                <div style={{
                  fontSize: '3.5rem',
                  fontWeight: '900',
                  background: 'linear-gradient(45deg, #8d9740, #b2bb5f, #e4f56a)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  textShadow: '0 4px 8px rgba(0,0,0,0.1)',
                  marginBottom: '0.5rem'
                }}>
                  {stat.number}
                </div>
                <h4 style={{color: '#34421c', marginBottom: '0.5rem'}}>{stat.label}</h4>
                <p style={{fontSize: '0.9rem', color: '#556022'}}>{stat.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Power Features */}
      <div className="mb-5">
        <h2 className="neon-text text-center mb-5" style={{fontSize: '2.8rem'}}>
          ⚡ Game-Changing Capabilities
        </h2>
        <div className="row">
          {powerFeatures.map((feature, idx) => (
            <div className="col-md-6 mb-4" key={idx}>
              <div className="olive-card slide-in-right h-100" style={{
                animationDelay: `${idx * 0.15}s`,
                background: 'linear-gradient(135deg, #eeefd8, #f9faf2)',
                border: '2px solid #b2bb5f',
                position: 'relative',
                overflow: 'hidden'
              }}>
                <div style={{
                  position: 'absolute',
                  top: '-50%',
                  right: '-50%',
                  width: '200%',
                  height: '200%',
                  background: `conic-gradient(from 0deg, transparent, rgba(178, 187, 95, 0.1), transparent)`,
                  animation: 'spin 20s linear infinite',
                  zIndex: 0
                }}>
                </div>
                <div style={{position: 'relative', zIndex: 1}}>
                  <div style={{
                    fontSize: '3rem',
                    marginBottom: '1rem',
                    filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.1))'
                  }}>
                    {feature.icon}
                  </div>
                  <h4 style={{color: '#34421c', marginBottom: '1rem'}}>{feature.title}</h4>
                  <p style={{marginBottom: '1.5rem', lineHeight: '1.6'}}>{feature.desc}</p>
                  <div style={{
                    background: 'rgba(141, 151, 64, 0.1)',
                    padding: '1rem',
                    borderRadius: '10px',
                    fontWeight: 'bold',
                    color: '#8d9740',
                    textAlign: 'center',
                    border: '2px solid rgba(141, 151, 64, 0.2)'
                  }}>
                    📈 {feature.stats}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Call to Action */}
      <div className="text-center" style={{
        background: 'linear-gradient(135deg, #8d9740, #b2bb5f)',
        padding: '3rem',
        borderRadius: '20px',
        color: '#f4f6f2',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'url("data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23ffffff" fill-opacity="0.1"%3E%3Ccircle cx="30" cy="30" r="4"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat',
          opacity: 0.3
        }}>
        </div>
        <div style={{position: 'relative', zIndex: 1}}>
          <h2 style={{
            fontSize: '3rem',
            marginBottom: '1rem',
            textShadow: '0 2px 4px rgba(0,0,0,0.3)'
          }}>
            🚀 Ready to Revolutionize Workplace Wellness?
          </h2>
          <p style={{
            fontSize: '1.3rem',
            marginBottom: '2rem',
            maxWidth: '600px',
            margin: '0 auto 2rem'
          }}>
            Join the <strong>10 million+ professionals</strong> who've transformed their stress management 
            with our breakthrough technology. Your mental health revolution starts now.
          </p>
          <div style={{display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap'}}>
            <a 
              href="/dashboard" 
              className="btn"
              style={{
                background: '#f4f6f2',
                color: '#8d9740',
                padding: '1rem 2rem',
                fontSize: '1.2rem',
                fontWeight: 'bold',
                borderRadius: '50px',
                textDecoration: 'none',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 15px rgba(0,0,0,0.2)'
              }}
            >
              🎯 Start Your Transformation
            </a>
            <a 
              href="/about" 
              className="btn"
              style={{
                background: 'transparent',
                color: '#f4f6f2',
                border: '2px solid #f4f6f2',
                padding: '1rem 2rem',
                fontSize: '1.2rem',
                fontWeight: 'bold',
                borderRadius: '50px',
                textDecoration: 'none',
                transition: 'all 0.3s ease'
              }}
            >
              📊 See the Science
            </a>
          </div>
          <div style={{
            marginTop: '2rem',
            fontSize: '1rem',
            opacity: 0.9
          }}>
            ✨ <strong>Special Launch Offer:</strong> First 1,000 users get lifetime 50% discount
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}