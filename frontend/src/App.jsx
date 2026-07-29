import React, { useState, useEffect, useRef } from 'react';
import {
  LayoutDashboard,
  Calendar,
  Percent,
  Compass,
  Home,
  Coffee,
  Briefcase,
  GraduationCap,
  Trophy,
  Bus,
  MessageSquare,
  Users,
  Sparkles,
  LogOut,
  Bell,
  Search,
  ChevronRight,
  Send,
  ArrowRight,
  CheckCircle,
  AlertTriangle,
  MapPin,
  Clock,
  ExternalLink,
  BookOpen,
  User,
  Star
} from 'lucide-react';
import './index.css';

const API = "http://127.0.0.1:8000/api/v1";

// ─── Helpers ──────────────────────────────────────────────────────────────────
const apiFetch = async (url, opts = {}) => {
  const res = await fetch(`${API}${url}`, opts);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
};

const Stars = ({ rating }) => {
  const r = Math.round(rating * 2) / 2;
  return (
    <span className="stars inline-flex items-center gap-0.5">
      {[1,2,3,4,5].map(i => (
        <Star
          key={i}
          className="w-3 h-3"
          style={{
            fill: i <= r ? '#f59e0b' : 'none',
            stroke: i <= r ? '#f59e0b' : '#475569'
          }}
        />
      ))}
      <span style={{ marginLeft: 4, fontSize: 11, color: '#94a3b8' }}>{rating?.toFixed(1)}</span>
    </span>
  );
};

const Badge = ({ text, color = 'accent' }) => (
  <span className={`badge badge-${color}`}>{text}</span>
);

const Loading = () => (
  <div className="loading-spinner">
    <div className="spinner"></div>
    <p>Loading...</p>
  </div>
);

const EmptyState = ({ icon, msg }) => (
  <div className="empty-state">
    {icon && <span className="empty-icon">{icon}</span>}
    <p>{msg}</p>
  </div>
);

// ─── Navigation items ─────────────────────────────────────────────────────────
const NAV = [
  { id: 'overview',    label: 'Overview',    icon: <LayoutDashboard className="w-4 h-4" /> },
  { id: 'timetable',   label: 'Timetable',   icon: <Calendar className="w-4 h-4" /> },
  { id: 'attendance',  label: 'Attendance',  icon: <Percent className="w-4 h-4" /> },
  { id: 'navigation',  label: 'Navigation',  icon: <Compass className="w-4 h-4" /> },
  { id: 'hostel',      label: 'Hostel',      icon: <Home className="w-4 h-4" /> },
  { id: 'cafeteria',   label: 'Cafeteria',   icon: <Coffee className="w-4 h-4" /> },
  { id: 'placement',   label: 'Placement',   icon: <Briefcase className="w-4 h-4" /> },
  { id: 'exam',        label: 'Exams',       icon: <GraduationCap className="w-4 h-4" /> },
  { id: 'hackathon',   label: 'Hackathons',  icon: <Trophy className="w-4 h-4" /> },
  { id: 'transport',   label: 'Transport',   icon: <Bus className="w-4 h-4" /> },
  { id: 'feedback',    label: 'Feedback',    icon: <MessageSquare className="w-4 h-4" /> },
  { id: 'alumni',      label: 'Alumni',      icon: <Users className="w-4 h-4" /> },
  { id: 'assistant',   label: 'AI Assistant',icon: <Sparkles className="w-4 h-4" /> },
];

