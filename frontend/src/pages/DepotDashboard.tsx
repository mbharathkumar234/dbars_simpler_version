import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Truck, Route, RefreshCw, ArrowLeft } from "lucide-react";
import BlockingPanel from "../components/BlockingPanel";
import ScenarioConsole from "../components/ScenarioConsole";
import { useAuth } from "../contexts/AuthContext";
import { useLanguage } from "../contexts/LanguageContext";
import { apiFetch } from "../lib/apiClient";

export default function DepotDashboard() {
  const { token } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [dispatchData, setDispatchData] = useState<any>(null);
  const [deploying, setDeploying] = useState<string | null>(null);

  const fetchRecommendations = () => {
    const headers = { Authorization: `Bearer ${token}` };
    apiFetch(`/depot/dispatch-recommendations`, { headers })
      .then(async (r) => (r.ok ? r.json() : null))
      .then((data) => { if (data) setDispatchData(data); })
      .catch(() => { });
  };

  useEffect(() => {
    const headers = { Authorization: `Bearer ${token}` };

    apiFetch(`/depot/dispatch-recommendations`, { headers })
      .then(async (r) => (r.ok ? r.json() : null))
      .then((data) => {
        if (data) setDispatchData(data);
      })
      .catch(() => { })
      .finally(() => setLoading(false));
  }, [token]);

  const handleDeployBus = async (routeNumber: string) => {
    setDeploying(routeNumber);
    try {
      await apiFetch(`/depot/deploy-bus`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ route_number: routeNumber })
      });
      fetchRecommendations();
    } catch (e) {
      console.error(e);
    } finally {
      setDeploying(null);
    }
  };

  if (loading) return <div className="page-container"><div className="page-loader">{t("common.loading")}</div></div>;

  return (
    <div className="page-container">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="depot-page">
        <div className="page-header bento-card" style={{ padding: '1.25rem 2rem', marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <button
            type="button"
            onClick={() => navigate(-1)}
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--surface-strong)', border: '1px solid var(--line-strong)', borderRadius: '50%', width: '38px', height: '38px', cursor: 'pointer', color: 'var(--text)', flexShrink: 0, transition: 'background 0.15s' }}
            onMouseEnter={e => (e.currentTarget.style.background = 'var(--surface-sunken)')}
            onMouseLeave={e => (e.currentTarget.style.background = 'var(--surface-strong)')}
            title="Go Back"
          >
            <ArrowLeft size={18} />
          </button>
          <Truck size={24} className="text-accent" style={{ flexShrink: 0 }} />
          <div style={{ flex: 1 }}>
            <h1 className="bento-title" style={{ margin: 0 }}>{t("depot.title")}</h1>
            <p className="text-muted" style={{ margin: 0, fontSize: '0.9rem' }}>Route timetable blocking, depot allocation, and dispatch recommendations</p>
          </div>
        </div>

        {/* Fleet blocking plan running on BMTC published timetable catalogue */}
        <BlockingPanel token={token} />

        {/* The timetable change scenario console */}
        <ScenarioConsole token={token} />

        {/* Dispatch Recommendations, built from real commuter votes */}
        {dispatchData && (
          <div className="bento-card" style={{ padding: '1.75rem', marginTop: '2rem', marginBottom: '2rem', background: 'var(--surface-glass)', backdropFilter: 'blur(16px)', border: '1px solid var(--line-strong)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '1rem' }}>
              <div>
                <h3 className="bento-title" style={{ fontSize: '1.25rem', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Route size={20} className="text-accent" /> Route Dispatch Recommendations
                </h3>
                <p className="text-muted" style={{ fontSize: '0.85rem', margin: '4px 0 0 0' }}>
                  Derived from commuter votes over the last {dispatchData.period_days ?? 14} days.
                </p>
              </div>
              <button onClick={fetchRecommendations} className="bento-btn secondary" style={{ padding: '6px 12px', fontSize: '0.8rem' }}>
                <RefreshCw size={14} /> Refresh
              </button>
            </div>

            {dispatchData.recommendations && dispatchData.recommendations.length > 0 ? (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
                {dispatchData.recommendations.map((rec: any) => {
                  const isDeployed = (dispatchData.deployed_buses || []).some((d: any) => d.route_number === rec.route_number);
                  return (
                    <div key={`${rec.route_number}-${rec.current_stop}-${rec.destination}`} style={{ padding: '1.25rem', borderRadius: '14px', background: 'var(--surface-strong)', border: '1px solid var(--line-strong)', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: '0.75rem' }}>
                      <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                          <span className="bus-badge" style={{ fontSize: '1.1rem', padding: '0.35rem 0.85rem' }}>Route {rec.route_number}</span>
                          <span style={{ padding: '2px 8px', borderRadius: '12px', fontSize: '0.72rem', fontWeight: 800, background: rec.surge_level === 'HIGH' ? '#f43f5e20' : rec.surge_level === 'MEDIUM' ? '#f59e0b20' : '#64748b20', color: rec.surge_level === 'HIGH' ? '#f43f5e' : rec.surge_level === 'MEDIUM' ? '#f59e0b' : '#64748b', border: `1px solid ${rec.surge_level === 'HIGH' ? '#f43f5e50' : rec.surge_level === 'MEDIUM' ? '#f59e0b50' : '#64748b50'}` }}>
                            {rec.surge_level} DEMAND
                          </span>
                        </div>
                        <h4 style={{ margin: '0 0 0.35rem 0', fontSize: '0.95rem' }}>{rec.current_stop} → {rec.destination}</h4>
                        <p className="text-muted" style={{ fontSize: '0.82rem', lineHeight: '1.4', margin: 0 }}>{rec.reason}</p>
                      </div>

                      <div style={{ paddingTop: '0.75rem', borderTop: '1px solid var(--line-strong)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ fontSize: '0.78rem', color: 'var(--text-3)' }}>
                          {rec.genuine_vote_count} vote{rec.genuine_vote_count === 1 ? '' : 's'} · {rec.unique_voters} voter{rec.unique_voters === 1 ? '' : 's'}
                        </div>
                        <button
                          className="bento-btn"
                          style={{ padding: '6px 14px', fontSize: '0.82rem', borderRadius: '8px', background: isDeployed ? '#10b981' : 'var(--gradient-brand)', color: 'white', border: 'none', cursor: isDeployed ? 'default' : 'pointer' }}
                          disabled={isDeployed || deploying === rec.route_number}
                          onClick={() => handleDeployBus(rec.route_number)}
                        >
                          {isDeployed ? '✓ Reviewed' : deploying === rec.route_number ? 'Saving...' : 'Mark Reviewed'}
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="text-muted" style={{ fontSize: '0.88rem', margin: 0 }}>
                {dispatchData.note || "No commuter votes recorded yet for dispatch analysis."}
              </p>
            )}
          </div>
        )}
      </motion.div>
    </div>
  );
}