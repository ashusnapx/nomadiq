'use client';

import React, { useState, useEffect } from 'react';
import { 
  Compass, MapPin, Calendar, DollarSign, Shield, Zap, RefreshCw, BarChart2, CheckCircle, 
  AlertTriangle, Play, HelpCircle, Thermometer, User, Activity, FileText, Settings, Sparkles
} from 'lucide-react';

interface ActivityItem {
  id: number;
  day_number: number;
  time_slot: string;
  name: string;
  description: string;
  location: string;
  cost: number;
  category: string;
  explanation?: string;
  citations?: string[];
  risk_score: number;
}

interface DayPlan {
  day_number: number;
  activities: ActivityItem[];
  daily_budget: number;
  weather_summary?: string;
}

interface Itinerary {
  id: number;
  variant: string;
  confidence_score: number;
  total_cost: number;
  days: DayPlan[];
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<'profile' | 'builder' | 'itinerary' | 'live' | 'trace' | 'evaluation' | 'simulation'>('builder');
  const [destination, setDestination] = useState('New York City');
  const [startDate, setStartDate] = useState('2026-06-15');
  const [endDate, setEndDate] = useState('2026-06-20');
  const [budgetMin, setBudgetMin] = useState(500);
  const [budgetMax, setBudgetMax] = useState(2500);
  const [persona, setPersona] = useState('Balanced Traveler');
  const [preferences, setPreferences] = useState('Sightseeing, local food spots, walkability, avoid extremely crowded tourist traps.');
  
  const [isLoading, setIsLoading] = useState(false);
  const [itineraries, setItineraries] = useState<Itinerary[]>([]);
  const [selectedVariant, setSelectedVariant] = useState<string>('Plan A (Balanced)');
  const [activeItinerary, setActiveItinerary] = useState<Itinerary | null>(null);

  // Live simulation event
  const [simType, setSimType] = useState('weather_disruption');
  const [simValue, setSimValue] = useState('Rain starting at 3 PM');
  const [simResults, setSimResults] = useState<any[]>([]);
  const [isSimulating, setIsSimulating] = useState(false);

  // Alerts feed
  const [alerts, setAlerts] = useState<any[]>([
    { id: 1, type: 'warning', text: 'Rain forecast for Day 2 afternoon in Central Park. Outdoor events may be impacted.', resolved: false },
    { id: 2, type: 'info', text: 'Transport route optimized: Subway preferred over taxi for rush hour.', resolved: true }
  ]);

  // Cost Governance & Traces
  const [tokenSummary, setTokenSummary] = useState({
    total_cost_usd: 0.042,
    total_prompt_tokens: 1850,
    total_completion_tokens: 820,
    cost_by_model: { 'gpt-4o-mini': 0.005, 'gpt-4o': 0.037 },
    over_budget: false
  });

  const [traces, setTraces] = useState<any[]>([
    { agent: 'UserPreferenceAgent', model: 'gpt-4o-mini', latency: 450, status: 'Success' },
    { agent: 'DestinationResearchAgent', model: 'gpt-4o', latency: 1890, status: 'Success' },
    { agent: 'WeatherIntelligenceAgent', model: 'gpt-4o-mini', latency: 310, status: 'Success' },
    { agent: 'TransportationAgent', model: 'gpt-4o-mini', latency: 620, status: 'Success' },
    { agent: 'OptimizationAgent', model: 'gpt-4o', latency: 2100, status: 'Success' },
    { agent: 'SafetyAgent', model: 'gpt-4o-mini', latency: 280, status: 'Success' }
  ]);

  const [evalReport, setEvalReport] = useState<any>({
    scores: {
      relevance: 0.95,
      personalization: 0.92,
      budget_adherence: 1.0,
      time_feasibility: 0.88,
      diversity: 0.85,
      hallucination_rate: 0.0
    },
    overall_score: 0.92,
    strengths: ['Highly customized to culinary preferences', 'Maintains cost well within bounds', 'Excellent routing consistency'],
    weaknesses: ['Dense day 2 plan leaves little buffer time'],
    recommendations: ['Consider shifting Met Museum to morning slot']
  });

