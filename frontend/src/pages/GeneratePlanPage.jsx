/**
 * Generate Plan Page
 * ====================
 * AI-powered diet plan generation with real-time nutrition targets.
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { profileAPI, plansAPI } from '../services/api';
import { FiZap, FiTarget, FiDroplet } from 'react-icons/fi';

export default function GeneratePlanPage() {
  const navigate = useNavigate();
  const [targets, setTargets] = useState(null);
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [overrides, setOverrides] = useState({
    diet_type: '',
    goal: '',
    plan_name: 'My Diet Plan',
  });

  useEffect(() => {
    loadTargets();
  }, []);

  const loadTargets = async () => {
    try {
      const res = await profileAPI.getTargets();
      setTargets(res.data.targets);
    } catch (err) {
      setError(err.response?.data?.error || 'Please complete your profile first');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    setError('');
    setPlan(null);

    try {
      const payload = {};
      if (overrides.diet_type) payload.diet_type = overrides.diet_type;
      if (overrides.goal) payload.goal = overrides.goal;
      if (overrides.plan_name) payload.plan_name = overrides.plan_name;

      const res = await plansAPI.generate(payload);
      setPlan(res.data.plan);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate plan. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  const renderMeal = (mealName, items, icon) => (
    <div className="meal-card">
      <div className="meal-card-header">
        <span className="meal-emoji">{icon}</span>
        <h3>{mealName}</h3>
      </div>
      <div className="meal-items">
        {items.map((item, idx) => (
          <div key={idx} className="meal-item">
            <div className="meal-item-name">{item.name}</div>
            <div className="meal-item-details">
              <span>{item.serving}</span>
              <span className="cal-badge">{item.kcal} kcal</span>
            </div>
            <div className="macro-pills">
              <span className="pill pill-protein">P: {item.protein}g</span>
              <span className="pill pill-carbs">C: {item.carbs}g</span>
              <span className="pill pill-fat">F: {item.fat}g</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  if (loading) return <div className="loading-screen"><div className="spinner"></div></div>;

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>🤖 Generate Diet Plan</h1>
        <p>AI will create a personalized meal plan based on your profile and goals</p>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {/* Nutrition Targets */}
      {targets && (
        <div className="targets-card">
          <h3><FiTarget /> Your Nutrition Targets</h3>
          <div className="targets-grid">
            <div className="target-item">
              <span className="target-label">BMR</span>
              <span className="target-value">{targets.bmr}</span>
              <span className="target-unit">kcal/day</span>
            </div>
            <div className="target-item">
              <span className="target-label">TDEE</span>
              <span className="target-value">{targets.tdee}</span>
              <span className="target-unit">kcal/day</span>
            </div>
            <div className="target-item highlight">
              <span className="target-label">Daily Target</span>
              <span className="target-value">{targets.daily_calories}</span>
              <span className="target-unit">kcal/day ({targets.goal_adjustment})</span>
            </div>
            <div className="target-item">
              <span className="target-label">Protein</span>
              <span className="target-value">{targets.macros.protein_g}g</span>
            </div>
            <div className="target-item">
              <span className="target-label">Carbs</span>
              <span className="target-value">{targets.macros.carbs_g}g</span>
            </div>
            <div className="target-item">
              <span className="target-label">Fat</span>
              <span className="target-value">{targets.macros.fat_g}g</span>
            </div>
            <div className="target-item">
              <span className="target-label"><FiDroplet /> Water</span>
              <span className="target-value">{targets.water_liters}L</span>
              <span className="target-unit">daily</span>
            </div>
          </div>
        </div>
      )}

      {/* Plan Options */}
      {!plan && targets && (
        <div className="generate-options">
          <div className="form-grid">
            <div className="form-group">
              <label>Plan Name</label>
              <input value={overrides.plan_name}
                     onChange={(e) => setOverrides(p => ({ ...p, plan_name: e.target.value }))}
                     placeholder="My Diet Plan" />
            </div>
            <div className="form-group">
              <label>Override Diet Type (optional)</label>
              <select value={overrides.diet_type}
                      onChange={(e) => setOverrides(p => ({ ...p, diet_type: e.target.value }))}>
                <option value="">Use profile default</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="non_vegetarian">Non-Vegetarian</option>
                <option value="eggetarian">Eggetarian</option>
              </select>
            </div>
            <div className="form-group">
              <label>Override Goal (optional)</label>
              <select value={overrides.goal}
                      onChange={(e) => setOverrides(p => ({ ...p, goal: e.target.value }))}>
                <option value="">Use profile default</option>
                <option value="lose_weight">Lose Weight</option>
                <option value="gain_weight">Gain Weight</option>
                <option value="maintain">Maintain</option>
                <option value="muscle_gain">Muscle Gain</option>
                <option value="general_fitness">General Fitness</option>
              </select>
            </div>
          </div>

          <button onClick={handleGenerate} className="btn btn-primary btn-lg btn-full"
                  disabled={generating}>
            {generating ? (
              <><span className="spinner-sm"></span> Generating your plan...</>
            ) : (
              <><FiZap /> Generate My Diet Plan</>
            )}
          </button>
        </div>
      )}

      {/* Generated Plan */}
      {plan && (
        <div className="plan-result fade-in">
          <div className="plan-disclaimer">
            ⚕️ This plan is for educational/general wellness demonstration only. It is NOT medical or clinical nutrition advice.
          </div>

          <h2>🍽️ {plan.plan_name}</h2>

          <div className="meals-grid">
            {renderMeal('Breakfast', plan.breakfast, '🌅')}
            {renderMeal('Lunch', plan.lunch, '☀️')}
            {renderMeal('Snack', plan.snack, '🍎')}
            {renderMeal('Dinner', plan.dinner, '🌙')}
          </div>

          {/* Summary */}
          <div className="plan-summary">
            <h3>📊 Nutrition Summary</h3>
            <div className="summary-grid">
              <div className="summary-item">
                <span className="summary-label">Total Calories</span>
                <span className="summary-value">{plan.total_calories} kcal</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Protein</span>
                <span className="summary-value">{plan.macros.protein_g}g</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Carbs</span>
                <span className="summary-value">{plan.macros.carbs_g}g</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Fat</span>
                <span className="summary-value">{plan.macros.fat_g}g</span>
              </div>
            </div>
            <p className="hydration-reminder">{plan.hydration_reminder}</p>
          </div>

          <div className="plan-actions">
            <button onClick={() => { setPlan(null); }} className="btn btn-outline">
              Generate Another Plan
            </button>
            <button onClick={() => navigate('/plans')} className="btn btn-primary">
              View All Plans →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
