/**
 * Profile Page
 * ==============
 * User profile form for collecting demographic and dietary information.
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { profileAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { FiSave, FiCheck } from 'react-icons/fi';

export default function ProfilePage() {
  const { updateUser } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const [form, setForm] = useState({
    name: '',
    age: '',
    height_cm: '',
    weight_kg: '',
    sex: 'not_specified',
    activity_level: 'moderate',
    dietary_preference: 'vegetarian',
    goal: 'maintain',
    allergies: [],
    cuisines: [],
    budget_per_day: '',
    timeline_weeks: 4,
  });

  const allergyOptions = ['nuts', 'dairy', 'gluten', 'eggs', 'soy', 'fish', 'shellfish'];
  const cuisineOptions = ['indian', 'continental', 'asian', 'mediterranean', 'any'];

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const res = await profileAPI.get();
      const p = res.data.profile;
      setForm({
        name: p.name || '',
        age: p.age || '',
        height_cm: p.height_cm || '',
        weight_kg: p.weight_kg || '',
        sex: p.sex || 'not_specified',
        activity_level: p.activity_level || 'moderate',
        dietary_preference: p.dietary_preference || 'vegetarian',
        goal: p.goal || 'maintain',
        allergies: p.allergies || [],
        cuisines: p.cuisines || [],
        budget_per_day: p.budget_per_day || '',
        timeline_weeks: p.timeline_weeks || 4,
      });
    } catch (err) {
      console.error('Failed to load profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const toggleArrayItem = (field, item) => {
    setForm(prev => ({
      ...prev,
      [field]: prev[field].includes(item)
        ? prev[field].filter(i => i !== item)
        : [...prev[field], item],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setSaving(true);

    try {
      const payload = {
        ...form,
        age: parseInt(form.age) || null,
        height_cm: parseFloat(form.height_cm) || null,
        weight_kg: parseFloat(form.weight_kg) || null,
        budget_per_day: parseFloat(form.budget_per_day) || 0,
        timeline_weeks: parseInt(form.timeline_weeks) || 4,
      };

      const res = await profileAPI.update(payload);
      setSuccess('Profile saved successfully!');
      updateUser({ profile_completed: res.data.profile_completed });

      if (res.data.profile_completed) {
        setTimeout(() => navigate('/generate'), 1500);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save profile');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="loading-screen"><div className="spinner"></div></div>;

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>👤 Your Profile</h1>
        <p>Tell us about yourself so we can create your perfect diet plan</p>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success"><FiCheck /> {success}</div>}

      <form onSubmit={handleSubmit} className="profile-form">
        {/* Basic Info */}
        <div className="form-section">
          <h3>📋 Basic Information</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="name">Full Name</label>
              <input id="name" name="name" value={form.name} onChange={handleChange}
                     placeholder="Your name" required />
            </div>
            <div className="form-group">
              <label htmlFor="age">Age</label>
              <input id="age" name="age" type="number" value={form.age} onChange={handleChange}
                     placeholder="e.g. 25" min="10" max="120" required />
            </div>
            <div className="form-group">
              <label htmlFor="sex">Sex</label>
              <select id="sex" name="sex" value={form.sex} onChange={handleChange}>
                <option value="not_specified">Prefer not to say</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>
          </div>
        </div>

        {/* Body Measurements */}
        <div className="form-section">
          <h3>📏 Body Measurements</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="height">Height (cm)</label>
              <input id="height" name="height_cm" type="number" value={form.height_cm}
                     onChange={handleChange} placeholder="e.g. 170" min="50" max="300" step="0.1" required />
            </div>
            <div className="form-group">
              <label htmlFor="weight">Weight (kg)</label>
              <input id="weight" name="weight_kg" type="number" value={form.weight_kg}
                     onChange={handleChange} placeholder="e.g. 68" min="20" max="500" step="0.1" required />
            </div>
          </div>
        </div>

        {/* Lifestyle */}
        <div className="form-section">
          <h3>🏃 Lifestyle & Goals</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="activity">Activity Level</label>
              <select id="activity" name="activity_level" value={form.activity_level} onChange={handleChange}>
                <option value="sedentary">Sedentary (little/no exercise)</option>
                <option value="light">Light (1-3 days/week)</option>
                <option value="moderate">Moderate (3-5 days/week)</option>
                <option value="active">Active (6-7 days/week)</option>
                <option value="very_active">Very Active (intense daily)</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="goal">Goal</label>
              <select id="goal" name="goal" value={form.goal} onChange={handleChange}>
                <option value="maintain">Maintain Weight</option>
                <option value="lose_weight">Lose Weight</option>
                <option value="gain_weight">Gain Weight</option>
                <option value="muscle_gain">Muscle Gain</option>
                <option value="general_fitness">General Fitness</option>
              </select>
            </div>
          </div>
        </div>

        {/* Dietary Preferences */}
        <div className="form-section">
          <h3>🥗 Dietary Preferences</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="dietary_preference">Diet Type</label>
              <select id="dietary_preference" name="dietary_preference" value={form.dietary_preference}
                      onChange={handleChange}>
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="non_vegetarian">Non-Vegetarian</option>
                <option value="eggetarian">Eggetarian</option>
              </select>
            </div>
            <div className="form-group">
              <label>Allergies (optional)</label>
              <div className="chip-group">
                {allergyOptions.map(a => (
                  <button key={a} type="button"
                          className={`chip ${form.allergies.includes(a) ? 'chip-active' : ''}`}
                          onClick={() => toggleArrayItem('allergies', a)}>
                    {a}
                  </button>
                ))}
              </div>
            </div>
            <div className="form-group">
              <label>Cuisine Preferences (optional)</label>
              <div className="chip-group">
                {cuisineOptions.map(c => (
                  <button key={c} type="button"
                          className={`chip ${form.cuisines.includes(c) ? 'chip-active' : ''}`}
                          onClick={() => toggleArrayItem('cuisines', c)}>
                    {c}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        <button type="submit" id="saveProfile" className="btn btn-primary btn-lg btn-full" disabled={saving}>
          {saving ? <span className="spinner-sm"></span> : <><FiSave /> Save Profile</>}
        </button>
      </form>
    </div>
  );
}