  // Mock initial load
  useEffect(() => {
    generateMockItinerary();
  }, []);

  const generateMockItinerary = () => {
    const mockPlanA: Itinerary = {
      id: 101,
      variant: 'Plan A (Balanced)',
      confidence_score: 0.95,
      total_cost: 1350,
      days: [
        {
          day_number: 1,
          daily_budget: 180,
          weather_summary: 'Sunny, 22°C',
          activities: [
            {
              id: 1,
              day_number: 1,
              time_slot: 'Morning',
              name: 'Bethesda Fountain & Terrace',
              description: 'Peaceful walk around the historic lake and fountain.',
              location: 'Central Park, NY',
              cost: 0,
              category: 'Sightseeing',
              explanation: 'Selected for central location and scenic walking path.',
              citations: ['NYC Insider Guidebook'],
              risk_score: 0.98
            },
            {
              id: 2,
              day_number: 1,
              time_slot: 'Lunch',
              name: 'Greenwich Village Food Tour',
              description: 'Tasting local pizza, bagels, and pastries in historic neighborhood.',
              location: 'Greenwich Village, NY',
              cost: 65,
              category: 'Food',
              explanation: 'Matches culinary interest.',
              citations: ['Eats Magazine'],
              risk_score: 0.95
            },
            {
              id: 3,
              day_number: 1,
              time_slot: 'Afternoon',
              name: 'High Line Promenade Walk',
              description: 'Stroll along the historic elevated rail track park.',
              location: 'Chelsea, NY',
              cost: 0,
              category: 'Sightseeing',
              explanation: 'Highly rated outdoor walking experience.',
              citations: ['NYC Parks Directory'],
              risk_score: 0.99
            }
          ]
        },
        {
          day_number: 2,
          daily_budget: 250,
          weather_summary: 'Partial Clouds, 24°C',
          activities: [
            {
              id: 4,
              day_number: 2,
              time_slot: 'Morning',
              name: 'Metropolitan Museum of Art',
              description: 'Exploring world class art collection.',
              location: 'Fifth Avenue, NY',
              cost: 30,
              category: 'Culture',
              explanation: 'Matches cultural interests.',
              citations: ['Museum Digest'],
              risk_score: 0.95
            }
          ]
        }
      ]
    };

    const mockPlanB: Itinerary = {
      id: 102,
      variant: 'Plan B (Budget-Focused)',
      confidence_score: 0.88,
      total_cost: 680,
      days: [
        {
          day_number: 1,
          daily_budget: 90,
          weather_summary: 'Sunny, 22°C',
          activities: [
            {
              id: 11,
              day_number: 1,
              time_slot: 'Morning',
              name: 'Central Park Walking Tour',
              description: 'Free self-guided scenic walking tour.',
              location: 'Central Park, NY',
              cost: 0,
              category: 'Sightseeing',
              explanation: 'Excellent value sightseeing activity.',
              citations: ['NYC Parks Directory'],
              risk_score: 0.98
            }
          ]
        }
      ]
    };

    const mockPlanC: Itinerary = {
      id: 103,
      variant: 'Plan C (Experience-Focused)',
      confidence_score: 0.98,
      total_cost: 2450,
      days: [
        {
          day_number: 1,
          daily_budget: 850,
          weather_summary: 'Sunny, 22°C',
          activities: [
            {
              id: 21,
              day_number: 1,
              time_slot: 'Morning',
              name: 'Private Helicopter Tour over Manhattan',
              description: 'Premium flight showcasing NYC skyline.',
              location: 'Downtown Heliport, NY',
              cost: 350,
              category: 'Adventure',
              explanation: 'Ultimate experience for sightseeing.',
              citations: ['Luxury Traveller Monthly'],
              risk_score: 0.92
            }
          ]
        }
      ]
    };

    setItineraries([mockPlanA, mockPlanB, mockPlanC]);
    setActiveItinerary(mockPlanA);
  };

