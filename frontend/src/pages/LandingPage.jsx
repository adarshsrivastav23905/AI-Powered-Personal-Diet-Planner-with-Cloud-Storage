/**
 * Landing Page
 * ==============
 * Hero section with animated gradient, feature cards, and CTA.
 */

import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FiCloud, FiShield, FiZap, FiSmartphone, FiDatabase, FiCpu } from 'react-icons/fi';

export default function LandingPage() {
  const { user } = useAuth();

  return (
    <div className="landing-page">
      <section className="hero">
        <div className="hero-content">
          <div className="hero-badge">🤖 AI Nutrition Coach • ☁️ Cloud-Synced</div>
          <h1>Your Personal<br /><span className="gradient-text">Smart Diet Planner</span></h1>
          <p className="hero-subtitle">
            Build healthier habits with personalized meal suggestions, smart nutrition targets,
            and a clean cloud-based dashboard designed around your goals and lifestyle.
          </p>
          <div className="hero-actions">
            {user ? (
              <Link to="/dashboard" className="btn btn-primary btn-lg">
                Open Dashboard →
              </Link>
            ) : (
              <>
                <Link to="/register" className="btn btn-primary btn-lg">
                  Start Your Plan →
                </Link>
                <Link to="/login" className="btn btn-outline btn-lg">
                  Sign In
                </Link>
              </>
            )}
          </div>
          <p className="hero-disclaimer">
            Educational and wellness-focused; not a substitute for professional medical nutrition advice.
          </p>
        </div>

        <div className="hero-visual">
          <div className="hero-card floating">
            <div className="meal-preview">
              <div className="meal-icon">🥗</div>
              <div>
                <strong>Lunch</strong>
                <p>Protein Bowl</p>
                <span className="cal-badge">420 kcal</span>
              </div>
            </div>
            <div className="meal-preview">
              <div className="meal-icon">🍳</div>
              <div>
                <strong>Breakfast</strong>
                <p>Oatmeal & Berries</p>
                <span className="cal-badge">350 kcal</span>
              </div>
            </div>
            <div className="meal-preview">
              <div className="meal-icon">🍲</div>
              <div>
                <strong>Dinner</strong>
                <p>Salmon Rice Bowl</p>
                <span className="cal-badge">510 kcal</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="stats-strip" aria-label="Project highlights">
        <div className="stat-box">
          <strong>AI-driven</strong>
          <span>Personal meal suggestions</span>
        </div>
        <div className="stat-box">
          <strong>Cloud-ready</strong>
          <span>Database + storage workflow</span>
        </div>
        <div className="stat-box">
          <strong>Secure access</strong>
          <span>JWT auth and user isolation</span>
        </div>
      </section>

      <section className="features" id="features">
        <h2>Why <span className="gradient-text">NutriCloud AI</span>?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon"><FiCpu size={32} /></div>
            <h3>AI-Driven Planning</h3>
            <p>Personalized meal plans generated from your profile, health goals, and dietary preferences.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"><FiCloud size={32} /></div>
            <h3>Cloud Storage</h3>
            <p>Your plans, files, and nutrition data stay available across devices and sessions.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"><FiShield size={32} /></div>
            <h3>Secure & Private</h3>
            <p>Authentication, isolation, and encrypted cloud storage protect user-specific data.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"><FiZap size={32} /></div>
            <h3>Goal-Based Targets</h3>
            <p>Smart calorie and macro planning aligned to your chosen fitness and wellness objective.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"><FiSmartphone size={32} /></div>
            <h3>Clean Interface</h3>
            <p>A polished dashboard experience that feels modern, simple, and easy to use on any device.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"><FiDatabase size={32} /></div>
            <h3>Reliable Backend</h3>
            <p>Structured REST APIs and profile-driven logic make the experience predictable and scalable.</p>
          </div>
        </div>
      </section>

      <section className="how-it-works">
        <h2>How It <span className="gradient-text">Works</span></h2>
        <div className="steps-grid">
          <div className="step-card">
            <div className="step-number">1</div>
            <h3>Create Profile</h3>
            <p>Enter key details like age, height, weight, activity level, and dietary preferences.</p>
          </div>
          <div className="step-card">
            <div className="step-number">2</div>
            <h3>Set Your Goal</h3>
            <p>Choose your target such as weight loss, maintenance, muscle gain, or overall wellness.</p>
          </div>
          <div className="step-card">
            <div className="step-number">3</div>
            <h3>Generate Plan</h3>
            <p>Receive a personalized meal plan with calories and macros tailored to your needs.</p>
          </div>
          <div className="step-card">
            <div className="step-number">4</div>
            <h3>Track & Improve</h3>
            <p>Update your profile, save plans, and adapt your routine as your goals evolve.</p>
          </div>
        </div>
      </section>

      <section className="submission-banner">
        <div>
          <p className="banner-kicker">Built for real-world learning</p>
          <h3>Designed to showcase cloud computing, AI planning, and full-stack development.</h3>
        </div>
        <Link to="/register" className="btn btn-primary btn-lg">Create Your Diet Plan</Link>
      </section>

      <footer className="footer">
        <p>© 2026 NutriCloud AI — Personal Diet Planner</p>
        <p className="footer-disclaimer">
          Educational demo project. Generated meal plans are wellness examples and not medical advice.
        </p>
      </footer>
    </div>
  );
}
