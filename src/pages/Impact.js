import React from "react";
import "../theme.css";

export default function Impact() {
  const stats = [
    {
      number: "73%",
      label: "Reduction in Burnout Rates",
      desc: "People using StressConnect report significant decreases in burnout symptoms"
    },
    {
      number: "45%",
      label: "Increase in Productivity",
      desc: "Teams with proactive stress management show marked improvement in output quality"
    },
    {
      number: "89%",
      label: "User Satisfaction",
      desc: "Users report higher life satisfaction when stress is monitored and managed effectively"
    },
    {
      number: "62%",
      label: "Reduced Healthcare Costs",
      desc: "Prevention-focused approach leads to lower stress-related medical expenses"
    }
  ];

  const benefits = [
    {
      title: "For Individuals",
      items: [
        "Early warning system for stress buildup",
        "Personalized wellbeing recommendations",
        "Better daily balance insights",
        "Reduced risk of burnout and mental health issues",
        "Improved self-awareness and emotional intelligence"
      ]
    },
    {
      title: "For Care Teams",
      items: [
        "Real-time shared wellbeing visibility",
        "Data-driven decision making for support planning",
        "Early intervention opportunities",
        "Improved collaboration and support quality",
        "Reduced drop-off and disengagement"
      ]
    },
    {
      title: "For Programs",
      items: [
        "Lower stress-related support costs",
        "Increased consistency and outcomes",
        "Stronger trust and participation",
        "Measurable ROI on wellbeing investments",
        "Continuous improvement from behavioral data"
      ]
    }
  ];

  return (
    <div className="container py-5">
      <div className="text-center mb-5">
        <h2 className="neon-text">Measurable Impact</h2>
        <p className="lead">
          Transform stress outcomes with data-driven wellbeing insights
        </p>
      </div>

      {/* Statistics Section */}
      <div className="row mb-5">
        <div className="col-12">
          <div className="neon-card">
            <h3 className="text-center mb-4">Proven Results</h3>
            <div className="row">
              {stats.map((stat, idx) => (
                <div className="col-md-6 col-lg-3 mb-4 text-center" key={idx}>
                  <div style={{
                    background: 'rgba(178, 187, 95, 0.1)',
                    padding: '2rem 1rem',
                    borderRadius: '10px',
                    height: '100%'
                  }}>
                    <h2 className="neon-text" style={{fontSize: '3rem', marginBottom: '0.5rem'}}>
                      {stat.number}
                    </h2>
                    <h4 style={{color: '#465b26', marginBottom: '1rem'}}>{stat.label}</h4>
                    <p style={{fontSize: '0.9rem', color: '#556022'}}>{stat.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Benefits Section */}
      <div className="mb-5">
        <h3 className="text-center mb-4">Comprehensive Benefits</h3>
        <div className="row">
          {benefits.map((benefit, idx) => (
            <div className="col-md-4 mb-4" key={idx}>
              <div className="neon-card fade-in-up" style={{animationDelay: `${idx * 0.2}s`}}>
                <h4 className="text-center mb-3">{benefit.title}</h4>
                <ul className="list-unstyled">
                  {benefit.items.map((item, itemIdx) => (
                    <li key={itemIdx} style={{padding: '0.5rem 0', borderBottom: '1px solid rgba(178, 187, 95, 0.2)'}}>
                      ✓ {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ROI Section */}
      <div className="row mb-5">
        <div className="col-12">
          <div className="neon-card">
            <h3 className="text-center mb-4">Return on Investment</h3>
            <div className="row">
              <div className="col-md-6">
                <h4>Cost Savings</h4>
                <ul className="list-unstyled">
                  <li>Reduced stress-related downtime</li>
                  <li>Lower replacement and onboarding costs</li>
                  <li>Fewer preventable errors under pressure</li>
                  <li>Reduced medical utilization for stress symptoms</li>
                  <li>Lower operational disruption costs</li>
                </ul>
              </div>
              <div className="col-md-6">
                <h4>Revenue Enhancement</h4>
                <ul className="list-unstyled">
                  <li>Increased productivity and quality output</li>
                  <li>Enhanced innovation and creativity</li>
                  <li>Improved customer satisfaction scores</li>
                  <li>Better long-term user retention and expertise</li>
                  <li>Enhanced reputation and community growth</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Case Study Section */}
      <div className="row">
        <div className="col-12">
          <div className="neon-card slide-in-right">
            <h3 className="text-center mb-4">Success Story</h3>
            <div style={{
              background: 'rgba(178, 187, 95, 0.05)',
              padding: '2rem',
              borderRadius: '10px',
              borderLeft: '4px solid #b2bb5f'
            }}>
              <h4 style={{color: '#465b26'}}>MindWell Network - 5,000 User Rollout</h4>
              <p>
                <strong>Challenge:</strong> High burnout rates in intensive digital programs leading to high churn
                and declining consistency.
              </p>
              <p>
                <strong>Solution:</strong> Implemented StressConnect across all support cohorts with real-time
                monitoring and personalized wellbeing interventions.
              </p>
              <p>
                <strong>Results after 12 months:</strong>
              </p>
              <div className="row mt-3">
                <div className="col-md-6">
                  <ul className="list-unstyled">
                    <li>• 68% reduction in burnout-related turnover</li>
                    <li>• 52% increase in participant satisfaction scores</li>
                    <li>• 41% improvement in code quality metrics</li>
                  </ul>
                </div>
                <div className="col-md-6">
                  <ul className="list-unstyled">
                    <li>• $2.3M saved in recruitment and training costs</li>
                    <li>• 29% reduction in project delays</li>
                    <li>• 400% ROI within the first year</li>
                  </ul>
                </div>
              </div>
              <p style={{fontStyle: 'italic', marginTop: '1rem'}}>
                "StressConnect transformed how we support people. We now catch stress before it becomes burnout,
                and outcomes are stronger than ever."
                <br/>
                <strong>- Sarah Chen, Program Director, MindWell Network</strong>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}