  const handleGenerate = async () => {
    setIsLoading(true);
    // Simulate API fetch delay
    setTimeout(() => {
      generateMockItinerary();
      setIsLoading(false);
      setActiveTab('itinerary');
      // Add trace step
      setTraces(prev => [
        ...prev,
        { agent: 'ReplanningAgent', model: 'gpt-4o', latency: 1950, status: 'Success' }
      ]);
    }, 2000);
  };

  const handleSimulation = () => {
    setIsSimulating(true);
    setTimeout(() => {
      setSimResults([
        { variant: 'Plan A (Balanced)', original_cost: 1350, simulated_cost: 1380, original_score: 0.95, simulated_score: 0.91, affected: 'High Line Walk (Rain)', replacement: 'Museum of Modern Art (Indoor)' },
        { variant: 'Plan B (Budget-Focused)', original_cost: 680, simulated_cost: 680, original_score: 0.88, simulated_score: 0.82, affected: 'Central Park Walking (Rain)', replacement: 'Chelsea Market Food Hall' }
      ]);
      setAlerts(prev => [
        { id: Date.now(), type: 'critical', text: `Disruption simulated: ${simValue}. Replanning successfully completed.`, resolved: false },
        ...prev
      ]);
      setIsSimulating(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen flex flex-col font-sans">
      {/* Top Header */}
      <header className="border-b border-gray-800 bg-[#0f111a] px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-400 to-blue-600 flex items-center justify-center text-black font-extrabold text-xl shadow-lg shadow-cyan-500/20">
            N
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
              NomadIQ <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-normal">Platform v1.0</span>
            </h1>
            <p className="text-xs text-gray-400">Travel Decision Intelligence Platform</p>
          </div>
        </div>

        {/* Global Stats Overview */}
        <div className="flex items-center gap-6 text-sm">
          <div className="bg-[#161925] border border-gray-800 px-3 py-1.5 rounded-lg flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            <span className="text-gray-400">Database:</span>
            <span className="text-emerald-400 font-semibold">pgvector (Connected)</span>
          </div>
          <div className="bg-[#161925] border border-gray-800 px-3 py-1.5 rounded-lg flex items-center gap-2">
            <DollarSign className="w-4 h-4 text-cyan-400" />
            <span className="text-gray-400">AI Cost:</span>
            <span className="text-cyan-400 font-semibold">${tokenSummary.total_cost_usd.toFixed(3)}</span>
          </div>
        </div>
      </header>

      {/* Main Content Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Navigation Sidebar */}
        <nav className="w-64 border-r border-gray-800 bg-[#0c0e16] p-4 flex flex-col gap-2 shrink-0">
          <button 
            onClick={() => setActiveTab('profile')} 
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left text-sm font-medium transition ${activeTab === 'profile' ? 'bg-cyan-500/10 text-cyan-400 border-l-4 border-cyan-500' : 'text-gray-400 hover:bg-gray-800/40'}`}
          >
            <User className="w-4 h-4" /> Traveler Profile
          </button>
          <button 
            onClick={() => setActiveTab('builder')} 
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left text-sm font-medium transition ${activeTab === 'builder' ? 'bg-cyan-500/10 text-cyan-400 border-l-4 border-cyan-500' : 'text-gray-400 hover:bg-gray-800/40'}`}
          >
            <Compass className="w-4 h-4" /> Trip Builder
          </button>
          <button 
            onClick={() => setActiveTab('itinerary')} 
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left text-sm font-medium transition ${activeTab === 'itinerary' ? 'bg-cyan-500/10 text-cyan-400 border-l-4 border-cyan-500' : 'text-gray-400 hover:bg-gray-800/40'}`}
          >
            <Calendar className="w-4 h-4" /> Itinerary Dashboard
          </button>
          <button 
            onClick={() => setActiveTab('live')} 
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left text-sm font-medium transition ${activeTab === 'live' ? 'bg-cyan-500/10 text-cyan-400 border-l-4 border-cyan-500' : 'text-gray-400 hover:bg-gray-800/40'}`}
          >
            <RefreshCw className="w-4 h-4" /> Live Updates Feed
          </button>
          <button 
            onClick={() => setActiveTab('trace')} 
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left text-sm font-medium transition ${activeTab === 'trace' ? 'bg-cyan-500/10 text-cyan-400 border-l-4 border-cyan-500' : 'text-gray-400 hover:bg-gray-800/40'}`}
          >
            <Activity className="w-4 h-4" /> Agent Trace Log
          </button>
          <button 
            onClick={() => setActiveTab('evaluation')} 
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left text-sm font-medium transition ${activeTab === 'evaluation' ? 'bg-cyan-500/10 text-cyan-400 border-l-4 border-cyan-500' : 'text-gray-400 hover:bg-gray-800/40'}`}
          >
            <BarChart2 className="w-4 h-4" /> Evaluation Metrics
          </button>
          <button 
            onClick={() => setActiveTab('simulation')} 
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left text-sm font-medium transition ${activeTab === 'simulation' ? 'bg-cyan-500/10 text-cyan-400 border-l-4 border-cyan-500' : 'text-gray-400 hover:bg-gray-800/40'}`}
          >
            <Zap className="w-4 h-4" /> What-If Simulator
          </button>
        </nav>

        {/* Workspace Panels */}
        <main className="flex-1 p-8 overflow-y-auto bg-[#090b11]">
          {/* TAB: BUILDER */}
          {activeTab === 'builder' && (
            <div className="max-w-4xl mx-auto space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-white">Create New Trip</h2>
                  <p className="text-sm text-gray-400">Configure parameters for the multi-agent planning workflow.</p>
                </div>
                <button 
                  onClick={handleGenerate}
                  disabled={isLoading}
                  className="px-6 py-3 rounded-xl font-semibold bg-gradient-to-r from-cyan-400 to-blue-600 hover:from-cyan-500 hover:to-blue-700 text-black shadow-lg shadow-cyan-500/20 disabled:opacity-50 flex items-center gap-2 transition"
                >
                  {isLoading ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" /> Compiling Plans...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" /> Launch AI Copilot
                    </>
                  )}
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Destination and Dates */}
                <div className="glass-panel p-6 rounded-2xl space-y-4">
                  <h3 className="text-lg font-semibold text-white flex items-center gap-2 border-b border-gray-800 pb-2">
                    <MapPin className="w-4 h-4 text-cyan-400" /> Geography & Timing
                  </h3>
                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-gray-400 uppercase">Target Destination</label>
                    <input 
                      type="text" 
                      value={destination} 
                      onChange={(e) => setDestination(e.target.value)}
                      className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-500" 
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="text-xs font-semibold text-gray-400 uppercase">Start Date</label>
                      <input 
                        type="date" 
                        value={startDate} 
                        onChange={(e) => setStartDate(e.target.value)}
                        className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-500" 
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-xs font-semibold text-gray-400 uppercase">End Date</label>
                      <input 
                        type="date" 
                        value={endDate} 
                        onChange={(e) => setEndDate(e.target.value)}
                        className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-500" 
                      />
                    </div>
                  </div>
                </div>

                {/* Budget & Persona */}
                <div className="glass-panel p-6 rounded-2xl space-y-4">
                  <h3 className="text-lg font-semibold text-white flex items-center gap-2 border-b border-gray-800 pb-2">
                    <DollarSign className="w-4 h-4 text-cyan-400" /> Budget & Archetype
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="text-xs font-semibold text-gray-400 uppercase">Min Budget ($)</label>
                      <input 
                        type="number" 
                        value={budgetMin} 
                        onChange={(e) => setBudgetMin(Number(e.target.value))}
                        className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-500" 
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-xs font-semibold text-gray-400 uppercase">Max Budget ($)</label>
                      <input 
                        type="number" 
                        value={budgetMax} 
                        onChange={(e) => setBudgetMax(Number(e.target.value))}
                        className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-500" 
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-gray-400 uppercase">Traveler Persona</label>
                    <select 
                      value={persona} 
                      onChange={(e) => setPersona(e.target.value)}
                      className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-500"
                    >
                      <option>Balanced Traveler</option>
                      <option>Adventure Seeker</option>
                      <option>Luxury Traveler</option>
                      <option>Food Explorer</option>
                      <option>Nature Enthusiast</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Natural Language Preferences */}
              <div className="glass-panel p-6 rounded-2xl space-y-3">
                <h3 className="text-lg font-semibold text-white flex items-center gap-2 border-b border-gray-800 pb-2">
                  <FileText className="w-4 h-4 text-cyan-400" /> Stated Interests & Constraints
                </h3>
                <textarea 
                  value={preferences}
                  onChange={(e) => setPreferences(e.target.value)}
                  rows={4}
                  placeholder="Describe your trip goals, food preferences, places to avoid, pacing..."
                  className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-cyan-500 text-sm"
                ></textarea>
              </div>
            </div>
          )}

          {/* TAB: ITINERARY DASHBOARD */}
          {activeTab === 'itinerary' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between border-b border-gray-800 pb-4">
                <div>
                  <h2 className="text-2xl font-bold text-white">Travel Itinerary Planner</h2>
                  <p className="text-sm text-gray-400">Compare optimized variants built by our multi-agent model router.</p>
                </div>
                {/* Variant Selector */}
                <div className="flex bg-[#121420] p-1 rounded-xl border border-gray-800">
                  {itineraries.map((it) => (
                    <button
                      key={it.variant}
                      onClick={() => {
                        setSelectedVariant(it.variant);
                        setActiveItinerary(it);
                      }}
                      className={`px-4 py-2 rounded-lg text-xs font-semibold transition ${selectedVariant === it.variant ? 'bg-cyan-500 text-black shadow-md' : 'text-gray-400 hover:text-white'}`}
                    >
                      {it.variant}
                    </button>
                  ))}
                </div>
              </div>

              {activeItinerary && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Timeline view */}
                  <div className="lg:col-span-2 space-y-6">
                    {activeItinerary.days.map((day) => (
                      <div key={day.day_number} className="glass-panel p-6 rounded-2xl space-y-4">
                        <div className="flex items-center justify-between border-b border-gray-800 pb-2">
                          <h3 className="text-lg font-bold text-white">Day {day.day_number}</h3>
                          <div className="flex items-center gap-4 text-xs">
                            <span className="text-gray-400 flex items-center gap-1">
                              <Thermometer className="w-3.5 h-3.5 text-orange-400" /> {day.weather_summary}
                            </span>
                            <span className="text-cyan-400 font-semibold">Budget: ${day.daily_budget}</span>
                          </div>
                        </div>

                        {/* Activities timeline */}
                        <div className="space-y-4">
                          {day.activities.map((act) => (
                            <div key={act.id} className="relative pl-6 border-l-2 border-cyan-500/30 hover:border-cyan-400 transition py-2">
                              <div className="absolute -left-[5px] top-4 w-2 h-2 rounded-full bg-cyan-400 shadow-md shadow-cyan-400/50"></div>
                              <div className="flex items-start justify-between">
                                <div>
                                  <span className="text-xs font-semibold text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded-full border border-cyan-900">{act.time_slot}</span>
                                  <h4 className="text-base font-bold text-white mt-1.5">{act.name}</h4>
                                  <p className="text-sm text-gray-400 mt-1">{act.description}</p>
                                  <span className="text-xs text-gray-500 mt-2 block">📍 {act.location}</span>
                                </div>
                                <span className="text-sm font-semibold text-white">${act.cost}</span>
                              </div>
                              {/* Explainability Block */}
                              {act.explanation && (
                                <div className="mt-3 bg-[#11141e] border border-gray-800/60 p-3 rounded-lg text-xs">
                                  <span className="font-semibold text-gray-300 block mb-1">Why Recommended:</span>
                                  <p className="text-gray-400 italic">"{act.explanation}"</p>
                                  {act.citations && act.citations.length > 0 && (
                                    <span className="text-[10px] text-cyan-500/80 block mt-1.5">📚 Sources: {act.citations.join(', ')}</span>
                                  )}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Sidebar - Cost Summary */}
                  <div className="space-y-6">
                    <div className="glass-panel p-6 rounded-2xl space-y-4">
                      <h3 className="text-lg font-bold text-white border-b border-gray-800 pb-2">Itinerary Analytics</h3>
                      <div className="space-y-3">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-400">Total Cost:</span>
                          <span className="text-white font-bold">${activeItinerary.total_cost}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-400">Confidence Score:</span>
                          <span className="text-emerald-400 font-semibold">{(activeItinerary.confidence_score * 100).toFixed(0)}%</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-400">Safety Rating:</span>
                          <span className="text-emerald-400 font-semibold">100% Safe</span>
                        </div>
                      </div>
                      <div className="pt-2">
                        <button className="w-full py-2.5 rounded-xl font-semibold bg-cyan-400 text-black hover:bg-cyan-500 transition text-sm">
                          Approve Itinerary Plan
                        </button>
                      </div>
                    </div>

                    {/* Alert Feed Widget */}
                    <div className="glass-panel p-6 rounded-2xl space-y-4">
                      <h3 className="text-lg font-bold text-white border-b border-gray-800 pb-2">Active Disruption Feed</h3>
                      <div className="space-y-3">
                        {alerts.map((al) => (
                          <div key={al.id} className={`p-3 rounded-lg border text-xs flex gap-2.5 ${al.type === 'critical' ? 'bg-red-950/20 border-red-900/40 text-red-300' : al.type === 'warning' ? 'bg-amber-950/20 border-amber-900/40 text-amber-300' : 'bg-blue-950/20 border-blue-900/40 text-blue-300'}`}>
                            {al.type === 'critical' ? <AlertTriangle className="w-4 h-4 shrink-0" /> : <HelpCircle className="w-4 h-4 shrink-0" />}
                            <div>
                              <p className="font-medium">{al.text}</p>
                              {al.resolved && <span className="text-[10px] text-emerald-400 block mt-1">✓ Resolved</span>}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB: LIVE UPDATES FEED */}
          {activeTab === 'live' && (
            <div className="max-w-4xl mx-auto space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white">Live Disruption Alerts</h2>
                <p className="text-sm text-gray-400">Monitor active transportation, weather, and schedule warnings.</p>
              </div>

              <div className="space-y-4">
                {alerts.map((al) => (
                  <div key={al.id} className={`p-4 rounded-xl border flex items-start gap-4 ${al.type === 'critical' ? 'bg-red-950/10 border-red-900/30' : 'bg-amber-950/10 border-amber-900/30'}`}>
                    <AlertTriangle className={`w-5 h-5 mt-0.5 ${al.type === 'critical' ? 'text-red-400' : 'text-amber-400'}`} />
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className={`text-xs font-bold uppercase tracking-wider ${al.type === 'critical' ? 'text-red-400' : 'text-amber-400'}`}>{al.type}</span>
                        <span className="text-xs text-gray-500">Just Now</span>
                      </div>
                      <p className="text-sm text-white mt-1.5">{al.text}</p>
                      <div className="mt-3 flex gap-2">
                        <button className="px-3 py-1 rounded bg-[#1e2330] border border-gray-800 hover:bg-gray-800 text-xs font-semibold text-white transition">
                          View Affected Activity
                        </button>
                        <button className="px-3 py-1 rounded bg-cyan-500 hover:bg-cyan-600 text-xs font-semibold text-black transition">
                          Run Selective Replan
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB: AGENT TRACE LOG */}
          {activeTab === 'trace' && (
            <div className="max-w-4xl mx-auto space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white">Multi-Agent Traces</h2>
                <p className="text-sm text-gray-400">Inspect real-time latency, token usage and cost tracking metrics for every step.</p>
              </div>

              {/* Aggregated Cost Dashboard */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="glass-panel p-5 rounded-xl space-y-2">
                  <span className="text-xs text-gray-400 uppercase font-semibold">Total Query Cost</span>
                  <p className="text-2xl font-black text-cyan-400 glow-text-cyan">${tokenSummary.total_cost_usd.toFixed(4)}</p>
                </div>
                <div className="glass-panel p-5 rounded-xl space-y-2">
                  <span className="text-xs text-gray-400 uppercase font-semibold">Total Prompt Tokens</span>
                  <p className="text-2xl font-black text-white">{tokenSummary.total_prompt_tokens}</p>
                </div>
                <div className="glass-panel p-5 rounded-xl space-y-2">
                  <span className="text-xs text-gray-400 uppercase font-semibold">Completion Tokens</span>
                  <p className="text-2xl font-black text-white">{tokenSummary.total_completion_tokens}</p>
                </div>
              </div>

              {/* Traces Table */}
              <div className="glass-panel rounded-xl overflow-hidden border border-gray-800">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-[#121420] border-b border-gray-800 text-xs font-semibold text-gray-400 uppercase">
                      <th className="px-6 py-4">Agent Name</th>
                      <th className="px-6 py-4">Model Routed</th>
                      <th className="px-6 py-4">Latency (ms)</th>
                      <th className="px-6 py-4">Status</th>
                    </tr>
                  </thead>
                  <tbody className="text-sm divide-y divide-gray-800">
                    {traces.map((tr, idx) => (
                      <tr key={idx} className="hover:bg-gray-800/10">
                        <td className="px-6 py-4 font-semibold text-white">{tr.agent}</td>
                        <td className="px-6 py-4 text-gray-400">{tr.model}</td>
                        <td className="px-6 py-4 text-cyan-400 font-medium">{tr.latency}ms</td>
                        <td className="px-6 py-4">
                          <span className="px-2 py-0.5 rounded-full text-xs bg-emerald-950 text-emerald-400 border border-emerald-900/40">
                            {tr.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB: EVALUATION METRICS */}
          {activeTab === 'evaluation' && (
            <div className="max-w-4xl mx-auto space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white">AI Evaluation Framework</h2>
                <p className="text-sm text-gray-400">Inspect automated benchmark metrics generated by the judge LLM.</p>
              </div>

              {/* Metrics scores grid */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
                {Object.entries(evalReport.scores).map(([name, val]: any) => (
                  <div key={name} className="glass-panel p-5 rounded-xl space-y-2">
                    <span className="text-xs text-gray-400 uppercase font-semibold">{name.replace('_', ' ')}</span>
                    <p className="text-2xl font-black text-cyan-400">{(val * 100).toFixed(0)}%</p>
                  </div>
                ))}
              </div>

              {/* Strengths & Weaknesses */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="glass-panel p-6 rounded-xl space-y-3">
                  <h3 className="text-base font-bold text-emerald-400 flex items-center gap-2 border-b border-gray-800 pb-2">
                    <CheckCircle className="w-4 h-4" /> Judge Key Strengths
                  </h3>
                  <ul className="space-y-2 text-sm text-gray-300 list-disc list-inside">
                    {evalReport.strengths.map((str: string, i: number) => (
                      <li key={i}>{str}</li>
                    ))}
                  </ul>
                </div>
                <div className="glass-panel p-6 rounded-xl space-y-3">
                  <h3 className="text-base font-bold text-red-400 flex items-center gap-2 border-b border-gray-800 pb-2">
                    <AlertTriangle className="w-4 h-4" /> Areas for Improvement
                  </h3>
                  <ul className="space-y-2 text-sm text-gray-300 list-disc list-inside">
                    {evalReport.weaknesses.map((wk: string, i: number) => (
                      <li key={i}>{wk}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* TAB: SIMULATION ENGINE */}
          {activeTab === 'simulation' && (
            <div className="max-w-4xl mx-auto space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white">What-If Simulation Engine</h2>
                <p className="text-sm text-gray-400">Simulate unexpected disruptions, budget drops, or closures to preview timeline impacts.</p>
              </div>

              {/* Simulation triggers */}
              <div className="glass-panel p-6 rounded-2xl space-y-4">
                <h3 className="text-lg font-semibold text-white border-b border-gray-800 pb-2">Define Hypothetical Scenario</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-gray-400 uppercase">Scenario Type</label>
                    <select 
                      value={simType} 
                      onChange={(e) => setSimType(e.target.value)}
                      className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-500 text-sm"
                    >
                      <option value="weather_disruption">Weather Disruption (e.g., Rain/Storm)</option>
                      <option value="budget_cut">Budget Reduction</option>
                      <option value="closure">Attraction Closure</option>
                    </select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-gray-400 uppercase">Parameter Value</label>
                    <input 
                      type="text" 
                      value={simValue} 
                      onChange={(e) => setSimValue(e.target.value)}
                      placeholder="e.g. 30% drop, Storm at 1 PM"
                      className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-500 text-sm" 
                    />
                  </div>
                </div>
                <div className="pt-2 flex justify-end">
                  <button 
                    onClick={handleSimulation}
                    disabled={isSimulating}
                    className="px-6 py-2.5 rounded-xl font-semibold bg-cyan-400 text-black hover:bg-cyan-500 transition text-sm flex items-center gap-2"
                  >
                    {isSimulating ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" /> Simulating...
                      </>
                    ) : (
                      <>
                        <Play className="w-4 h-4" /> Inject Scenario
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* Simulation comparison results */}
              {simResults.length > 0 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-bold text-white">Scenario Impact Report</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {simResults.map((res, i) => (
                      <div key={i} className="glass-panel p-6 rounded-xl space-y-4 border border-cyan-500/20">
                        <span className="text-xs font-bold text-cyan-400 uppercase">{res.variant}</span>
                        <div className="grid grid-cols-2 gap-4 text-sm border-t border-b border-gray-800 py-3 my-2">
                          <div>
                            <span className="text-gray-500 text-xs block">Original Cost</span>
                            <span className="text-white font-semibold">${res.original_cost}</span>
                          </div>
                          <div>
                            <span className="text-gray-500 text-xs block">Simulated Cost</span>
                            <span className="text-cyan-400 font-semibold">${res.simulated_cost}</span>
                          </div>
                          <div className="mt-2">
                            <span className="text-gray-500 text-xs block">Original Score</span>
                            <span className="text-emerald-400 font-semibold">{(res.original_score * 100).toFixed(0)}%</span>
                          </div>
                          <div className="mt-2">
                            <span className="text-gray-500 text-xs block">Simulated Score</span>
                            <span className="text-yellow-400 font-semibold">{(res.simulated_score * 100).toFixed(0)}%</span>
                          </div>
                        </div>
                        <div className="space-y-2 text-xs">
                          <div>
                            <span className="text-gray-400 font-semibold block">Affected Activity:</span>
                            <p className="text-red-400">{res.affected}</p>
                          </div>
                          <div className="pt-1">
                            <span className="text-gray-400 font-semibold block">Surgically Substituted:</span>
                            <p className="text-emerald-400">{res.replacement}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB: PROFILE */}
          {activeTab === 'profile' && (
            <div className="max-w-2xl mx-auto space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white">Traveler Preferences Profile</h2>
                <p className="text-sm text-gray-400">Manage global persona details and persistent preferences.</p>
              </div>

              <div className="glass-panel p-6 rounded-2xl space-y-4">
                <div className="space-y-2">
                  <label className="text-xs font-semibold text-gray-400 uppercase">Age Bracket</label>
                  <input type="text" defaultValue="25-35 Years" className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-2.5 text-white" />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-semibold text-gray-400 uppercase">Dietary Exclusions</label>
                  <input type="text" defaultValue="Gluten Free" className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-2.5 text-white" />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-semibold text-gray-400 uppercase">Mobility Level</label>
                  <input type="text" defaultValue="Active Walker" className="w-full bg-[#121420] border border-gray-800 rounded-xl px-4 py-2.5 text-white" />
                </div>
                <div className="pt-2">
                  <button className="px-6 py-2.5 rounded-xl font-semibold bg-cyan-400 text-black hover:bg-cyan-500 transition text-sm">
                    Save Profile Settings
                  </button>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
