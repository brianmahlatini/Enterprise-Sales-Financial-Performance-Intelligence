import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { BarChart3, Filter, LineChart, ShieldCheck, Target, TrendingUp } from 'lucide-react';
import { Bar, BarChart, CartesianGrid, Legend, Line, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import './styles.css';

const API = 'http://127.0.0.1:8000/api';
const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
const pct = new Intl.NumberFormat('en-US', { style: 'percent', maximumFractionDigits: 1 });

function Metric({ icon: Icon, label, value, subtext }) {
  return (
    <section className="metric">
      <div className="metricIcon"><Icon size={20} /></div>
      <div>
        <p>{label}</p>
        <strong>{value}</strong>
        <span>{subtext}</span>
      </div>
    </section>
  );
}

function App() {
  const [filters, setFilters] = useState(null);
  const [params, setParams] = useState({ region: 'All', segment: 'All', start: '2022-01-01', end: '2025-12-31' });
  const [kpis, setKpis] = useState(null);
  const [trends, setTrends] = useState([]);
  const [breakdown, setBreakdown] = useState([]);
  const [customers, setCustomers] = useState([]);

  const query = useMemo(() => new URLSearchParams(params).toString(), [params]);

  useEffect(() => {
    fetch(`${API}/filters`).then((r) => r.json()).then((data) => {
      setFilters(data);
      setParams((p) => ({ ...p, start: data.minDate, end: data.maxDate }));
    });
    fetch(`${API}/customers/top`).then((r) => r.json()).then(setCustomers);
  }, []);

  useEffect(() => {
    fetch(`${API}/kpis?${query}`).then((r) => r.json()).then(setKpis);
    fetch(`${API}/trends?${query}`).then((r) => r.json()).then(setTrends);
    fetch(`${API}/breakdown?by=region&start=${params.start}&end=${params.end}`).then((r) => r.json()).then(setBreakdown);
  }, [query, params.start, params.end]);

  if (!filters || !kpis) return <main className="loading">Loading financial intelligence...</main>;

  return (
    <main>
      <header className="topbar">
        <div>
          <span className="eyebrow">Executive dashboard</span>
          <h1>Enterprise Sales & Financial Performance Intelligence</h1>
        </div>
        <div className="trust"><ShieldCheck size={18} /> RLS-ready regional view</div>
      </header>

      <section className="filters">
        <Filter size={18} />
        <select value={params.region} onChange={(e) => setParams({ ...params, region: e.target.value })}>
          {filters.regions.map((r) => <option key={r}>{r}</option>)}
        </select>
        <select value={params.segment} onChange={(e) => setParams({ ...params, segment: e.target.value })}>
          {filters.segments.map((s) => <option key={s}>{s}</option>)}
        </select>
        <input type="date" value={params.start} onChange={(e) => setParams({ ...params, start: e.target.value })} />
        <input type="date" value={params.end} onChange={(e) => setParams({ ...params, end: e.target.value })} />
      </section>

      <section className="metrics">
        <Metric icon={TrendingUp} label="Revenue" value={money.format(kpis.revenue)} subtext={`${kpis.orders.toLocaleString()} sales orders`} />
        <Metric icon={BarChart3} label="Gross Profit" value={money.format(kpis.grossProfit)} subtext={`${pct.format(kpis.margin)} gross margin`} />
        <Metric icon={LineChart} label="YoY Growth" value={pct.format(kpis.yoyGrowth)} subtext="Current year vs prior year" />
        <Metric icon={Target} label="Target Variance" value={money.format(kpis.targetVariance)} subtext={`${pct.format(kpis.revenue / kpis.targetRevenue - 1)} against target`} />
      </section>

      <section className="grid">
        <article className="panel wide">
          <h2>Revenue and Gross Profit Trend</h2>
          <ResponsiveContainer width="100%" height={310}>
            <LineChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="period" minTickGap={26} />
              <YAxis tickFormatter={(v) => `$${Math.round(v / 1000)}k`} />
              <Tooltip formatter={(v) => money.format(v)} />
              <Legend />
              <Line type="monotone" dataKey="revenue" stroke="#0f766e" strokeWidth={3} dot={false} />
              <Line type="monotone" dataKey="gross_profit" name="gross profit" stroke="#7c3aed" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </article>

        <article className="panel">
          <h2>Regional Performance</h2>
          <ResponsiveContainer width="100%" height={310}>
            <BarChart data={breakdown}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" />
              <YAxis tickFormatter={(v) => `$${Math.round(v / 1000)}k`} />
              <Tooltip formatter={(v) => typeof v === 'number' ? money.format(v) : v} />
              <Bar dataKey="revenue" fill="#2563eb" radius={[4, 4, 0, 0]} />
              <Bar dataKey="gross_profit" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </article>
      </section>

      <section className="panel">
        <h2>Top Customers Drill-Through Table</h2>
        <table>
          <thead><tr><th>Customer</th><th>Segment</th><th>Region</th><th>Revenue</th><th>Gross Profit</th><th>Margin</th></tr></thead>
          <tbody>
            {customers.map((c) => (
              <tr key={c.customer_name}>
                <td>{c.customer_name}</td><td>{c.segment}</td><td>{c.region}</td>
                <td>{money.format(c.revenue)}</td><td>{money.format(c.gross_profit)}</td><td>{pct.format(c.margin)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