// ════════════════════════════════════════════════════════════════════════════════
//  LOGIN PAGE
// ════════════════════════════════════════════════════════════════════════════════
function LoginPage({ onLogin }) {
  const [sid, setSid] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const QUICK = ['S100001','S100025','S100100','S100200','S100500'];

  const handleLogin = async (id) => {
    const studentId = id || sid.trim();
    const pwd = id ? 'test' : password;
    if (!studentId) { setError('Enter a Student ID'); return; }
    if (!pwd) { setError('Enter a Password'); return; }
    setLoading(true); setError('');
    try {
      const data = await apiFetch(`/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: studentId, password: pwd })
      });
      onLogin(data);
    } catch {
      setError('Invalid ID or Password.');
    } finally { setLoading(false); }
  };

  return (
    <div className="login-bg">
      <div className="login-orb orb1"></div>
      <div className="login-orb orb2"></div>
      <div className="login-card">
        <div className="login-logo">
          <Sparkles className="logo-icon w-8 h-8 text-indigo-400" />
          <div>
            <h1 className="login-title">Smart Campus AI</h1>
            <p className="login-sub">Multi-Agent Platform · 11 Agents</p>
          </div>
        </div>
        <p className="login-desc">Powered by LangGraph · FastAPI · React</p>
        <div className="login-input-row">
          <input
            className="login-input"
            placeholder="Enter Student ID (e.g. S100001)"
            value={sid}
            onChange={e => setSid(e.target.value)}
          />
          <input
            className="login-input"
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleLogin()}
          />
          <button className="btn-primary" onClick={() => handleLogin()} disabled={loading}>
            {loading ? '...' : 'Login →'}
          </button>
        </div>
        {error && <p className="login-error">{error}</p>}
        <div className="quick-label">Quick access</div>
        <div className="quick-chips">
          {QUICK.map(id => (
            <button key={id} className="chip" onClick={() => handleLogin(id)}>{id}</button>
          ))}
        </div>
        <div className="login-features">
          {['Navigation','Hostel','Cafeteria','Placement','Exams','Hackathons','Transport','Feedback','Alumni'].map(f => (
            <span key={f} className="feature-tag">{f}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  OVERVIEW
// ════════════════════════════════════════════════════════════════════════════════
function Overview({ student }) {
  const [metrics, setMetrics] = useState(null);
  const [schedule, setSchedule] = useState([]);

  useEffect(() => {
    apiFetch(`/attendance/student/${student.student_id}`).then(d => {
      setMetrics({ pct: d.overall_percentage?.toFixed(1) || 0, courses: d.courses?.length || 0 });
    }).catch(()=>{});
    apiFetch(`/timetable/student/${student.student_id}`).then(d => {
      const today = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][new Date().getDay()];
      setSchedule((d||[]).filter(s=>s.day_of_week===today).slice(0,5));
    }).catch(()=>{});
  }, [student]);

  const cards = [
    { label: 'Attendance', value: `${metrics?.pct||0}%`, sub: 'Overall', icon: <Percent className="w-5 h-5 mx-auto mb-2 text-green-400" />, color: 'green' },
    { label: 'CGPA', value: student.cgpa?.toFixed(2), sub: 'Current', icon: <GraduationCap className="w-5 h-5 mx-auto mb-2 text-blue-400" />, color: 'blue' },
    { label: 'Courses', value: metrics?.courses||0, sub: 'Enrolled', icon: <BookOpen className="w-5 h-5 mx-auto mb-2 text-purple-400" />, color: 'purple' },
    { label: 'Semester', value: student.semester, sub: 'Current', icon: <Calendar className="w-5 h-5 mx-auto mb-2 text-orange-400" />, color: 'orange' },
  ];

  return (
    <div className="page">
      <div className="page-header">
        <h2>Welcome back, {student.name.split(' ')[0]}!</h2>
        <p className="page-sub">{student.department} · {student.email}</p>
      </div>
      <div className="metric-grid">
        {cards.map(c => (
          <div key={c.label} className={`metric-card metric-${c.color}`}>
            <div className="metric-icon">{c.icon}</div>
            <div className="metric-value">{c.value}</div>
            <div className="metric-label">{c.label}</div>
            <div className="metric-sub">{c.sub}</div>
          </div>
        ))}
      </div>
      <div className="two-col">
        <div className="card">
          <div className="card-header">
            <Calendar className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Today's Schedule</h3>
          </div>
          {schedule.length ? schedule.map((s,i) => (
            <div key={i} className="schedule-row">
              <div className="schedule-time">{s.start_time}</div>
              <div>
                <div className="schedule-course">{s.course?.name}</div>
                <div className="schedule-meta">{s.faculty?.name} · {s.classroom?.room_name}</div>
              </div>
            </div>
          )) : <EmptyState icon={<Sparkles className="w-8 h-8 text-slate-500" />} msg="No classes today!" />}
        </div>
        <div className="card">
          <div className="card-header">
            <Sparkles className="w-4 h-4 text-purple-400" />
            <h3 className="card-title">AI Agents Active</h3>
          </div>
          <div className="agent-grid-sm">
            {['Timetable','Attendance','Navigation','Hostel','Cafeteria','Placement','Exams','Hackathons','Transport','Feedback','Alumni'].map(a => (
              <div key={a} className="agent-chip">
                <span className="agent-dot"></span>{a}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  TIMETABLE
// ════════════════════════════════════════════════════════════════════════════════
function Timetable({ student }) {
  const [data, setData] = useState(null);
  const [day, setDay] = useState('Monday');
  const [loading, setLoading] = useState(true);
  const DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday'];

  useEffect(() => {
    apiFetch(`/timetable/student/${student.student_id}`)
      .then(setData).finally(()=>setLoading(false));
  }, [student]);

  const slots = data?.filter(s=>s.day_of_week===day)||[];

  return (
    <div className="page">
      <div className="page-header"><h2>Timetable Agent</h2><p className="page-sub">CSP-based schedule optimizer</p></div>
      {loading ? <Loading /> : (
        <>
          <div className="day-tabs">
            {DAYS.map(d=>(
              <button key={d} className={`day-tab ${day===d?'active':''}`} onClick={()=>setDay(d)}>{d}</button>
            ))}
          </div>
          <div className="card">
            <div className="card-header">
              <Calendar className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">{day} Classes</h3>
            </div>
            {slots.length ? slots.map((s,i)=>(
              <div key={i} className="schedule-row">
                <div className="schedule-time-block">
                  <div className="schedule-time">{s.start_time}</div>
                  <div className="schedule-end">{s.end_time}</div>
                </div>
                <div className="schedule-info">
                  <div className="schedule-course">{s.course?.name} <Badge text={s.course?.course_code} /></div>
                  <div className="schedule-meta">
                    <span className="schedule-meta-item"><User className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-slate-400" />{s.faculty?.name}</span> &nbsp;&nbsp;
                    <span className="schedule-meta-item"><Home className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-slate-400" />{s.classroom?.room_name}</span> &nbsp;&nbsp;
                    <span className="schedule-meta-item"><MapPin className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-slate-400" />{s.classroom?.building}</span>
                  </div>
                </div>
              </div>
            )) : <EmptyState icon={<Calendar className="w-8 h-8 text-slate-500" />} msg="No classes scheduled for this day" />}
          </div>
        </>
      )}
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  ATTENDANCE
// ════════════════════════════════════════════════════════════════════════════════
function Attendance({ student }) {
  const [courses, setCourses] = useState([]);
  const [risk, setRisk] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      apiFetch(`/attendance/student/${student.student_id}`),
      apiFetch(`/attendance/risk-analysis?student_id=${student.student_id}`).catch(()=>null)
    ]).then(([c, r]) => { setCourses(c.courses || []); setRisk(r); }).finally(()=>setLoading(false));
  }, [student]);

  const overall = courses.length ? (courses.reduce((s,c)=>s+c.attendance_percentage,0)/courses.length).toFixed(1) : 0;

  return (
    <div className="page">
      <div className="page-header"><h2>Attendance Agent</h2><p className="page-sub">ML-powered risk detection · Random Forest model</p></div>
      {loading ? <Loading /> : (
        <>
          <div className="metric-grid">
            <div className="metric-card metric-blue" style={{gridColumn:'span 2'}}>
              <div className="metric-icon"><Percent className="w-5 h-5 mx-auto text-blue-400" /></div>
              <div className="metric-value">{overall}%</div>
              <div className="metric-label">Overall Attendance</div>
              <div className="metric-sub">
                <span className="inline-flex items-center gap-1 justify-center w-full">
                  {overall >= 75 ? (
                    <><CheckCircle className="w-3.5 h-3.5 text-green-400" /> Safe — Above 75%</>
                  ) : (
                    <><AlertTriangle className="w-3.5 h-3.5 text-red-400" /> At Risk — Below 75%</>
                  )}
                </span>
              </div>
            </div>
            {risk && (
              <div className={`metric-card ${risk.risk_level === 'High' ? 'metric-orange' : 'metric-green'}`} style={{gridColumn:'span 2'}}>
                <div className="metric-icon"><Sparkles className="w-5 h-5 mx-auto text-purple-400" /></div>
                <div className="metric-value">{risk.risk_level || 'Low'}</div>
                <div className="metric-label">ML Risk Level</div>
                <div className="metric-sub">Random Forest Prediction</div>
              </div>
            )}
          </div>
          <div className="card">
            <div className="card-header">
              <BookOpen className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">Course-wise Breakdown</h3>
            </div>
            {courses.map((c,i) => (
              <div key={i} className="attendance-row">
                <div className="att-info">
                  <div className="att-course">{c.course_name} <Badge text={c.course_code} color={c.attendance_percentage >= 75 ? 'green' : 'red'} /></div>
                  <div className="att-meta">{c.present_classes}/{c.total_classes} classes · {c.attendance_percentage?.toFixed(1)}%
                    {c.attendance_percentage < 75 && <span className="shortage-tag"> · Need {Math.ceil((0.75*c.total_classes - c.present_classes)/0.25)} more</span>}
                  </div>
                </div>
                <div className="att-bar-wrap">
                  <div className="att-bar">
                    <div className="att-fill" style={{ width:`${Math.min(c.attendance_percentage,100)}%`, background: c.attendance_percentage>=75?'#22c55e':'#ef4444' }}></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  NAVIGATION
// ════════════════════════════════════════════════════════════════════════════════
function Navigation({ student }) {
  const [buildings, setBuildings] = useState([]);
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [route, setRoute] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    apiFetch('/navigation/buildings').then(setBuildings).catch(()=>{});
  }, []);

  const findRoute = async () => {
    if (!from || !to) { setError('Select both From and To buildings'); return; }
    setLoading(true); setError(''); setRoute(null);
    try {
      const data = await apiFetch(`/navigation/route?from_building=${encodeURIComponent(from)}&to_building=${encodeURIComponent(to)}`);
      setRoute(data);
    } catch { setError('No route found between selected buildings.'); }
    finally { setLoading(false); }
  };

  const byType = buildings.reduce((acc,b) => { (acc[b.type]=acc[b.type]||[]).push(b); return acc; }, {});

  return (
    <div className="page">
      <div className="page-header"><h2>Campus Navigation Agent</h2><p className="page-sub">A* pathfinding algorithm · Dijkstra shortest route</p></div>
      <div className="two-col">
        <div className="card">
          <div className="card-header">
            <Search className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Find Route</h3>
          </div>
          <div className="form-group">
            <label className="form-label">From Building</label>
            <select className="form-select" value={from} onChange={e=>setFrom(e.target.value)}>
              <option value="">Select building...</option>
              {buildings.map(b=><option key={b.id} value={b.name}>{b.name}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">To Building</label>
            <select className="form-select" value={to} onChange={e=>setTo(e.target.value)}>
              <option value="">Select building...</option>
              {buildings.map(b=><option key={b.id} value={b.name}>{b.name}</option>)}
            </select>
          </div>
          {error && <p className="error-text">{error}</p>}
          <button className="btn-primary" onClick={findRoute} disabled={loading}>{loading?'Finding...':'Find Shortest Route'}</button>
          {route && (
            <div className="route-result">
              <div className="route-stat"><span className="route-val">{route.walk_time_minutes} min</span><span className="route-sub">Walk Time</span></div>
              <div className="route-stat"><span className="route-val">{route.distance_estimate_meters}m</span><span className="route-sub">Distance</span></div>
              <div className="route-stat"><span className="route-val">{route.hops}</span><span className="route-sub">Hops</span></div>
              <div className="route-path">
                <strong>Path:</strong> {route.path?.join(' -> ')}
              </div>
              <Badge text={`Algorithm: ${route.algorithm}`} color="purple" />
            </div>
          )}
        </div>
        <div className="card">
          <div className="card-header">
            <Home className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Campus Buildings</h3>
          </div>
          {Object.entries(byType).map(([type, bs]) => (
            <div key={type}>
              <div className="building-type-label">{type.toUpperCase()}</div>
              {bs.map(b=>(
                <div key={b.id} className="building-row">
                  <span className="building-name">{b.name}</span>
                  <Badge text={`${b.floors}F`} color="purple" />
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  HOSTEL
// ════════════════════════════════════════════════════════════════════════════════
function Hostel({ student }) {
  const [info, setInfo] = useState(null);
  const [complaints, setComplaints] = useState([]);
  const [menu, setMenu] = useState([]);
  const [complaintText, setComplaintText] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [msg, setMsg] = useState('');

  useEffect(() => {
    apiFetch(`/hostel/student/${student.student_id}`).then(setInfo).catch(()=>setInfo({hostel_allocated:false}));
    apiFetch(`/hostel/complaints/${student.student_id}`).then(setComplaints).catch(()=>{});
    apiFetch('/hostel/mess-menu').then(setMenu).catch(()=>{});
  }, [student]);

  const fileComplaint = async () => {
    if (!complaintText.trim()) return;
    setSubmitting(true);
    try {
      const res = await apiFetch('/hostel/complaint', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ student_id: student.student_id, complaint_text: complaintText })
      });
      setMsg(res.message); setComplaintText('');
      apiFetch(`/hostel/complaints/${student.student_id}`).then(setComplaints).catch(()=>{});
    } catch { setMsg('Failed to submit complaint'); }
    finally { setSubmitting(false); }
  };

  const dayMenu = menu.filter(m => m.day === ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][new Date().getDay()]);

  return (
    <div className="page">
      <div className="page-header"><h2>Hostel Assistant Agent</h2><p className="page-sub">Complaint classifier · TF-IDF · Mess menu</p></div>
      <div className="two-col">
        <div>
          {info?.hostel_allocated ? (
            <div className="card">
              <div className="card-header">
                <Home className="w-4 h-4 text-indigo-400" />
                <h3 className="card-title">Your Room</h3>
              </div>
              <div className="info-grid">
                <div className="info-item"><div className="info-label">Hostel</div><div className="info-val">{info.hostel_name}</div></div>
                <div className="info-item"><div className="info-label">Room</div><div className="info-val">{info.room_number} ({info.room_type})</div></div>
                <div className="info-item"><div className="info-label">Floor</div><div className="info-val">{info.floor}</div></div>
                <div className="info-item"><div className="info-label">Fee</div><div className="info-val">₹{info.monthly_fee}/mo</div></div>
                <div className="info-item"><div className="info-label">Warden</div><div className="info-val">{info.warden_name}</div></div>
                <div className="info-item"><div className="info-label">Phone</div><div className="info-val">{info.warden_phone}</div></div>
              </div>
            </div>
          ) : (
            <div className="card"><EmptyState icon={<Home className="w-8 h-8 text-slate-500" />} msg="No hostel allocation found for your account" /></div>
          )}
          <div className="card" style={{marginTop:16}}>
            <div className="card-header">
              <MessageSquare className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">File Complaint</h3>
            </div>
            <textarea className="form-textarea" rows={3} placeholder="Describe your complaint (e.g. water leakage, broken light...)" value={complaintText} onChange={e=>setComplaintText(e.target.value)} />
            {msg && <p className="info-text">{msg}</p>}
            <button className="btn-primary" onClick={fileComplaint} disabled={submitting}>{submitting?'Submitting...':'Submit (Auto-Classify)'}</button>
            {complaints.length > 0 && (
              <div style={{marginTop:16}}>
                <div className="section-sub">My Complaints</div>
                {complaints.slice(0,5).map((c,i)=>(
                  <div key={i} className="complaint-row">
                    <Badge text={c.category} color="purple" /> <Badge text={c.status} color={c.status==='Resolved'?'green':c.status==='Open'?'red':'orange'} />
                    <div className="complaint-text">{c.text}</div>
                    <div className="complaint-meta">{c.filed_at}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className="card">
          <div className="card-header">
            <Coffee className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Today's Mess Menu</h3>
          </div>
          {dayMenu.length ? dayMenu.map((m,i)=>(
            <div key={i} className="menu-row">
              <div className="menu-meal"><Badge text={m.meal_type} color="blue" /></div>
              <div className="menu-items">{m.items}</div>
              {m.calories_approx && <div className="menu-cal">~{m.calories_approx} cal</div>}
            </div>
          )) : <EmptyState icon={<Coffee className="w-8 h-8 text-slate-500" />} msg="Menu not available today" />}
        </div>
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  CAFETERIA
// ════════════════════════════════════════════════════════════════════════════════
function Cafeteria({ student }) {
  const [menu, setMenu] = useState([]);
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [ratingMsg, setRatingMsg] = useState('');

  useEffect(() => {
    Promise.all([
      apiFetch('/cafeteria/menu'),
      apiFetch(`/cafeteria/recommendations/${student.student_id}`)
    ]).then(([m,r])=>{ setMenu(m); setRecs(r); }).finally(()=>setLoading(false));
  }, [student]);

  const submitRating = async (itemId, rating) => {
    try {
      await apiFetch('/cafeteria/rate', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ student_id: student.student_id, food_item_id: itemId, rating })
      });
      setRatingMsg(`Rated ${rating}/5 — Thanks!`);
      setTimeout(()=>setRatingMsg(''), 3000);
    } catch { setRatingMsg('Failed to submit rating'); }
  };

  if (loading) return <Loading />;

  return (
    <div className="page">
      <div className="page-header"><h2>Cafeteria Recommendation Agent</h2><p className="page-sub">Content-Based + Collaborative Filtering</p></div>
      {ratingMsg && <div className="toast">{ratingMsg}</div>}
      <div className="two-col">
        <div className="card">
          <div className="card-header">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Recommendations for You</h3>
          </div>
          {recs.slice(0,6).map((item,i)=>(
            <div key={i} className="food-card">
              <div className="food-header">
                <div>
                  <div className="food-name">{item.name} &nbsp; <Badge text={item.is_veg ? 'Veg' : 'Non-Veg'} color={item.is_veg ? 'green' : 'red'} /></div>
                  <div className="food-meta">{item.cuisine} · {item.category} · ₹{item.price}</div>
                </div>
                <div>
                  <Stars rating={item.avg_rating} />
                  <div className="match-badge">{item.recommendation_score}% match</div>
                </div>
              </div>
              <div className="food-tags">{item.tags?.split(',').map(t=><Badge key={t} text={t} color="purple" />)}</div>
              <div className="rating-row">
                Rate: {[1,2,3,4,5].map(n=>(
                  <button key={n} className="rate-btn" onClick={()=>submitRating(item.food_item_id, n)}>{'★'.repeat(n)}</button>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div className="card">
          <div className="card-header">
            <Coffee className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Today's Menu</h3>
          </div>
          {['Breakfast','Lunch','Snacks','Dinner'].map(slot => {
            const items = menu.filter(m=>m.meal_slot===slot);
            return items.length ? (
              <div key={slot}>
                <div className="menu-slot-label"><Badge text={slot} color="blue" /></div>
                {items.slice(0,3).map((m,i)=>(
                  <div key={i} className="menu-item-row">
                    <span>{m.name} &nbsp; <Badge text={m.is_veg ? 'Veg' : 'Non-Veg'} color={m.is_veg ? 'green' : 'red'} /></span>
                    <span className="menu-price">₹{m.price}</span>
                  </div>
                ))}
              </div>
            ) : null;
          })}
        </div>
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  PLACEMENT
// ════════════════════════════════════════════════════════════════════════════════
function Placement({ student }) {
  const [profile, setProfile] = useState(null);
  const [companies, setCompanies] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [qTopic, setQTopic] = useState('DSA');
  const [gap, setGap] = useState(null);
  const [tab, setTab] = useState('profile');
  const [loading, setLoading] = useState(true);

  const TOPICS = ['DSA','OS','DBMS','CN','Python','ML','HR','System Design'];

  useEffect(() => {
    Promise.all([
      apiFetch(`/placement/profile/${student.student_id}`),
      apiFetch(`/placement/companies/${student.student_id}`)
    ]).then(([p,c])=>{ setProfile(p); setCompanies(c); }).finally(()=>setLoading(false));
  }, [student]);

  useEffect(() => {
    apiFetch(`/placement/interview-questions?topic=${qTopic}&n=5`).then(setQuestions).catch(()=>{});
  }, [qTopic]);

  useEffect(() => {
    apiFetch('/placement/analyze-skills', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ student_id: student.student_id })
    }).then(setGap).catch(()=>{});
  }, [student]);

  if (loading) return <Loading />;

  const score = profile?.readiness_score || 0;

  return (
    <div className="page">
      <div className="page-header"><h2>Placement Preparation Agent</h2><p className="page-sub">KNN matching · TF-IDF · Interview Q&A</p></div>
      <div className="tab-row">
        {['profile','companies','interview','skills'].map(t=>(
          <button key={t} className={`tab-btn ${tab===t?'active':''}`} onClick={()=>setTab(t)}>{t.charAt(0).toUpperCase()+t.slice(1)}</button>
        ))}
      </div>
      {tab==='profile' && profile && (
        <div className="two-col">
          <div className="card">
            <div className="card-header">
              <Percent className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">Readiness Score</h3>
            </div>
            <div className="score-ring-wrap">
              <div className="score-ring" style={{'--score': score}}>
                <div className="score-inner">
                  <div className="score-val">{score}</div>
                  <div className="score-label">/ 100</div>
                </div>
              </div>
            </div>
            <div className="info-grid">
              {Object.entries(profile.score_breakdown||{}).map(([k,v])=>(
                <div key={k} className="info-item">
                  <div className="info-label">{k.replace(/_/g,' ')}</div>
                  <div className="info-val">{v}</div>
                </div>
              ))}
            </div>
          </div>
          <div className="card">
            <div className="card-header">
              <Briefcase className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">Your Skills ({profile.skill_count})</h3>
            </div>
            <div className="skill-tags">
              {profile.skills?.map(s=>(
                <span key={s.name} className={`skill-tag skill-${s.proficiency.toLowerCase()}`}>{s.name}</span>
              ))}
            </div>
            <div className="info-grid" style={{marginTop:12}}>
              <div className="info-item"><div className="info-label">Projects</div><div className="info-val">{profile.projects}</div></div>
              <div className="info-item"><div className="info-label">Internships</div><div className="info-val">{profile.internships}</div></div>
              <div className="info-item"><div className="info-label">Certifications</div><div className="info-val">{profile.certifications}</div></div>
              <div className="info-item"><div className="info-label">Mock Interviews</div><div className="info-val">{profile.mock_interviews_done}</div></div>
            </div>
          </div>
        </div>
      )}
      {tab==='companies' && (
        <div className="card">
          <div className="card-header">
            <Home className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Matched Companies ({companies.length})</h3>
          </div>
          {companies.map((c,i)=>(
            <div key={i} className="company-row">
              <div className="company-header">
                <div>
                  <div className="company-name">{c.name} <Badge text={c.industry} /></div>
                  <div className="company-meta">₹{c.package_lpa_min}–{c.package_lpa_max} LPA · Min CGPA: {c.min_cgpa}</div>
                </div>
                <div className="company-score">{c.match_score}%<div className="company-score-sub">match</div></div>
              </div>
              {c.matched_skills?.length>0 && <div className="skill-tags">{c.matched_skills.map(s=><span key={s} className="skill-tag skill-advanced">{s}</span>)}</div>}
              {c.missing_skills?.length>0 && <div className="missing-label">Learn: {c.missing_skills.join(', ')}</div>}
            </div>
          ))}
        </div>
      )}
      {tab==='interview' && (
        <div className="card">
          <div className="card-header">
            <MessageSquare className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Interview Q&amp;A</h3>
          </div>
          <div className="topic-row">
            {TOPICS.map(t=><button key={t} className={`topic-btn ${qTopic===t?'active':''}`} onClick={()=>setQTopic(t)}>{t}</button>)}
          </div>
          {questions.map((q,i)=>(
            <div key={i} className="qa-card">
              <div className="qa-q"><Badge text={q.difficulty} color={q.difficulty==='Easy'?'green':q.difficulty==='Medium'?'orange':'red'} /> {q.question}</div>
              <div className="qa-a">{q.answer}</div>
            </div>
          ))}
        </div>
      )}
      {tab==='skills' && gap && (
        <div className="two-col">
          <div className="card">
            <div className="card-header">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <h3 className="card-title">Skills You Have</h3>
            </div>
            {gap.skills_you_have?.map((s,i)=>(
              <div key={i} className="gap-row"><span className="gap-skill">{s.name}</span><Badge text={`${s.demand_count} companies`} color="green" /></div>
            ))}
          </div>
          <div className="card">
            <div className="card-header">
              <BookOpen className="w-4 h-4 text-orange-400" />
              <h3 className="card-title">Skills to Learn</h3>
            </div>
            <p className="section-sub">Completion: {gap.completion_pct}%</p>
            {gap.skills_to_learn?.map((s,i)=>(
              <div key={i} className="gap-row"><span className="gap-skill">{s.name}</span><Badge text={`${s.demand_count} companies`} color="red" /></div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  EXAM
// ════════════════════════════════════════════════════════════════════════════════
function Exam({ student }) {
  const [schedule, setSchedule] = useState(null);
  const [tickets, setTickets] = useState(null);
  const [results, setResults] = useState(null);
  const [tab, setTab] = useState('schedule');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      apiFetch(`/exam/schedule/${student.student_id}`),
      apiFetch(`/exam/hall-ticket/${student.student_id}`),
      apiFetch(`/exam/results/${student.student_id}`)
    ]).then(([s,t,r])=>{ setSchedule(s); setTickets(t); setResults(r); }).finally(()=>setLoading(false));
  }, [student]);

  if (loading) return <Loading />;

  return (
    <div className="page">
      <div className="page-header"><h2>Exam Discovery Agent</h2><p className="page-sub">Rule Engine · Countdown · Hall Tickets · Results</p></div>
      {schedule?.countdown && <div className="countdown-banner">{schedule.countdown}</div>}
      <div className="tab-row">
        {['schedule','tickets','results'].map(t=>(
          <button key={t} className={`tab-btn ${tab===t?'active':''}`} onClick={()=>setTab(t)}>{t.charAt(0).toUpperCase()+t.slice(1)}</button>
        ))}
      </div>
      {tab==='schedule' && (
        <div className="two-col">
          <div className="card">
            <div className="card-header">
              <Clock className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">Upcoming ({schedule?.total_upcoming||0})</h3>
            </div>
            {schedule?.upcoming_exams?.slice(0,6).map((e,i)=>(
              <div key={i} className="exam-row">
                <div className="exam-date-block">
                  <div className="exam-day">{new Date(e.date).getDate()}</div>
                  <div className="exam-month">{new Date(e.date).toLocaleString('default',{month:'short'})}</div>
                </div>
                <div className="exam-info">
                  <div className="exam-course">{e.course_name} <Badge text={e.exam_type} color={e.exam_type==='EndSem'?'red':'blue'} /></div>
                  <div className="exam-meta">
                    <span className="exam-meta-item"><Home className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-slate-400" />{e.venue}</span> &nbsp;·&nbsp; {e.start_time}–{e.end_time}
                  </div>
                  <div className={`days-left ${e.days_left<=3?'urgent':e.days_left<=7?'soon':''}`}>{e.days_left} days left</div>
                </div>
              </div>
            ))}
          </div>
          <div className="card">
            <div className="card-header">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <h3 className="card-title">Completed Exams</h3>
            </div>
            {schedule?.past_exams?.slice(0,6).map((e,i)=>(
              <div key={i} className="exam-row past">
                <div className="exam-course">{e.course_name} <Badge text={e.exam_type} /></div>
                <div className="exam-meta">{e.date}</div>
              </div>
            ))}
          </div>
        </div>
      )}
      {tab==='tickets' && (
        <div className="card">
          <div className="card-header">
            <GraduationCap className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Hall Tickets ({tickets?.hall_tickets?.length||0})</h3>
          </div>
          <div className="hall-ticket-header">
            <div>Student: <strong>{tickets?.name}</strong> · {tickets?.department} · Sem {tickets?.semester}</div>
          </div>
          {tickets?.hall_tickets?.map((t,i)=>(
            <div key={i} className="ticket-card">
              <div className="ticket-id">{t.ticket_id}</div>
              <div className="ticket-info">
                <div><strong>{t.course}</strong> ({t.course_code})</div>
                <div>{t.exam_type} · {t.date} · {t.time}</div>
                <div>
                  <Home className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-slate-400" />{t.venue} &nbsp;·&nbsp; Seat: <strong>{t.seat_number}</strong>
                </div>
              </div>
              <Badge text={t.is_issued?'Issued':'Pending'} color={t.is_issued?'green':'red'} />
            </div>
          ))}
        </div>
      )}
      {tab==='results' && (
        <div className="card">
          <div className="card-header">
            <Percent className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Results · Overall: {results?.overall_percentage}%</h3>
          </div>
          {results?.results?.map((r,i)=>(
            <div key={i} className="result-row">
              <div>
                <div className="result-course">{r.course} <Badge text={r.exam_type} /></div>
                <div className="result-meta">{r.date}</div>
              </div>
              <div className="result-score">
                <span className={`grade grade-${r.grade}`}>{r.grade}</span>
                <span className="result-marks">{r.marks_obtained}/{r.max_marks}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  HACKATHON
// ════════════════════════════════════════════════════════════════════════════════
function Hackathon({ student }) {
  const [recs, setRecs] = useState([]);
  const [all, setAll] = useState([]);
  const [registered, setRegistered] = useState([]);
  const [tab, setTab] = useState('recommended');
  const [msg, setMsg] = useState('');
  const [loading, setLoading] = useState(true);

  const loadData = () => {
    Promise.all([
      apiFetch(`/hackathon/recommendations/${student.student_id}`),
      apiFetch('/hackathon/all'),
      apiFetch(`/hackathon/registered/${student.student_id}`)
    ]).then(([r,a,reg])=>{ setRecs(r); setAll(a); setRegistered(reg); }).finally(()=>setLoading(false));
  };

  useEffect(() => { loadData(); }, [student]);

  const register = async (hackathonId, title) => {
    try {
      await apiFetch('/hackathon/register', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ student_id: student.student_id, hackathon_id: hackathonId })
      });
      setMsg(`Registered for "${title}"`);
      loadData();
    } catch (e) { setMsg('Already registered or error'); }
    setTimeout(()=>setMsg(''), 4000);
  };

  if (loading) return <Loading />;

  const HackCard = ({ h, showReg = true }) => (
    <div className="hack-card">
      <div className="hack-header">
        <div>
          <div className="hack-title">{h.title}</div>
          <div className="hack-meta">{h.organizer} · <Badge text={h.platform} /> · <Badge text={h.mode} color="purple" /></div>
        </div>
        {h.match_score !== undefined && <div className="hack-match">{h.match_score}%<div className="hack-match-sub">match</div></div>}
      </div>
      <div className="hack-theme">{h.theme}</div>
      <div className="hack-tags">{h.skill_tags?.map(t=><Badge key={t} text={t} color="purple" />)}</div>
      <div className="hack-footer">
        <span><Trophy className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-amber-500" />{h.prize_pool}</span>
        <span><Users className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-slate-400" />{h.team_size}</span>
        <span className={h.deadline_days_left<=7?'urgent-text':''}>
          <Calendar className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-slate-400" />{h.registration_deadline} {h.deadline_days_left!==null && `(${h.deadline_days_left}d left)`}
        </span>
      </div>
      {showReg && <button className="btn-sm" onClick={()=>register(h.id, h.title)}>Register</button>}
    </div>
  );

  return (
    <div className="page">
      <div className="page-header"><h2>Hackathon Recommendation Agent</h2><p className="page-sub">Jaccard Similarity · Content-Based Filtering</p></div>
      {msg && <div className="toast">{msg}</div>}
      <div className="tab-row">
        {[['recommended','For You'],['all','All'],['registered','Registered']].map(([t,l])=>(
          <button key={t} className={`tab-btn ${tab===t?'active':''}`} onClick={()=>setTab(t)}>{l}</button>
        ))}
      </div>
      <div className="hack-grid">
        {tab==='recommended' && recs.map((h,i)=><HackCard key={i} h={h} />)}
        {tab==='all' && all.map((h,i)=><HackCard key={i} h={h} />)}
        {tab==='registered' && registered.map((h,i)=>(
          <div key={i} className="hack-card registered">
            <HackCard h={h} showReg={false} />
            {h.team_name && <div className="team-tag">Team: {h.team_name}</div>}
            {h.result && <Badge text={h.result} color={h.result==='Winner'?'green':'blue'} />}
          </div>
        ))}
        {(tab==='recommended'&&!recs.length)||(tab==='all'&&!all.length)||(tab==='registered'&&!registered.length) ?
          <EmptyState icon={<Trophy className="w-8 h-8 text-slate-500" />} msg="No hackathons found" /> : null}
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  TRANSPORT
// ════════════════════════════════════════════════════════════════════════════════
function Transport({ student }) {
  const [buses, setBuses] = useState([]);
  const [selected, setSelected] = useState(null);
  const [stops, setStops] = useState(null);
  const [delay, setDelay] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiFetch('/transport/buses').then(setBuses).finally(()=>setLoading(false));
  }, []);

  const selectBus = async (bus) => {
    setSelected(bus); setStops(null); setDelay(null);
    const [s, d] = await Promise.all([
      apiFetch(`/transport/route/${bus.bus_number}`),
      apiFetch(`/transport/delay-prediction/${bus.bus_number}`)
    ]);
    setStops(s); setDelay(d);
  };

  if (loading) return <Loading />;

  return (
    <div className="page">
      <div className="page-header"><h2>Transport Information Agent</h2><p className="page-sub">Exponential Smoothing delay prediction · Dijkstra route planning</p></div>
      <div className="two-col">
        <div className="card">
          <div className="card-header">
            <Bus className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Campus Buses</h3>
          </div>
          {buses.map((bus,i)=>(
            <div key={i} className={`bus-row ${selected?.bus_number===bus.bus_number?'selected':''}`} onClick={()=>selectBus(bus)}>
              <div className="bus-number">{bus.bus_number}</div>
              <div className="bus-info">
                <div className="bus-route">{bus.route_name}</div>
                <div className="bus-meta">Capacity: {bus.capacity} · {bus.stop_count} stops · Driver: {bus.driver_name}</div>
              </div>
            </div>
          ))}
        </div>
        <div>
          {delay && (
            <div className={`card delay-card ${delay.predicted_delay_minutes > 10 ? 'delay-high' : delay.predicted_delay_minutes > 2 ? 'delay-med' : 'delay-low'}`}>
              <div className="card-header" style={{justifyContent: 'center'}}>
                <Clock className="w-4 h-4 text-indigo-400" />
                <h3 className="card-title">Delay Prediction — {selected?.bus_number}</h3>
              </div>
              <div className="delay-val">{delay.predicted_delay_minutes} min</div>
              <Badge text={delay.status} color={delay.predicted_delay_minutes<=2?'green':delay.predicted_delay_minutes<=10?'orange':'red'} />
              <div className="delay-meta">Avg: {delay.historical_avg_delay} min · Reason: {delay.common_reason} · {delay.confidence} confidence</div>
            </div>
          )}
          {stops && (
            <div className="card" style={{marginTop:16}}>
              <div className="card-header">
                <MapPin className="w-4 h-4 text-indigo-400" />
                <h3 className="card-title">Route Stops — {selected?.bus_number}</h3>
              </div>
              {stops.stops?.map((s,i)=>(
                <div key={i} className="stop-row">
                  <div className="stop-num">{s.order}</div>
                  <div className="stop-info">
                    <div className="stop-name">{s.name}</div>
                    <div className="stop-time">{s.scheduled_arrival}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
          {!selected && <EmptyState icon={<Bus className="w-8 h-8 text-slate-500" />} msg="Select a bus to see stops and delay prediction" />}
        </div>
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  FEEDBACK
// ════════════════════════════════════════════════════════════════════════════════
function Feedback({ student }) {
  const [summary, setSummary] = useState(null);
  const [rating, setRating] = useState(4);
  const [text, setText] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [msg, setMsg] = useState('');
  const [sentiment, setSentiment] = useState('');

  useEffect(() => {
    apiFetch('/feedback/summary').then(setSummary).catch(()=>{});
  }, []);

  const submitFeedback = async () => {
    if (!text.trim()) { setMsg('Please write some feedback'); return; }
    setSubmitting(true);
    try {
      const res = await apiFetch('/feedback/submit', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ student_id: student.student_id, form_id: 1, rating, feedback_text: text })
      });
      setSentiment(res.sentiment);
      setMsg(`Submitted! Sentiment detected: ${res.sentiment} (score: ${res.sentiment_score?.toFixed(2)})`);
      setText(''); setRating(4);
      apiFetch('/feedback/summary').then(setSummary).catch(()=>{});
    } catch { setMsg('Failed to submit'); }
    finally { setSubmitting(false); }
  };

  return (
    <div className="page">
      <div className="page-header"><h2>Feedback Collection Agent</h2><p className="page-sub">TextBlob Sentiment Analysis · Real-time analytics</p></div>
      <div className="two-col">
        <div className="card">
          <h3 className="card-title">Submit Feedback</h3>
          <div className="form-group">
            <label className="form-label">Your Rating</label>
            <div className="rating-select">
              {[1,2,3,4,5].map(n=>(
                <button key={n} className={`rate-star ${rating>=n?'active':''}`} onClick={()=>setRating(n)}>★</button>
              ))}
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Your Feedback</label>
            <textarea className="form-textarea" rows={4} placeholder="Write your feedback about faculty, courses, facilities..." value={text} onChange={e=>setText(e.target.value)} />
          </div>
          {msg && <div className={`info-text ${msg.startsWith('Submitted')?'success-text':''}`}>{msg}</div>}
          <button className="btn-primary" onClick={submitFeedback} disabled={submitting}>{submitting?'Analyzing...':'Submit & Analyze Sentiment'}</button>
        </div>
        {summary && (
          <div className="card">
            <div className="card-header">
              <Percent className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">Platform Analytics</h3>
            </div>
            <div className="metric-card metric-blue" style={{marginBottom:12}}>
              <div className="metric-value">{summary.avg_platform_rating?.toFixed(1)} / 5.0</div>
              <div className="metric-label">Platform Rating</div>
              <div className="metric-sub">{summary.total_responses} responses · {summary.overall_health}</div>
            </div>
            <div className="sentiment-bars">
              {Object.entries(summary.sentiment_pct||{}).map(([sent,pct])=>(
                <div key={sent} className="sentiment-row">
                  <span className="sent-label">{sent}</span>
                  <div className="sent-bar"><div className="sent-fill" style={{width:`${pct}%`, background:sent==='Positive'?'#22c55e':sent==='Negative'?'#ef4444':'#94a3b8'}}></div></div>
                  <span className="sent-pct">{pct}%</span>
                </div>
              ))}
            </div>
            {summary.top_rated_faculty?.length > 0 && (
              <div style={{marginTop:12}}>
                <div className="section-sub">Top Rated Faculty</div>
                {summary.top_rated_faculty.map((f,i)=>(
                  <div key={i} className="faculty-row">
                    <span>{f.name}</span>
                    <Stars rating={f.avg_rating} />
                    <span className="fac-count">({f.response_count})</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  ALUMNI
// ════════════════════════════════════════════════════════════════════════════════
function Alumni({ student }) {
  const [recs, setRecs] = useState([]);
  const [all, setAll] = useState([]);
  const [myMentors, setMyMentors] = useState([]);
  const [tab, setTab] = useState('recommended');
  const [msg, setMsg] = useState('');
  const [loading, setLoading] = useState(true);

  const loadData = () => {
    Promise.all([
      apiFetch(`/alumni/recommendations/${student.student_id}`),
      apiFetch('/alumni/all?is_mentor=true'),
      apiFetch(`/alumni/my-mentors/${student.student_id}`)
    ]).then(([r,a,m])=>{ setRecs(r); setAll(a); setMyMentors(m); }).finally(()=>setLoading(false));
  };

  useEffect(() => { loadData(); }, [student]);

  const requestMentorship = async (alumniId, name) => {
    try {
      await apiFetch('/alumni/request-mentorship', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ student_id: student.student_id, alumni_id: alumniId, message: 'Hi, I would love to connect and learn from your experience!', goal: 'Career Guidance' })
      });
      setMsg(`Mentorship request sent to ${name}`);
      loadData();
    } catch { setMsg('Request already pending or error'); }
    setTimeout(()=>setMsg(''), 4000);
  };

  if (loading) return <Loading />;

  const AlumniCard = ({ a }) => (
    <div className="alumni-card">
      <div className="alumni-avatar">{a.name.charAt(0)}</div>
      <div className="alumni-info">
        <div className="alumni-name">{a.name}</div>
        <div className="alumni-role">{a.current_role} @ {a.current_company}</div>
        <div className="alumni-dept">{a.department} · {a.graduation_year} · {a.experience_years} yrs exp</div>
        {a.match_score !== undefined && <div className="alumni-match">Match score: {a.match_score}% · Skill match: {a.skill_match_pct}%</div>}
        <div className="alumni-skills">{a.skills?.slice(0,4).map(s=><Badge key={s} text={s} color="purple" />)}</div>
        {a.expertise_areas?.slice(0,3).map(e=><Badge key={e} text={e} />)}
      </div>
      <button className="btn-sm" onClick={()=>requestMentorship(a.id, a.name)}>Connect</button>
    </div>
  );

  return (
    <div className="page">
      <div className="page-header"><h2>Alumni Connect Agent</h2><p className="page-sub">KNN matching · Cosine Similarity on skill vectors</p></div>
      {msg && <div className="toast">{msg}</div>}
      <div className="tab-row">
        {[['recommended','Recommended'],['all','All Alumni'],['mentors','My Mentors']].map(([t,l])=>(
          <button key={t} className={`tab-btn ${tab===t?'active':''}`} onClick={()=>setTab(t)}>{l}</button>
        ))}
      </div>
      <div className="alumni-grid">
        {tab==='recommended' && recs.map((a,i)=><AlumniCard key={i} a={a} />)}
        {tab==='all' && all.slice(0,20).map((a,i)=><AlumniCard key={i} a={a} />)}
        {tab==='mentors' && myMentors.map((m,i)=>(
          <div key={i} className="mentor-request-card">
            <div className="alumni-name">{m.alumni_name}</div>
            <div className="alumni-role">{m.alumni_role} @ {m.alumni_company}</div>
            <div className="mentor-meta">Goal: {m.goal} · <Badge text={m.status} color={m.status==='Accepted'?'green':m.status==='Pending'?'orange':'red'} /></div>
          </div>
        ))}
        {!recs.length&&tab==='recommended' ? <EmptyState icon={<Users className="w-8 h-8 text-slate-500" />} msg="No mentor matches. Add skills in Placement first." /> : null}
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  AI ASSISTANT
// ════════════════════════════════════════════════════════════════════════════════
function Assistant({ student }) {
  const [messages, setMessages] = useState([
    { role: 'bot', text: `Hi ${student.name.split(' ')[0]}! I am your Smart Campus AI Assistant. Ask me anything!` }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  const SUGGESTIONS = [
    'What is my attendance?', 'Show my timetable today', 'Any exam coming up?',
    'Recommend food for me', 'Find route to Library', 'Show hostel info',
    'Match companies for me', 'Recommend a hackathon', 'Show bus schedule',
    'Connect me with a mentor',
  ];

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const send = async (text) => {
    const q = text || input.trim();
    if (!q) return;
    setInput(''); setLoading(true);
    setMessages(m => [...m, { role: 'user', text: q }]);
    try {
      const data = await apiFetch('/orchestrator/query', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q, student_id: student.student_id })
      });
      setMessages(m => [...m, { role: 'bot', text: data.response }]);
    } catch {
      setMessages(m => [...m, { role: 'bot', text: 'Connection error. Make sure the backend is running.' }]);
    } finally { setLoading(false); }
  };

  return (
    <div className="page chat-page">
      <div className="page-header"><h2>Smart Campus AI Assistant</h2><p className="page-sub">11-Agent Orchestrator · LangGraph routing</p></div>
      <div className="chat-wrap">
        <div className="chat-messages">
          {messages.map((m,i)=>(
            <div key={i} className={`chat-msg ${m.role}`}>
              <div className="chat-bubble">
                <pre className="chat-text">{m.text}</pre>
              </div>
            </div>
          ))}
          {loading && <div className="chat-msg bot"><div className="chat-bubble typing-dots"><span></span><span></span><span></span></div></div>}
          <div ref={bottomRef} />
        </div>
        <div className="suggestion-row">
          {SUGGESTIONS.slice(0,5).map((s,i)=>(
            <button key={i} className="suggestion-chip" onClick={()=>send(s)}>{s}</button>
          ))}
        </div>
        <div className="chat-input-row">
          <input
            className="chat-input"
            placeholder="Ask about timetable, exams, hackathons, food, hostel..."
            value={input}
            onChange={e=>setInput(e.target.value)}
            onKeyDown={e=>e.key==='Enter'&&send()}
          />
          <button className="btn-send" onClick={()=>send()} disabled={loading} aria-label="Send message">
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  MAIN APP
// ════════════════════════════════════════════════════════════════════════════════
function App() {
  const [student, setStudent] = useState(null);
  const [active, setActive] = useState('overview');
  const [collapsed, setCollapsed] = useState(false);
  const [notifications, setNotifications] = useState([
    { id: 1, text: "Upcoming Exam Tomorrow", read: false, time: "1 hour ago" },
    { id: 2, text: "Attendance dropped below 80%", read: false, time: "2 hours ago" },
    { id: 3, text: "Hackathon Registration closes today", read: false, time: "4 hours ago" },
    { id: 4, text: "Bus delayed by 10 minutes", read: true, time: "1 day ago" },
    { id: 5, text: "Placement interview scheduled", read: true, time: "2 days ago" },
    { id: 6, text: "New cafeteria menu available", read: true, time: "3 days ago" },
  ]);
  const [showNotifications, setShowNotifications] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Close notifications on click outside
  useEffect(() => {
    if (!showNotifications) return;
    const handleOutsideClick = (e) => {
      if (!e.target.closest('.notification-wrap')) {
        setShowNotifications(false);
      }
    };
    document.addEventListener('click', handleOutsideClick);
    return () => document.removeEventListener('click', handleOutsideClick);
  }, [showNotifications]);

  // Clear search on active page changes
  useEffect(() => {
    setSearchQuery('');
  }, [active]);

  const toggleRead = (id) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: !n.read } : n));
  };

  const markAllRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
  };

  const SEARCH_MAPPINGS = [
    { id: 'overview',    keywords: ['overview', 'dashboard', 'home', 'main'] },
    { id: 'timetable',   keywords: ['timetable', 'schedule', 'class', 'classes', 'today'] },
    { id: 'attendance',  keywords: ['attendance', 'present', 'absent', 'percentage', 'risk', 'atten'] },
    { id: 'navigation',  keywords: ['navigation', 'map', 'route', 'building', 'buildings', 'campus', 'nav'] },
    { id: 'hostel',      keywords: ['hostel', 'room', 'mess', 'warden', 'complaint', 'host'] },
    { id: 'cafeteria',   keywords: ['cafeteria', 'canteen', 'food', 'veg', 'menu', 'cafe'] },
    { id: 'placement',   keywords: ['placement', 'jobs', 'careers', 'companies', 'readiness', 'skills', 'plac'] },
    { id: 'exam',        keywords: ['exams', 'exam', 'results', 'hall ticket', 'ticket', 'grade'] },
    { id: 'hackathon',   keywords: ['hackathons', 'hackathon', 'recommend', 'recs', 'platform', 'team', 'reg'] },
    { id: 'transport',   keywords: ['transport', 'bus', 'buses', 'route', 'delay', 'driver', 'trans'] },
    { id: 'feedback',    keywords: ['feedback', 'rating', 'sentiment', 'faculty', 'textblob'] },
    { id: 'alumni',      keywords: ['alumni', 'mentor', 'mentors', 'mentorship', 'connect', 'graduation'] },
    { id: 'assistant',   keywords: ['ai assistant', 'assistant', 'chat', 'chatbot', 'ai', 'graph', 'orchestrator'] },
  ];

  const handleSearchChange = (e) => {
    const val = e.target.value;
    setSearchQuery(val);
    const query = val.toLowerCase().trim();
    if (!query) return;

    const matched = SEARCH_MAPPINGS.find(m => 
      m.id.includes(query) ||
      NAV.find(n => n.id === m.id)?.label.toLowerCase().includes(query) ||
      m.keywords.some(k => k.startsWith(query) || query.startsWith(k))
    );

    if (matched) {
      setActive(matched.id);
    }
  };

  if (!student) return <LoginPage onLogin={setStudent} />;

  const pages = {
    overview:   <Overview   student={student} />,
    timetable:  <Timetable  student={student} />,
    attendance: <Attendance student={student} />,
    navigation: <Navigation student={student} />,
    hostel:     <Hostel     student={student} />,
    cafeteria:  <Cafeteria  student={student} />,
    placement:  <Placement  student={student} />,
    exam:       <Exam       student={student} />,
    hackathon:  <Hackathon  student={student} />,
    transport:  <Transport  student={student} />,
    feedback:   <Feedback   student={student} />,
    alumni:     <Alumni     student={student} />,
    assistant:  <Assistant  student={student} />,
  };

  const currentNav = NAV.find(n => n.id === active);
  const pageTitle = currentNav ? currentNav.label : 'Overview';
  const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });

  return (
    <div className={`dashboard ${collapsed ? 'sidebar-collapsed' : ''}`}>
      <aside className="sidebar">
        <div className="sidebar-logo" onClick={()=>setCollapsed(c=>!c)}>
          <GraduationCap className="logo-mark text-indigo-400 w-5 h-5" />
          {!collapsed && <span className="logo-text">Smart Campus</span>}
        </div>
        <div className="sidebar-profile">
          <div className="profile-avatar">{student.name.charAt(0)}</div>
          {!collapsed && (
            <div className="profile-info">
              <div className="profile-name">{student.name.split(' ')[0]}</div>
              <div className="profile-dept">{student.department} · S{student.semester}</div>
            </div>
          )}
        </div>
        <nav className="sidebar-nav">
          {NAV.map(item => (
            <button
              key={item.id}
              className={`nav-item ${active === item.id ? 'active' : ''}`}
              onClick={() => setActive(item.id)}
              title={item.label}
            >
              <span className="nav-icon">{item.icon}</span>
              {!collapsed && <span className="nav-label">{item.label}</span>}
            </button>
          ))}
        </nav>
        <button className="sidebar-logout" onClick={()=>setStudent(null)} title="Logout">
          <LogOut className="w-4 h-4" />{!collapsed && ' Logout'}
        </button>
      </aside>
      <main className="main-content">
        <header className="top-bar">
          <div className="top-bar-left">
            <div className="breadcrumbs">
              <span>Smart Campus</span>
              <ChevronRight className="w-3.5 h-3.5 separator" />
              <span className="current">{pageTitle}</span>
            </div>
            <h1 className="top-bar-title">{pageTitle}</h1>
          </div>
          <div className="top-bar-right">
            <div className="top-bar-search">
              <Search className="w-4 h-4 search-icon" />
              <input 
                type="text" 
                placeholder="Quick search..." 
                className="search-input" 
                value={searchQuery}
                onChange={handleSearchChange}
              />
            </div>
            <div className="top-bar-date">
              <Calendar className="w-4 h-4 text-slate-400" />
              <span>{currentDate}</span>
            </div>
            <div className="notification-wrap">
              <button 
                className="icon-btn notification-btn" 
                aria-label="Notifications"
                onClick={() => setShowNotifications(!showNotifications)}
              >
                <Bell className="w-4 h-4" />
                {notifications.some(n => !n.read) && <span className="badge-dot"></span>}
              </button>
              {showNotifications && (
                <div className="notification-dropdown">
                  <div className="dropdown-header">
                    <h4>Notifications</h4>
                    {notifications.some(n => !n.read) && (
                      <button className="mark-all-read" onClick={markAllRead}>
                        Mark all as read
                      </button>
                    )}
                  </div>
                  <div className="dropdown-body">
                    {notifications.length === 0 ? (
                      <div className="empty-notifications">No alerts</div>
                    ) : (
                      notifications.map(n => (
                        <div 
                          key={n.id} 
                          className={`notification-item ${n.read ? 'read' : 'unread'}`}
                          onClick={() => toggleRead(n.id)}
                        >
                          <div className="notification-text">{n.text}</div>
                          <div className="notification-time">{n.time}</div>
                          {!n.read && <span className="unread-indicator"></span>}
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>
            <div className="top-bar-avatar" title={student.name}>
              {student.name.charAt(0)}
            </div>
          </div>
        </header>
        <div className="content-inner">
          {pages[active] || <Overview student={student} />}
        </div>
      </main>
    </div>
  );
}

export default App;
