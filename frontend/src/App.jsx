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
  Lock,
  Star,
  FileText
} from 'lucide-react';
import './index.css';

const SECELogo = ({ className = "w-8 h-8", light = false, onlyCrest = false }) => {
  if (onlyCrest) {
    return (
      <svg className={className} viewBox="0 0 100 130" fill="none" xmlns="http://www.w3.org/2000/svg">
        {/* Right side filled block */}
        <path d="M52,18 L90,18 C90,18 90,65 90,85 C90,105 52,120 52,120 Z"
          fill={light ? "rgba(255,255,255,0.15)" : "#0B4EA2"}
          stroke={light ? "#FFFFFF" : "#0B4EA2"}
          strokeWidth="2" />

        {/* Left side outline lines */}
        <path d="M10,18 L48,18 C48,18 48,65 48,85 C48,105 10,120 10,120 Z"
          fill={light ? "#0B4EA2" : "#FFFFFF"}
          stroke={light ? "#FFFFFF" : "#0B4EA2"}
          strokeWidth="4" />

        {/* Dividing line between left and right halves */}
        <line x1="50" y1="18" x2="50" y2="120" stroke={light ? "#FFFFFF" : "#FFFFFF"} strokeWidth="4" />

        {/* Left side divisions */}
        <line x1="10" y1="52" x2="48" y2="52" stroke={light ? "#FFFFFF" : "#0B4EA2"} strokeWidth="3" />
        <line x1="10" y1="84" x2="48" y2="84" stroke={light ? "#FFFFFF" : "#0B4EA2"} strokeWidth="3" />

        {/* Top text above left half */}
        <text x="10" y="12" fontFamily="'Plus Jakarta Sans', sans-serif" fontSize="6.5" fontWeight="800" fill={light ? "#FFFFFF" : "#0B4EA2"} letterSpacing="-0.1">Leadership &amp; Excellence</text>

        {/* 1st box: Open Book */}
        <g transform="translate(18, 24)">
          <path d="M4,11 C8,9 14,10 14,10 C14,10 20,9 24,11 L24,4 C20,2 14,3 14,3 C14,3 8,2 4,4 Z" fill="none" stroke={light ? "#FFFFFF" : "#0B4EA2"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          <line x1="14" y1="3" x2="14" y2="10" stroke={light ? "#FFFFFF" : "#0B4EA2"} strokeWidth="1.5" />
        </g>

        {/* 2nd box: Five-pointed Star */}
        <polygon points="29,58 32,64 39,65 34,70 35,77 29,73 23,77 24,70 19,65 26,64" fill="none" stroke={light ? "#FFFFFF" : "#0B4EA2"} strokeWidth="2" strokeLinejoin="round" />

        {/* 3rd box: Rising columns */}
        <g transform="translate(16, 90)">
          <path d="M2,24 L2,16 L10,10 L18,16 L18,24" fill="none" stroke={light ? "#FFFFFF" : "#0B4EA2"} strokeWidth="2" strokeLinecap="round" />
          <line x1="6" y1="24" x2="6" y2="13" stroke={light ? "#FFFFFF" : "#0B4EA2"} strokeWidth="2" />
          <line x1="10" y1="24" x2="10" y2="10" stroke={light ? "#FFFFFF" : "#0B4EA2"} strokeWidth="2" />
          <line x1="14" y1="24" x2="14" y2="13" stroke={light ? "#FFFFFF" : "#0B4EA2"} strokeWidth="2" />
        </g>

        {/* Right side: Torch and Flame */}
        <path d="M66,54 L74,54 L72,94 L68,94 Z" fill="#FFFFFF" />
        <path d="M70,22 C73,30 79,35 77,46 C75,50 70,52 68,52 C64,52 62,48 64,42 C64,36 68,34 68,30 C68,26 65,26 65,22 C67,26 71,28 71,32 C71,36 67,38 67,42 C67,46 72,48 73,44 C74,40 70,36 70,22 Z" fill="#FFC107" />
      </svg>
    );
  }

  // Full Horizontal Logo (Crest + Typography)
  return (
    <svg className={className} viewBox="0 0 450 160" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Crest portion on the left */}
      <g id="crest" transform="translate(10, 10)">
        <path d="M52,18 L90,18 C90,18 90,65 90,85 C90,105 52,120 52,120 Z" fill="#0B4EA2" stroke="#0B4EA2" strokeWidth="2" />
        <path d="M10,18 L48,18 C48,18 48,65 48,85 C48,105 10,120 10,120 Z" fill="#FFFFFF" stroke="#0B4EA2" strokeWidth="4" />
        <line x1="50" y1="18" x2="50" y2="120" stroke="#FFFFFF" strokeWidth="4" />
        <line x1="10" y1="52" x2="48" y2="52" stroke="#0B4EA2" strokeWidth="3" />
        <line x1="10" y1="84" x2="48" y2="84" stroke="#0B4EA2" strokeWidth="3" />
        <text x="10" y="12" fontFamily="'Plus Jakarta Sans', sans-serif" fontSize="6.5" fontWeight="800" fill="#0B4EA2" letterSpacing="-0.1">Leadership &amp; Excellence</text>
        <g transform="translate(18, 24)">
          <path d="M4,11 C8,9 14,10 14,10 C14,10 20,9 24,11 L24,4 C20,2 14,3 14,3 C14,3 8,2 4,4 Z" fill="none" stroke="#0B4EA2" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          <line x1="14" y1="3" x2="14" y2="10" stroke="#0B4EA2" strokeWidth="1.5" />
        </g>
        <polygon points="29,58 32,64 39,65 34,70 35,77 29,73 23,77 24,70 19,65 26,64" fill="none" stroke="#0B4EA2" strokeWidth="2" strokeLinejoin="round" />
        <g transform="translate(16, 90)">
          <path d="M2,24 L2,16 L10,10 L18,16 L18,24" fill="none" stroke="#0B4EA2" strokeWidth="2" strokeLinecap="round" />
          <line x1="6" y1="24" x2="6" y2="13" stroke="#0B4EA2" strokeWidth="2" />
          <line x1="10" y1="24" x2="10" y2="10" stroke="#0B4EA2" strokeWidth="2" />
          <line x1="14" y1="24" x2="14" y2="13" stroke="#0B4EA2" strokeWidth="2" />
        </g>
        <path d="M66,54 L74,54 L72,94 L68,94 Z" fill="#FFFFFF" />
        <path d="M70,22 C73,30 79,35 77,46 C75,50 70,52 68,52 C64,52 62,48 64,42 C64,36 68,34 68,30 C68,26 65,26 65,22 C67,26 71,28 71,32 C71,36 67,38 67,42 C67,46 72,48 73,44 C74,40 70,36 70,22 Z" fill="#FFC107" />
      </g>

      {/* Typography portion */}
      <g transform="translate(115, 36)">
        <text x="0" y="0" fontFamily="'Plus Jakarta Sans', 'Inter', sans-serif" fontSize="34" fontWeight="800" fill={light ? "#FFFFFF" : "#0B4EA2"} letterSpacing="-0.5">Sri Eshwar</text>
        <text x="0" y="28" fontFamily="'Plus Jakarta Sans', 'Inter', sans-serif" fontSize="20" fontWeight="700" fill={light ? "rgba(255,255,255,0.9)" : "#0D2F6F"} letterSpacing="-0.3">College of Engineering</text>
        <text x="0" y="50" fontFamily="'Plus Jakarta Sans', 'Inter', sans-serif" fontSize="14" fontWeight="700" fill={light ? "rgba(255,255,255,0.8)" : "#0B4EA2"} letterSpacing="-0.2">Coimbatore | Tamilnadu</text>
        <text x="0" y="70" fontFamily="'Plus Jakarta Sans', 'Inter', sans-serif" fontSize="13" fontWeight="800" fill={light ? "var(--gold)" : "#1E5AA8"} letterSpacing="0.2">An Autonomous Institution</text>
      </g>
    </svg>
  );
};

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
      {[1, 2, 3, 4, 5].map(i => (
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
  { id: 'overview', label: 'Overview', icon: <LayoutDashboard className="w-4 h-4" /> },
  { id: 'timetable', label: 'Timetable', icon: <Calendar className="w-4 h-4" /> },
  { id: 'attendance', label: 'Attendance', icon: <Percent className="w-4 h-4" /> },
  { id: 'exam', label: 'Exams', icon: <GraduationCap className="w-4 h-4" /> },
  { id: 'placement', label: 'Placement', icon: <Briefcase className="w-4 h-4" /> },
  { id: 'office', label: 'Office', icon: <FileText className="w-4 h-4" /> },
  { id: 'hostel', label: 'Hostel', icon: <Home className="w-4 h-4" /> },
  { id: 'transport', label: 'Transport', icon: <Bus className="w-4 h-4" /> },
  { id: 'cafeteria', label: 'Cafeteria', icon: <Coffee className="w-4 h-4" /> },
  { id: 'navigation', label: 'Navigation', icon: <Compass className="w-4 h-4" /> },
  { id: 'hackathon', label: 'Hackathons', icon: <Trophy className="w-4 h-4" /> },
  { id: 'alumni', label: 'Alumni', icon: <Users className="w-4 h-4" /> },
  { id: 'feedback', label: 'Feedback', icon: <MessageSquare className="w-4 h-4" /> },
  { id: 'assistant', label: 'AI Assistant', icon: <Sparkles className="w-4 h-4" /> },
];

// ════════════════════════════════════════════════════════════════════════════════
//  LOGIN PAGE
// ════════════════════════════════════════════════════════════════════════════════
function LoginPage({ onLogin }) {
  const [sid, setSid] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const QUICK_PROFILES = [
    { id: 'S100001', sem: 3, label: 'AI & Data Science' },
    { id: 'S100025', sem: 4, label: 'Computer Science' },
    { id: 'S100100', sem: 2, label: 'Physics' },
    { id: 'S100200', sem: 4, label: 'Mathematics' },
    { id: 'S100500', sem: 8, label: 'Business Administration (MBA)' }
  ];

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
      <div className="login-card">
        <div className="login-header">
          <div className="login-logo-container">
            <SECELogo className="w-16 h-16" />
          </div>
          <h1 className="login-title">Smart Campus AI</h1>
          <p className="login-subtitle">Sri Eshwar College Student Platform</p>
        </div>

        <div className="login-fields">
          <div className="input-group">
            <User className="input-icon w-4 h-4" />
            <input
              type="text"
              className="login-input"
              placeholder="Enter Student ID (e.g. S100001)"
              value={sid}
              onChange={e => setSid(e.target.value)}
              aria-label="Student ID"
            />
          </div>
          <div className="input-group">
            <Lock className="input-icon w-4 h-4" />
            <input
              type="password"
              className="login-input"
              placeholder="Enter password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleLogin()}
              aria-label="Password"
            />
          </div>
          {error && (
            <p className="login-error">
              <AlertTriangle className="w-4 h-4 text-red-400" />
              <span>{error}</span>
            </p>
          )}
          <button className="btn-primary login-btn" onClick={() => handleLogin()} disabled={loading}>
            {loading ? (
              <span className="loading-spinner"></span>
            ) : (
              'Sign In'
            )}
          </button>
        </div>

        <div className="login-features-list">
          <div className="feature-item">
            <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
            <span>AI Assistant</span>
          </div>
          <div className="feature-item">
            <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
            <span>Attendance Analytics</span>
          </div>
          <div className="feature-item">
            <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
            <span>Smart Timetable</span>
          </div>
          <div className="feature-item">
            <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
            <span>Placement Intelligence</span>
          </div>
          <div className="feature-item" style={{ gridColumn: 'span 2' }}>
            <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
            <span>Campus Navigation & 11 Specialized Agents</span>
          </div>
        </div>

        <div className="quick-access-section">
          <div className="quick-label">Quick access accounts</div>
          <div className="quick-grid">
            {QUICK_PROFILES.map(prof => (
              <button
                key={prof.id}
                className="quick-card"
                onClick={() => handleLogin(prof.id)}
                title={`Log in as ${prof.id}`}
              >
                <div className="quick-card-header">
                  <span className="quick-id">{prof.id}</span>
                  <span className="quick-sem">Sem {prof.sem}</span>
                </div>
                <div className="quick-dept">{prof.label}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="login-footer">
          <p>Secure Single Sign-On • Smart Campus</p>
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
    }).catch(() => { });
    apiFetch(`/timetable/student/${student.student_id}`).then(d => {
      const today = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][new Date().getDay()];
      setSchedule((d || []).filter(s => s.day_of_week === today).slice(0, 5));
    }).catch(() => { });
  }, [student]);

  const cards = [
    { label: 'Attendance', value: `${metrics?.pct || 0}%`, sub: 'Overall', icon: <Percent className="w-5 h-5 mx-auto mb-2 text-green-400" />, color: 'green' },
    { label: 'CGPA', value: student.cgpa?.toFixed(2), sub: 'Current', icon: <GraduationCap className="w-5 h-5 mx-auto mb-2 text-blue-400" />, color: 'blue' },
    { label: 'Courses', value: metrics?.courses || 0, sub: 'Enrolled', icon: <BookOpen className="w-5 h-5 mx-auto mb-2 text-purple-400" />, color: 'purple' },
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
          {schedule.length ? schedule.map((s, i) => (
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
            {['Timetable', 'Attendance', 'Navigation', 'Hostel', 'Cafeteria', 'Placement', 'Exams', 'Hackathons', 'Transport', 'Feedback', 'Alumni'].map(a => (
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
  const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

  useEffect(() => {
    apiFetch(`/timetable/student/${student.student_id}`)
      .then(setData).finally(() => setLoading(false));
  }, [student]);

  const slots = data?.filter(s => s.day_of_week === day) || [];

  return (
    <div className="page">
      <div className="page-header"><h2>Timetable Agent</h2><p className="page-sub">Manage class schedules and teacher allocations.</p></div>
      {loading ? <Loading /> : (
        <>
          <div className="day-tabs">
            {DAYS.map(d => (
              <button key={d} className={`day-tab ${day === d ? 'active' : ''}`} onClick={() => setDay(d)}>{d}</button>
            ))}
          </div>
          <div className="card">
            <div className="card-header">
              <Calendar className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">{day} Classes</h3>
            </div>
            {slots.length ? slots.map((s, i) => (
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
      apiFetch(`/attendance/risk-analysis?student_id=${student.student_id}`).catch(() => null)
    ]).then(([c, r]) => { setCourses(c.courses || []); setRisk(r); }).finally(() => setLoading(false));
  }, [student]);

  const overall = courses.length ? (courses.reduce((s, c) => s + c.attendance_percentage, 0) / courses.length).toFixed(1) : 0;

  return (
    <div className="page">
      <div className="page-header"><h2>Attendance Agent</h2><p className="page-sub">Track attendance and eligibility.</p></div>
      {loading ? <Loading /> : (
        <>
          <div className="metric-grid">
            <div className="metric-card metric-blue" style={{ gridColumn: 'span 2' }}>
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
              <div className={`metric-card ${risk.risk_level === 'High' ? 'metric-orange' : 'metric-green'}`} style={{ gridColumn: 'span 2' }}>
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
            {courses.map((c, i) => (
              <div key={i} className="attendance-row">
                <div className="att-info">
                  <div className="att-course">{c.course_name} <Badge text={c.course_code} color={c.attendance_percentage >= 75 ? 'green' : 'red'} /></div>
                  <div className="att-meta">{c.present_classes}/{c.total_classes} classes · {c.attendance_percentage?.toFixed(1)}%
                    {c.attendance_percentage < 75 && <span className="shortage-tag"> · Need {Math.ceil((0.75 * c.total_classes - c.present_classes) / 0.25)} more</span>}
                  </div>
                </div>
                <div className="att-bar-wrap">
                  <div className="att-bar">
                    <div className="att-fill" style={{ width: `${Math.min(c.attendance_percentage, 100)}%`, background: c.attendance_percentage >= 75 ? '#22c55e' : '#ef4444' }}></div>
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

  const MAP_NODES = {
    // Buildings
    "Main Gate": { x: 45.4, y: 7.8 },
    "Main Block": { x: 35.2, y: 25.4 },
    "AI Block": { x: 56.2, y: 21.8 },
    "Mech Block": { x: 56.2, y: 34.2 },
    "Office Room": { x: 47.4, y: 41.8 },
    "Amenity Center": { x: 45.2, y: 55.4 },
    "Xerox Shop": { x: 53.2, y: 53.0 },
    "Cafe Corner": { x: 59.2, y: 53.0 },
    "Medical Center": { x: 65.2, y: 53.0 },
    "Tea Shop": { x: 54.2, y: 64.0 },
    "Mario": { x: 60.2, y: 64.0 },
    "Playground": { x: 30.2, y: 51.0 },
    "Drone Block": { x: 28.2, y: 67.2 },
    "Boys Hostel A Block": { x: 75.2, y: 21.8 },
    "Boys Hostel B Block": { x: 83.2, y: 21.8 },
    "Boys Hostel C Block": { x: 75.2, y: 33.2 },
    "Boys Hostel D Block": { x: 83.2, y: 33.2 },
    "Girls Hostel A Block": { x: 75.2, y: 54.0 },
    "Girls Hostel B Block": { x: 82.2, y: 54.0 },
    "Girls Hostel C Block": { x: 79.2, y: 63.0 },

    // Junctions
    "J_Main_Road_1": { x: 43.8, y: 25.4 },
    "J_Main_Road_2": { x: 43.8, y: 34.2 },
    "J_Main_Road_3": { x: 43.8, y: 44.0 },
    "J_Playground_1": { x: 38.0, y: 47.8 },
    "J_Playground_2": { x: 38.0, y: 67.2 },
    "J_Amenity_South": { x: 45.2, y: 62.4 },
    "J_Hostel_Road_1": { x: 68.8, y: 21.8 },
    "J_Hostel_Road_2": { x: 68.8, y: 54.0 },
    "J_Shops_Row": { x: 59.2, y: 47.8 },
    "J_Shops_Bottom": { x: 57.2, y: 59.0 }
  };

  const MAP_EDGES = {
    "Main Gate": ["J_Main_Road_1"],
    "J_Main_Road_1": ["Main Gate", "Main Block", "AI Block", "J_Main_Road_2", "J_Hostel_Road_1"],
    "Main Block": ["J_Main_Road_1"],
    "AI Block": ["J_Main_Road_1"],
    "J_Main_Road_2": ["J_Main_Road_1", "Mech Block", "J_Main_Road_3"],
    "Mech Block": ["J_Main_Road_2"],
    "J_Main_Road_3": ["J_Main_Road_2", "Office Room", "Amenity Center", "J_Playground_1", "J_Shops_Row"],
    "Office Room": ["J_Main_Road_3"],
    "Amenity Center": ["J_Main_Road_3", "J_Amenity_South"],
    "J_Playground_1": ["J_Main_Road_3", "Playground", "J_Playground_2"],
    "Playground": ["J_Playground_1"],
    "J_Playground_2": ["J_Playground_1", "Drone Block", "J_Amenity_South"],
    "Drone Block": ["J_Playground_2"],
    "J_Amenity_South": ["J_Playground_2", "Amenity Center"],
    "J_Shops_Row": ["J_Main_Road_3", "Xerox Shop", "Cafe Corner", "Medical Center", "J_Hostel_Road_2"],
    "Xerox Shop": ["J_Shops_Row", "J_Shops_Bottom"],
    "Cafe Corner": ["J_Shops_Row", "J_Shops_Bottom"],
    "Medical Center": ["J_Shops_Row"],
    "J_Shops_Bottom": ["Xerox Shop", "Cafe Corner", "Tea Shop", "Mario"],
    "Tea Shop": ["J_Shops_Bottom"],
    "Mario": ["J_Shops_Bottom"],
    "J_Hostel_Road_1": ["J_Main_Road_1", "Boys Hostel A Block", "Boys Hostel C Block"],
    "Boys Hostel A Block": ["J_Hostel_Road_1", "Boys Hostel B Block"],
    "Boys Hostel B Block": ["Boys Hostel A Block"],
    "Boys Hostel C Block": ["J_Hostel_Road_1", "Boys Hostel D Block"],
    "Boys Hostel D Block": ["Boys Hostel C Block"],
    "J_Hostel_Road_2": ["J_Shops_Row", "Girls Hostel A Block", "Girls Hostel C Block"],
    "Girls Hostel A Block": ["J_Hostel_Road_2", "Girls Hostel B Block"],
    "Girls Hostel B Block": ["Girls Hostel A Block"],
    "Girls Hostel C Block": ["J_Hostel_Road_2"]
  };

  const getNodeKey = (name) => {
    if (!name) return null;
    const cleanName = name.toLowerCase().replace(/[^a-z0-9]/g, '');
    return Object.keys(MAP_NODES).find(k => k.toLowerCase().replace(/[^a-z0-9]/g, '') === cleanName) || null;
  };

  useEffect(() => {
    apiFetch('/navigation/buildings').then(setBuildings).catch(() => { });
  }, []);

  const findRoute = async () => {
    if (!from || !to) { setError('Select both From and To buildings'); return; }
    setLoading(true); setError(''); setRoute(null);
    try {
      const data = await apiFetch(`/navigation/route?from_building=${encodeURIComponent(from)}&to_building=${encodeURIComponent(to)}`);

      const startKey = getNodeKey(from);
      const endKey = getNodeKey(to);

      if (!startKey || !endKey) {
        setError('Location not found on the uploaded campus map.');
        setLoading(false);
        return;
      }

      // Dijkstra
      const dist = {};
      const prev = {};
      const queue = [];
      Object.keys(MAP_NODES).forEach(node => {
        dist[node] = Infinity;
        prev[node] = null;
      });
      dist[startKey] = 0;
      queue.push({ id: startKey, d: 0 });

      while (queue.length > 0) {
        queue.sort((a, b) => a.d - b.d);
        const u = queue.shift().id;
        if (u === endKey) break;
        const neighbors = MAP_EDGES[u] || [];
        neighbors.forEach(v => {
          const dx = MAP_NODES[u].x - MAP_NODES[v].x;
          const dy = MAP_NODES[u].y - MAP_NODES[v].y;
          const weight = Math.sqrt(dx * dx + dy * dy);
          const alt = dist[u] + weight;
          if (alt < dist[v]) {
            dist[v] = alt;
            prev[v] = u;
            queue.push({ id: v, d: alt });
          }
        });
      }

      const vPath = [];
      let curr = endKey;
      while (curr !== null) {
        vPath.push(curr);
        curr = prev[curr];
      }
      vPath.reverse();

      if (vPath[0] !== startKey) {
        setError('No valid path found on the map.');
      } else {
        setRoute({
          ...data,
          visualPath: vPath.map(k => MAP_NODES[k])
        });
      }
    } catch (err) {
      setError('No route found between selected buildings.');
    } finally {
      setLoading(false);
    }
  };

  const startCoords = getNodeKey(from) ? MAP_NODES[getNodeKey(from)] : null;
  const endCoords = getNodeKey(to) ? MAP_NODES[getNodeKey(to)] : null;

  return (
    <div className="page">
      <div className="page-header">
        <h2>Campus Navigation Agent</h2>
        <p className="page-sub">Campus building layouts and optimal walking routes.</p>
      </div>
      <div className="two-col">
        <div className="card">
          <div className="card-header">
            <Search className="w-4 h-4 text-blue-600" />
            <h3 className="card-title">Find Route</h3>
          </div>
          <div className="form-group">
            <label className="form-label">From Building</label>
            <select className="form-select" value={from} onChange={e => setFrom(e.target.value)}>
              <option value="">Select building...</option>
              {buildings.map(b => <option key={b.id} value={b.name}>{b.name}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">To Building</label>
            <select className="form-select" value={to} onChange={e => setTo(e.target.value)}>
              <option value="">Select building...</option>
              {buildings.map(b => <option key={b.id} value={b.name}>{b.name}</option>)}
            </select>
          </div>
          {error && <p className="error-text text-red-600 font-semibold my-2">{error}</p>}
          <button className="btn-primary w-full" onClick={findRoute} disabled={loading}>{loading ? 'Finding Route...' : 'Find Shortest Route'}</button>

          {route && (
            <div className="route-result mt-4 p-4 bg-slate-50 border rounded-lg">
              <div className="flex justify-between border-b pb-2 mb-2 text-sm font-semibold">
                <span>Estimated Walk: <span className="text-blue-900 font-extrabold">{route.walk_time_minutes} min</span></span>
                <span>Distance: <span className="text-blue-900 font-extrabold">{route.distance_estimate_meters}m</span></span>
              </div>
              <div className="text-xs text-slate-600 leading-relaxed">
                <strong>Walk Path:</strong> {route.path?.join(' ➔ ')}
              </div>
            </div>
          )}
        </div>

        <div className="card flex flex-col items-center">
          <div className="card-header w-full border-b pb-2 mb-4">
            <MapPin className="w-4 h-4 text-blue-600" />
            <h3 className="card-title">Sri Eshwar Campus Map Route Drawer</h3>
          </div>

          <div style={{ position: 'relative', width: '100%', overflow: 'hidden', borderRadius: '12px' }}>
            <img
              src="/campus_map.jpg"
              alt="Campus Map"
              style={{ width: '100%', height: 'auto', display: 'block', borderRadius: '12px' }}
            />
            <svg
              viewBox="0 0 100 100"
              style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none' }}
            >
              {route?.visualPath && (
                <path
                  d={`M ${route.visualPath.map(p => `${p.x} ${p.y}`).join(' L ')}`}
                  fill="none"
                  stroke="#ef4444"
                  strokeWidth="1.6"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  style={{ filter: 'drop-shadow(0 0 3px rgba(239, 68, 68, 0.6))' }}
                />
              )}
              {startCoords && (
                <circle cx={startCoords.x} cy={startCoords.y} r="2.0" fill="#22c55e" stroke="#FFFFFF" strokeWidth="0.5" />
              )}
              {endCoords && (
                <circle cx={endCoords.x} cy={endCoords.y} r="2.0" fill="#ef4444" stroke="#FFFFFF" strokeWidth="0.5" />
              )}
            </svg>
          </div>
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
    apiFetch(`/hostel/student/${student.student_id}`).then(setInfo).catch(() => setInfo({ hostel_allocated: false }));
    apiFetch(`/hostel/complaints/${student.student_id}`).then(setComplaints).catch(() => { });
    apiFetch('/hostel/mess-menu').then(setMenu).catch(() => { });
  }, [student]);

  const fileComplaint = async () => {
    if (!complaintText.trim()) return;
    setSubmitting(true);
    try {
      const res = await apiFetch('/hostel/complaint', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: student.student_id, complaint_text: complaintText })
      });
      setMsg(res.message); setComplaintText('');
      apiFetch(`/hostel/complaints/${student.student_id}`).then(setComplaints).catch(() => { });
    } catch { setMsg('Failed to submit complaint'); }
    finally { setSubmitting(false); }
  };

  const dayMenu = menu.filter(m => m.day === ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][new Date().getDay()]);

  return (
    <div className="page">
      <div className="page-header"><h2>Hostel Assistant Agent</h2><p className="page-sub">Room allocations and daily mess menu.</p></div>
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
          <div className="card" style={{ marginTop: 16 }}>
            <div className="card-header">
              <MessageSquare className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">File Complaint</h3>
            </div>
            <textarea className="form-textarea" rows={3} placeholder="Describe your complaint (e.g. water leakage, broken light...)" value={complaintText} onChange={e => setComplaintText(e.target.value)} />
            {msg && <p className="info-text">{msg}</p>}
            <button className="btn-primary" onClick={fileComplaint} disabled={submitting}>{submitting ? 'Submitting...' : 'Submit (Auto-Classify)'}</button>
            {complaints.length > 0 && (
              <div style={{ marginTop: 16 }}>
                <div className="section-sub">My Complaints</div>
                {complaints.slice(0, 5).map((c, i) => (
                  <div key={i} className="complaint-row">
                    <Badge text={c.category} color="purple" /> <Badge text={c.status} color={c.status === 'Resolved' ? 'green' : c.status === 'Open' ? 'red' : 'orange'} />
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
          {dayMenu.length ? dayMenu.map((m, i) => (
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
    ]).then(([m, r]) => { setMenu(m); setRecs(r); }).finally(() => setLoading(false));
  }, [student]);

  const submitRating = async (itemId, rating) => {
    try {
      await apiFetch('/cafeteria/rate', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: student.student_id, food_item_id: itemId, rating })
      });
      setRatingMsg(`Rated ${rating}/5 — Thanks!`);
      setTimeout(() => setRatingMsg(''), 3000);
    } catch { setRatingMsg('Failed to submit rating'); }
  };

  if (loading) return <Loading />;

  return (
    <div className="page">
      <div className="page-header"><h2>Cafeteria Recommendation Agent</h2><p className="page-sub">Daily cafeteria menu and food recommendations.</p></div>
      {ratingMsg && <div className="toast">{ratingMsg}</div>}
      <div className="two-col">
        <div className="card">
          <div className="card-header">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Recommendations for You</h3>
          </div>
          {recs.slice(0, 6).map((item, i) => (
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
              <div className="food-tags">{item.tags?.split(',').map(t => <Badge key={t} text={t} color="purple" />)}</div>
              <div className="rating-row">
                Rate: {[1, 2, 3, 4, 5].map(n => (
                  <button key={n} className="rate-btn" onClick={() => submitRating(item.food_item_id, n)}>{'★'.repeat(n)}</button>
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
          {['Breakfast', 'Lunch', 'Snacks', 'Dinner'].map(slot => {
            const items = menu.filter(m => m.meal_slot === slot);
            return items.length ? (
              <div key={slot}>
                <div className="menu-slot-label"><Badge text={slot} color="blue" /></div>
                {items.slice(0, 3).map((m, i) => (
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

  const TOPICS = ['DSA', 'OS', 'DBMS', 'CN', 'Python', 'ML', 'HR', 'System Design'];

  useEffect(() => {
    Promise.all([
      apiFetch(`/placement/profile/${student.student_id}`),
      apiFetch(`/placement/companies/${student.student_id}`)
    ]).then(([p, c]) => { setProfile(p); setCompanies(c); }).finally(() => setLoading(false));
  }, [student]);

  useEffect(() => {
    apiFetch(`/placement/interview-questions?topic=${qTopic}&n=5`).then(setQuestions).catch(() => { });
  }, [qTopic]);

  useEffect(() => {
    apiFetch('/placement/analyze-skills', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: student.student_id })
    }).then(setGap).catch(() => { });
  }, [student]);

  if (loading) return <Loading />;

  const score = profile?.readiness_score || 0;

  return (
    <div className="page">
      <div className="page-header"><h2>Placement Preparation Agent</h2><p className="page-sub">Campus recruitment updates and preparation metrics.</p></div>
      <div className="tab-row">
        {['profile', 'companies', 'interview', 'skills'].map(t => (
          <button key={t} className={`tab-btn ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>{t.charAt(0).toUpperCase() + t.slice(1)}</button>
        ))}
      </div>
      {tab === 'profile' && profile && (
        <div className="two-col">
          <div className="card">
            <div className="card-header">
              <Percent className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">Readiness Score</h3>
            </div>
            <div className="score-ring-wrap">
              <div className="score-ring" style={{ '--score': score }}>
                <div className="score-inner">
                  <div className="score-val">{score}</div>
                  <div className="score-label">/ 100</div>
                </div>
              </div>
            </div>
            <div className="info-grid">
              {Object.entries(profile.score_breakdown || {}).map(([k, v]) => (
                <div key={k} className="info-item">
                  <div className="info-label">{k.replace(/_/g, ' ')}</div>
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
              {profile.skills?.map(s => (
                <span key={s.name} className={`skill-tag skill-${s.proficiency.toLowerCase()}`}>{s.name}</span>
              ))}
            </div>
            <div className="info-grid" style={{ marginTop: 12 }}>
              <div className="info-item"><div className="info-label">Projects</div><div className="info-val">{profile.projects}</div></div>
              <div className="info-item"><div className="info-label">Internships</div><div className="info-val">{profile.internships}</div></div>
              <div className="info-item"><div className="info-label">Certifications</div><div className="info-val">{profile.certifications}</div></div>
              <div className="info-item"><div className="info-label">Mock Interviews</div><div className="info-val">{profile.mock_interviews_done}</div></div>
            </div>
          </div>
        </div>
      )}
      {tab === 'companies' && (
        <div className="card">
          <div className="card-header">
            <Home className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Matched Companies ({companies.length})</h3>
          </div>
          {companies.map((c, i) => (
            <div key={i} className="company-row">
              <div className="company-header">
                <div>
                  <div className="company-name">{c.name} <Badge text={c.industry} /></div>
                  <div className="company-meta">₹{c.package_lpa_min}–{c.package_lpa_max} LPA · Min CGPA: {c.min_cgpa}</div>
                </div>
                <div className="company-score">{c.match_score}%<div className="company-score-sub">match</div></div>
              </div>
              {c.matched_skills?.length > 0 && <div className="skill-tags">{c.matched_skills.map(s => <span key={s} className="skill-tag skill-advanced">{s}</span>)}</div>}
              {c.missing_skills?.length > 0 && <div className="missing-label">Learn: {c.missing_skills.join(', ')}</div>}
            </div>
          ))}
        </div>
      )}
      {tab === 'interview' && (
        <div className="card">
          <div className="card-header">
            <MessageSquare className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Interview Q&amp;A</h3>
          </div>
          <div className="topic-row">
            {TOPICS.map(t => <button key={t} className={`topic-btn ${qTopic === t ? 'active' : ''}`} onClick={() => setQTopic(t)}>{t}</button>)}
          </div>
          {questions.map((q, i) => (
            <div key={i} className="qa-card">
              <div className="qa-q"><Badge text={q.difficulty} color={q.difficulty === 'Easy' ? 'green' : q.difficulty === 'Medium' ? 'orange' : 'red'} /> {q.question}</div>
              <div className="qa-a">{q.answer}</div>
            </div>
          ))}
        </div>
      )}
      {tab === 'skills' && gap && (
        <div className="two-col">
          <div className="card">
            <div className="card-header">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <h3 className="card-title">Skills You Have</h3>
            </div>
            {gap.skills_you_have?.map((s, i) => (
              <div key={i} className="gap-row"><span className="gap-skill">{s.name}</span><Badge text={`${s.demand_count} companies`} color="green" /></div>
            ))}
          </div>
          <div className="card">
            <div className="card-header">
              <BookOpen className="w-4 h-4 text-orange-400" />
              <h3 className="card-title">Skills to Learn</h3>
            </div>
            <p className="section-sub">Completion: {gap.completion_pct}%</p>
            {gap.skills_to_learn?.map((s, i) => (
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
    ]).then(([s, t, r]) => { setSchedule(s); setTickets(t); setResults(r); }).finally(() => setLoading(false));
  }, [student]);

  if (loading) return <Loading />;

  return (
    <div className="page">
      <div className="page-header"><h2>Exam Discovery Agent</h2><p className="page-sub">Exam schedules, hall tickets, and results.</p></div>
      {schedule?.countdown && <div className="countdown-banner">{schedule.countdown}</div>}
      <div className="tab-row">
        {['schedule', 'tickets', 'results'].map(t => (
          <button key={t} className={`tab-btn ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>{t.charAt(0).toUpperCase() + t.slice(1)}</button>
        ))}
      </div>
      {tab === 'schedule' && (
        <div className="two-col">
          <div className="card">
            <div className="card-header">
              <Clock className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">Upcoming ({schedule?.total_upcoming || 0})</h3>
            </div>
            {schedule?.upcoming_exams?.slice(0, 6).map((e, i) => (
              <div key={i} className="exam-row">
                <div className="exam-date-block">
                  <div className="exam-day">{new Date(e.date).getDate()}</div>
                  <div className="exam-month">{new Date(e.date).toLocaleString('default', { month: 'short' })}</div>
                </div>
                <div className="exam-info">
                  <div className="exam-course">{e.course_name} <Badge text={e.exam_type} color={e.exam_type === 'EndSem' ? 'red' : 'blue'} /></div>
                  <div className="exam-meta">
                    <span className="exam-meta-item"><Home className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-slate-400" />{e.venue}</span> &nbsp;·&nbsp; {e.start_time}–{e.end_time}
                  </div>
                  <div className={`days-left ${e.days_left <= 3 ? 'urgent' : e.days_left <= 7 ? 'soon' : ''}`}>{e.days_left} days left</div>
                </div>
              </div>
            ))}
          </div>
          <div className="card">
            <div className="card-header">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <h3 className="card-title">Completed Exams</h3>
            </div>
            {schedule?.past_exams?.slice(0, 6).map((e, i) => (
              <div key={i} className="exam-row past">
                <div className="exam-course">{e.course_name} <Badge text={e.exam_type} /></div>
                <div className="exam-meta">{e.date}</div>
              </div>
            ))}
          </div>
        </div>
      )}
      {tab === 'tickets' && (
        <div className="card">
          <div className="card-header">
            <GraduationCap className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Hall Tickets ({tickets?.hall_tickets?.length || 0})</h3>
          </div>
          <div className="hall-ticket-header">
            <div>Student: <strong>{tickets?.name}</strong> · {tickets?.department} · Sem {tickets?.semester}</div>
          </div>
          {tickets?.hall_tickets?.map((t, i) => (
            <div key={i} className="ticket-card">
              <div className="ticket-id">{t.ticket_id}</div>
              <div className="ticket-info">
                <div><strong>{t.course}</strong> ({t.course_code})</div>
                <div>{t.exam_type} · {t.date} · {t.time}</div>
                <div>
                  <Home className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-slate-400" />{t.venue} &nbsp;·&nbsp; Seat: <strong>{t.seat_number}</strong>
                </div>
              </div>
              <Badge text={t.is_issued ? 'Issued' : 'Pending'} color={t.is_issued ? 'green' : 'red'} />
            </div>
          ))}
        </div>
      )}
      {tab === 'results' && (
        <div className="card">
          <div className="card-header">
            <Percent className="w-4 h-4 text-indigo-400" />
            <h3 className="card-title">Results · Overall: {results?.overall_percentage}%</h3>
          </div>
          {results?.results?.map((r, i) => (
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
    ]).then(([r, a, reg]) => { setRecs(r); setAll(a); setRegistered(reg); }).finally(() => setLoading(false));
  };

  useEffect(() => { loadData(); }, [student]);

  const register = async (hackathonId, title) => {
    try {
      await apiFetch('/hackathon/register', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: student.student_id, hackathon_id: hackathonId })
      });
      setMsg(`Registered for "${title}"`);
      loadData();
    } catch (e) { setMsg('Already registered or error'); }
    setTimeout(() => setMsg(''), 4000);
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
      <div className="hack-tags">{h.skill_tags?.map(t => <Badge key={t} text={t} color="purple" />)}</div>
      <div className="hack-footer">
        <span><Trophy className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-amber-500" />{h.prize_pool}</span>
        <span><Users className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-slate-400" />{h.team_size}</span>
        <span className={h.deadline_days_left <= 7 ? 'urgent-text' : ''}>
          <Calendar className="inline-block w-3.5 h-3.5 mr-1 align-text-bottom text-slate-400" />{h.registration_deadline} {h.deadline_days_left !== null && `(${h.deadline_days_left}d left)`}
        </span>
      </div>
      {showReg && <button className="btn-sm" onClick={() => register(h.id, h.title)}>Register</button>}
    </div>
  );

  return (
    <div className="page">
      <div className="page-header"><h2>Hackathon Recommendation Agent</h2><p className="page-sub">Contests and coding competitions matching your skills.</p></div>
      {msg && <div className="toast">{msg}</div>}
      <div className="tab-row">
        {[['recommended', 'For You'], ['all', 'All'], ['registered', 'Registered']].map(([t, l]) => (
          <button key={t} className={`tab-btn ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>{l}</button>
        ))}
      </div>
      <div className="hack-grid">
        {tab === 'recommended' && recs.map((h, i) => <HackCard key={i} h={h} />)}
        {tab === 'all' && all.map((h, i) => <HackCard key={i} h={h} />)}
        {tab === 'registered' && registered.map((h, i) => (
          <div key={i} className="hack-card registered">
            <HackCard h={h} showReg={false} />
            {h.team_name && <div className="team-tag">Team: {h.team_name}</div>}
            {h.result && <Badge text={h.result} color={h.result === 'Winner' ? 'green' : 'blue'} />}
          </div>
        ))}
        {(tab === 'recommended' && !recs.length) || (tab === 'all' && !all.length) || (tab === 'registered' && !registered.length) ?
          <EmptyState icon={<Trophy className="w-8 h-8 text-slate-500" />} msg="No hackathons found" /> : null}
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  TRANSPORT
// ════════════════════════════════════════════════════════════════════════════════
function Transport({ student }) {
  const [tab, setTab] = useState('live'); // live, booking, my-tickets
  const [buses, setBuses] = useState([]);
  const [selectedBus, setSelectedBus] = useState(null);
  const [stops, setStops] = useState(null);
  const [delay, setDelay] = useState(null);
  const [loading, setLoading] = useState(true);
  const [regionFilter, setRegionFilter] = useState('All');

  // Booking state
  const [leaveDate, setLeaveDate] = useState(() => {
    const d = new Date();
    d.setDate(d.getDate() + 7); // Default to next week
    return d.toISOString().split('T')[0];
  });
  const [bookingCity, setBookingCity] = useState('Coimbatore');
  const [bookingBusId, setBookingBusId] = useState('');
  const [bookingBoarding, setBookingBoarding] = useState('College Main Gate');
  const [bookingDrop, setBookingDrop] = useState('');
  const [roomNumber, setRoomNumber] = useState('Kaveri Block - 304');
  const [phone, setPhone] = useState('9876543210');

  const [seats, setSeats] = useState([]);
  const [selectedSeat, setSelectedSeat] = useState(null);

  // Modal states
  const [showQR, setShowQR] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  // Tickets log
  const [tickets, setTickets] = useState([]);
  const [toastMsg, setToastMsg] = useState('');

  const loadBuses = (city) => {
    setLoading(true);
    apiFetch(`/transport/buses?city=${city || 'All'}`)
      .then(setBuses)
      .finally(() => setLoading(false));
  };

  const loadTickets = () => {
    apiFetch(`/transport/my-tickets/${student.student_id}`)
      .then(setTickets);
  };

  useEffect(() => {
    loadBuses(regionFilter);
  }, [regionFilter]);

  useEffect(() => {
    loadTickets();
  }, [student]);

  // Load seats when bus or date changes in booking
  useEffect(() => {
    if (bookingBusId && leaveDate) {
      apiFetch(`/transport/seats/${bookingBusId}?date=${leaveDate}`)
        .then(setSeats);
      setSelectedSeat(null);
    }
  }, [bookingBusId, leaveDate]);

  const selectBus = async (bus) => {
    setSelectedBus(bus);
    setStops(null);
    setDelay(null);
    const [s, d] = await Promise.all([
      apiFetch(`/transport/route/${bus.bus_number}`),
      apiFetch(`/transport/delay-prediction/${bus.bus_number}`)
    ]);
    setStops(s);
    setDelay(d);
  };

  const handleApplyBooking = (e) => {
    e.preventDefault();
    if (!bookingBusId) {
      setToastMsg('Please select a bus route.');
      setTimeout(() => setToastMsg(''), 3000);
      return;
    }
    if (!selectedSeat) {
      setToastMsg('Please select a seat from the seat map.');
      setTimeout(() => setToastMsg(''), 3000);
      return;
    }
    setShowQR(true);
  };

  const handlePaymentCompleted = async () => {
    setIsProcessing(true);
    const selectedBusObj = buses.find(b => b.id === parseInt(bookingBusId));
    try {
      const res = await apiFetch('/transport/book-ticket', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_id: student.student_id,
          student_name: student.name,
          hostel_block_room: roomNumber,
          bus_id: parseInt(bookingBusId),
          seat_number: selectedSeat,
          travel_date: leaveDate,
          destination_city: bookingCity,
          boarding_point: bookingBoarding,
          drop_point: bookingDrop || selectedBusObj?.route_name.split(' ➔ ').pop() || 'Terminal',
          departure_time: selectedBusObj?.departure_time || '16:30',
          contact_phone: phone
        })
      });
      setToastMsg(res.message || 'Ticket booked successfully!');
      setShowQR(false);
      setTab('my-tickets');
      loadTickets();
      // Reload seats
      apiFetch(`/transport/seats/${bookingBusId}?date=${leaveDate}`)
        .then(setSeats);
      setSelectedSeat(null);
    } catch (err) {
      setToastMsg('Booking failed. The seat might have been taken.');
    } finally {
      setIsProcessing(false);
      setTimeout(() => setToastMsg(''), 4000);
    }
  };

  const handleCancelTicket = async (tktId) => {
    try {
      await apiFetch(`/transport/cancel-ticket/${tktId}`, { method: 'POST' });
      setToastMsg('Ticket cancelled successfully.');
      loadTickets();
      if (bookingBusId) {
        apiFetch(`/transport/seats/${bookingBusId}?date=${leaveDate}`).then(setSeats);
      }
    } catch {
      setToastMsg('Failed to cancel ticket.');
    }
    setTimeout(() => setToastMsg(''), 3000);
  };

  const handlePrintTicket = (tkt) => {
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
      <html>
        <head>
          <title>E-Ticket Pass - ${tkt.ticket_number}</title>
          <style>
            body { font-family: 'Plus Jakarta Sans', sans-serif; padding: 40px; color: #1e293b; }
            .ticket { border: 2px dashed #0b4ea2; padding: 30px; border-radius: 12px; max-width: 500px; margin: 0 auto; }
            .header { text-align: center; border-bottom: 2px solid #0b4ea2; padding-bottom: 15px; margin-bottom: 20px; }
            .title { font-size: 24px; font-weight: 800; color: #0b4ea2; }
            .subtitle { font-size: 12px; color: #64748b; margin-top: 5px; }
            .field { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 14px; }
            .label { font-weight: 600; color: #64748b; }
            .value { font-weight: 700; color: #0f172a; }
            .qr { text-align: center; margin-top: 25px; }
            .qr-box { display: inline-block; padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px; font-family: monospace; font-size: 11px; background: #f8fafc; }
          </style>
        </head>
        <body>
          <div class="ticket">
            <div class="header">
              <div class="title">SRI ESHWAR COLLEGE OF ENGINEERING</div>
              <div class="subtitle">Autonomous Institution · Coimbatore</div>
              <div style="font-size: 16px; font-weight: 700; margin-top: 10px; color: #ffc107;">HOSTELLER VACATION EXPRESS</div>
            </div>
            <div class="field"><span class="label">Ticket Number</span><span class="value">${tkt.ticket_number}</span></div>
            <div class="field"><span class="label">Passenger Name</span><span class="value">${tkt.student_name}</span></div>
            <div class="field"><span class="label">Student ID</span><span class="value">${tkt.student_id}</span></div>
            <div class="field"><span class="label">Hostel Room</span><span class="value">${tkt.hostel_block_room}</span></div>
            <div class="field"><span class="label">Travel Date</span><span class="value">${tkt.travel_date}</span></div>
            <div class="field"><span class="label">Bus Number</span><span class="value">${tkt.bus_number}</span></div>
            <div class="field"><span class="label">Seat Number</span><span class="value">${tkt.seat_number}</span></div>
            <div class="field"><span class="label">Boarding Point</span><span class="value">${tkt.boarding_point}</span></div>
            <div class="field"><span class="label">Destination Drop</span><span class="value">${tkt.drop_point}</span></div>
            <div class="field"><span class="label">Departure Time</span><span class="value">${tkt.departure_time}</span></div>
            <div class="qr">
              <div class="qr-box">
                [QR VERIFIED]<br/>
                ${tkt.qr_code_data}
              </div>
            </div>
          </div>
          <script>
            window.onload = function() { window.print(); window.close(); }
          </script>
        </body>
      </html>
    `);
    printWindow.document.close();
  };

  const filteredBuses = buses.filter(b => regionFilter === 'All' || b.city === regionFilter);
  const cityFilteredBusesForBooking = buses.filter(b => b.city === bookingCity);
  const selectedBusForBooking = buses.find(b => b.id === parseInt(bookingBusId));

  if (loading && buses.length === 0) return <Loading />;

  return (
    <div className="page">
      <div className="page-header">
        <h2>Smart Campus Transport Agent</h2>
        <p className="page-sub">Live Route Tracking, Delay Analytics & Hosteller Vacation Seat Reservation</p>
      </div>

      {toastMsg && <div className="toast">{toastMsg}</div>}

      <div className="tab-row">
        {[
          ['live', 'Live Bus Tracking'],
          ['booking', 'Vacation Leave Booking'],
          ['my-tickets', 'My Booked E-Tickets']
        ].map(([t, l]) => (
          <button
            key={t}
            className={`tab-btn ${tab === t ? 'active' : ''}`}
            onClick={() => setTab(t)}
          >
            {l}
          </button>
        ))}
      </div>

      <div className="transport-content mt-4">
        {tab === 'live' && (
          <div className="flex flex-col gap-6">
            <div className="flex flex-wrap gap-2 mb-2">
              {['All', 'Coimbatore', 'Tiruppur', 'Udumalai', 'Pollachi'].map(r => (
                <button
                  key={r}
                  className={`tab-btn px-4 py-1.5 text-xs ${regionFilter === r ? 'active' : ''}`}
                  onClick={() => setRegionFilter(r)}
                >
                  {r}
                </button>
              ))}
            </div>

            <div className="two-col">
              <div className="flex flex-col gap-4 max-h-[600px] overflow-y-auto pr-1">
                {filteredBuses.map((bus, i) => (
                  <div
                    key={i}
                    className={`bus-card cursor-pointer transition ${selectedBus?.bus_number === bus.bus_number ? 'border-l-4 border-l-blue-800' : ''}`}
                    onClick={() => selectBus(bus)}
                  >
                    <div className="bus-badge-city">{bus.city}</div>
                    <div className="flex items-center gap-2">
                      <Bus className="w-5 h-5 text-blue-600" />
                      <div className="font-extrabold text-base text-blue-900">{bus.bus_number}</div>
                    </div>
                    <div className="text-sm font-semibold text-slate-700">{bus.route_name}</div>
                    <div className="flex justify-between text-xs text-slate-500 mt-1">
                      <span>Driver: {bus.driver_name}</span>
                      <span>Speed: <span className="text-blue-700 font-bold">{bus.speed_kmh} km/h</span></span>
                    </div>
                    <div className="progress-track">
                      <div className="progress-bar-fill" style={{ width: `${bus.progress_pct}%` }}></div>
                      <div className="progress-dot" style={{ left: `${bus.progress_pct}%` }}></div>
                    </div>
                    <div className="flex justify-between text-xs font-semibold text-slate-600">
                      <span>Occupancy: {bus.occupancy} / 50 seats</span>
                      <span>Progress: {bus.progress_pct}%</span>
                    </div>
                  </div>
                ))}
              </div>

              <div>
                {delay && (
                  <div className={`card delay-card ${delay.predicted_delay_minutes > 10 ? 'delay-high' : delay.predicted_delay_minutes > 2 ? 'delay-med' : 'delay-low'}`}>
                    <div className="card-header" style={{ justifyContent: 'center' }}>
                      <Clock className="w-4 h-4 text-blue-600" />
                      <h3 className="card-title">Live Delay Prediction — {selectedBus?.bus_number}</h3>
                    </div>
                    <div className="delay-val font-extrabold text-3xl my-2 text-center text-blue-900">{delay.predicted_delay_minutes} min</div>
                    <div className="text-center mb-2">
                      <Badge text={delay.status} color={delay.predicted_delay_minutes <= 2 ? 'green' : delay.predicted_delay_minutes <= 10 ? 'orange' : 'red'} />
                    </div>
                    <div className="delay-meta text-xs text-slate-500 text-center leading-relaxed">
                      Avg Delay: {delay.historical_avg_delay} min · Reason: {delay.common_reason} <br /> Confidence: {delay.confidence}
                    </div>
                  </div>
                )}

                {stops && (
                  <div className="card mt-4">
                    <div className="card-header">
                      <MapPin className="w-4 h-4 text-blue-600" />
                      <h3 className="card-title">Route Stops & Highlights</h3>
                    </div>
                    <div className="spot-timeline">
                      {stops.stops?.map((s, i) => (
                        <div key={i} className={`spot-item ${s.is_spot ? 'is-spot font-bold text-blue-900' : 'text-slate-600'}`}>
                          <span>{s.name}</span>
                          <span className="text-xs text-slate-400 font-semibold">{s.scheduled_arrival} {s.is_spot ? '📍 Spot' : ''}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {!selectedBus && <EmptyState icon={<Bus className="w-8 h-8 text-slate-500" />} msg="Select a bus route to monitor live progress and delay predictions." />}
              </div>
            </div>
          </div>
        )}

        {tab === 'booking' && (
          <div className="two-col">
            <div className="card">
              <div className="card-header">
                <Calendar className="w-5 h-5 text-blue-600" />
                <h3 className="card-title">Leave Details</h3>
              </div>
              <form onSubmit={handleApplyBooking} className="flex flex-col gap-4">
                <div className="form-group">
                  <label className="form-label">Leave Date</label>
                  <input
                    type="date"
                    className="form-input"
                    value={leaveDate}
                    onChange={e => setLeaveDate(e.target.value)}
                    required
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Destination City</label>
                  <select
                    className="form-select"
                    value={bookingCity}
                    onChange={e => {
                      setBookingCity(e.target.value);
                      setBookingBusId('');
                      setBookingDrop('');
                    }}
                  >
                    {['Coimbatore', 'Tiruppur', 'Udumalai', 'Pollachi'].map(c => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Select Route Express</label>
                  <select
                    className="form-select"
                    value={bookingBusId}
                    onChange={e => {
                      setBookingBusId(e.target.value);
                      setBookingDrop('');
                    }}
                    required
                  >
                    <option value="">-- Choose Route --</option>
                    {cityFilteredBusesForBooking.map(b => (
                      <option key={b.id} value={b.id}>{b.bus_number} : {b.route_name}</option>
                    ))}
                  </select>
                </div>
                {selectedBusForBooking && (
                  <div className="form-group">
                    <label className="form-label">Boarding Point</label>
                    <select
                      className="form-select"
                      value={bookingBoarding}
                      onChange={e => setBookingBoarding(e.target.value)}
                    >
                      <option value="College Main Gate">College Main Gate</option>
                    </select>
                  </div>
                )}
                <div className="form-group">
                  <label className="form-label">Drop Landmark Point</label>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="e.g. Town Hall Stand"
                    value={bookingDrop}
                    onChange={e => setBookingDrop(e.target.value)}
                    required
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Hostel Room Details</label>
                  <input
                    type="text"
                    className="form-input"
                    value={roomNumber}
                    onChange={e => setRoomNumber(e.target.value)}
                    required
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Contact Phone</label>
                  <input
                    type="tel"
                    className="form-input"
                    value={phone}
                    onChange={e => setPhone(e.target.value)}
                    required
                  />
                </div>
                <div className="p-3 bg-slate-50 border rounded-lg flex justify-between items-center mt-2 text-sm">
                  <span className="font-semibold text-slate-600">Ticket Fare</span>
                  <span className="font-extrabold text-blue-900 text-lg">₹45.00</span>
                </div>
                <button type="submit" className="btn-primary w-full mt-2">Proceed to Pay &amp; Reserve Seat</button>
              </form>
            </div>

            <div className="card flex flex-col items-center">
              <div className="card-header w-full border-b pb-2 mb-4">
                <Bus className="w-5 h-5 text-blue-600" />
                <h3 className="card-title">Interactive 2x2 Cabin Seat Map</h3>
              </div>
              {!bookingBusId ? (
                <EmptyState msg="Please select a route to view seat layout map." />
              ) : (
                <div className="seat-map-container w-full">
                  <div className="bus-steering-wheel">
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">FRONT / DRIVER</span>
                  </div>
                  <div className="seats-grid">
                    {seats.filter(s => s.row <= 12).map(s => (
                      <button
                        key={s.seat_number}
                        className={`seat ${s.is_booked ? 'booked' : selectedSeat === s.seat_number ? 'selected' : 'available'}`}
                        disabled={s.is_booked}
                        onClick={() => setSelectedSeat(s.seat_number)}
                      >
                        {s.seat_number}
                      </button>
                    ))}
                  </div>
                  <div className="rear-bench-row">
                    {seats.filter(s => s.row === 13).map(s => (
                      <button
                        key={s.seat_number}
                        className={`seat ${s.is_booked ? 'booked' : selectedSeat === s.seat_number ? 'selected' : 'available'}`}
                        disabled={s.is_booked}
                        onClick={() => setSelectedSeat(s.seat_number)}
                      >
                        {s.seat_number}
                      </button>
                    ))}
                  </div>
                  <div className="seat-legend mt-4 border-t pt-3 w-full flex justify-center text-sm">
                    <div className="legend-item">
                      <span className="w-3.5 h-3.5 bg-slate-200 border rounded-sm"></span>
                      <span>Available</span>
                    </div>
                    <div className="legend-item">
                      <span className="w-3.5 h-3.5 bg-blue-600 rounded-sm"></span>
                      <span>Selected</span>
                    </div>
                    <div className="legend-item">
                      <span className="w-3.5 h-3.5 bg-slate-400 rounded-sm"></span>
                      <span>Booked</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {tab === 'my-tickets' && (
          <div className="card">
            <div className="card-header border-b pb-2 mb-4">
              <FileText className="w-5 h-5 text-blue-600" />
              <h3 className="card-title">Vacation Leave E-Tickets Log</h3>
            </div>
            {tickets.length === 0 ? (
              <EmptyState msg="You have no travel tickets registered. Hostellers can book leave travel in the Booking tab." />
            ) : (
              <div className="flex flex-col gap-6">
                {tickets.map((tkt, i) => (
                  <div key={i} className="ticket-pass border rounded-xl overflow-hidden hover:shadow-md transition">
                    <div className="p-4 bg-slate-50 border-b flex justify-between items-center">
                      <div>
                        <div className="font-extrabold text-blue-900 leading-snug">{tkt.ticket_number}</div>
                        <div className="text-xs text-slate-500 font-semibold">Travel Date: {tkt.travel_date}</div>
                      </div>
                      <Badge text={tkt.status} color={tkt.status === 'CONFIRMED' ? 'green' : 'red'} />
                    </div>
                    <div className="p-4 flex flex-col gap-4">
                      <div className="ticket-details-grid">
                        <div>
                          <div className="ticket-detail-label">Passenger</div>
                          <div className="ticket-detail-value">{tkt.student_name} ({tkt.student_id})</div>
                        </div>
                        <div>
                          <div className="ticket-detail-label">Room Number</div>
                          <div className="ticket-detail-value">{tkt.hostel_block_room}</div>
                        </div>
                        <div>
                          <div className="ticket-detail-label">Bus Number</div>
                          <div className="ticket-detail-value">{tkt.bus_number}</div>
                        </div>
                        <div>
                          <div className="ticket-detail-label">Seat ID</div>
                          <div className="ticket-detail-value">{tkt.seat_number}</div>
                        </div>
                        <div>
                          <div className="ticket-detail-label">Boarding Point</div>
                          <div className="ticket-detail-value">{tkt.boarding_point} ({tkt.departure_time})</div>
                        </div>
                        <div>
                          <div className="ticket-detail-label">Destination Drop</div>
                          <div className="ticket-detail-value">{tkt.drop_point}</div>
                        </div>
                      </div>
                      <div className="ticket-qr-area">
                        <div className="ticket-qr-box">
                          [QR VERIFIED PASS]<br />
                          {tkt.qr_code_data}
                        </div>
                      </div>
                      {tkt.status === 'CONFIRMED' && (
                        <div className="flex gap-2 justify-end border-t pt-3">
                          <button
                            className="btn-danger py-1.5 px-4 text-xs font-semibold"
                            onClick={() => handleCancelTicket(tkt.id)}
                          >
                            Cancel Pass
                          </button>
                          <button
                            className="btn-primary py-1.5 px-4 text-xs font-semibold"
                            onClick={() => handlePrintTicket(tkt)}
                          >
                            Download E-Ticket PDF
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {showQR && (
        <div className="upi-modal-overlay">
          <div className="upi-modal-card">
            <h3 className="font-extrabold text-blue-900 text-lg">Scan QR to Complete Payment</h3>
            <p className="text-xs text-slate-500">Scan using GPay, PhonePe, or BHIM UPI app</p>
            <div className="upi-qr-wrapper">
              <svg className="w-40 h-40" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                {/* Simulated QR Code lines */}
                <rect x="5" y="5" width="25" height="25" stroke="#0b4ea2" strokeWidth="6" fill="none" />
                <rect x="12" y="12" width="11" height="11" fill="#0b4ea2" />
                <rect x="70" y="5" width="25" height="25" stroke="#0b4ea2" strokeWidth="6" fill="none" />
                <rect x="77" y="12" width="11" height="11" fill="#0b4ea2" />
                <rect x="5" y="70" width="25" height="25" stroke="#0b4ea2" strokeWidth="6" fill="none" />
                <rect x="12" y="77" width="11" height="11" fill="#0b4ea2" />
                {/* Random blocks */}
                <rect x="40" y="10" width="15" height="5" fill="#123a73" />
                <rect x="45" y="20" width="10" height="10" fill="#123a73" />
                <rect x="15" y="40" width="15" height="10" fill="#123a73" />
                <rect x="35" y="45" width="20" height="15" fill="#123a73" />
                <rect x="65" y="40" width="10" height="25" fill="#123a73" />
                <rect x="10" y="60" width="5" height="5" fill="#123a73" />
                <rect x="45" y="70" width="15" height="15" fill="#123a73" />
                <rect x="75" y="70" width="10" height="10" fill="#123a73" />
                <rect x="70" y="85" width="15" height="5" fill="#123a73" />
              </svg>
              <div className="scanner-laser"></div>
            </div>
            <div className="text-sm">
              <div className="text-slate-500 font-semibold">Amount: <span className="text-blue-900 font-extrabold text-base">₹45.00</span></div>
              <div className="text-slate-400 text-xs mt-0.5">UPI ID: smartcampus@upi</div>
            </div>
            <div className="flex gap-2 w-full mt-2">
              <button
                className="btn-danger flex-1"
                onClick={() => setShowQR(false)}
                disabled={isProcessing}
              >
                Cancel
              </button>
              <button
                className="btn-primary flex-1"
                onClick={handlePaymentCompleted}
                disabled={isProcessing}
              >
                {isProcessing ? 'Processing...' : '✓ Payment Completed'}
              </button>
            </div>
          </div>
        </div>
      )}
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
    apiFetch('/feedback/summary').then(setSummary).catch(() => { });
  }, []);

  const submitFeedback = async () => {
    if (!text.trim()) { setMsg('Please write some feedback'); return; }
    setSubmitting(true);
    try {
      const res = await apiFetch('/feedback/submit', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: student.student_id, form_id: 1, rating, feedback_text: text })
      });
      setSentiment(res.sentiment);
      setMsg(`Submitted! Sentiment detected: ${res.sentiment} (score: ${res.sentiment_score?.toFixed(2)})`);
      setText(''); setRating(4);
      apiFetch('/feedback/summary').then(setSummary).catch(() => { });
    } catch { setMsg('Failed to submit'); }
    finally { setSubmitting(false); }
  };

  return (
    <div className="page">
      <div className="page-header"><h2>Feedback Collection Agent</h2><p className="page-sub">Submit course feedback and view ratings.</p></div>
      <div className="two-col">
        <div className="card">
          <h3 className="card-title">Submit Feedback</h3>
          <div className="form-group">
            <label className="form-label">Your Rating</label>
            <div className="rating-select">
              {[1, 2, 3, 4, 5].map(n => (
                <button key={n} className={`rate-star ${rating >= n ? 'active' : ''}`} onClick={() => setRating(n)}>★</button>
              ))}
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Your Feedback</label>
            <textarea className="form-textarea" rows={4} placeholder="Write your feedback about faculty, courses, facilities..." value={text} onChange={e => setText(e.target.value)} />
          </div>
          {msg && <div className={`info-text ${msg.startsWith('Submitted') ? 'success-text' : ''}`}>{msg}</div>}
          <button className="btn-primary" onClick={submitFeedback} disabled={submitting}>{submitting ? 'Analyzing...' : 'Submit & Analyze Sentiment'}</button>
        </div>
        {summary && (
          <div className="card">
            <div className="card-header">
              <Percent className="w-4 h-4 text-indigo-400" />
              <h3 className="card-title">Platform Analytics</h3>
            </div>
            <div className="metric-card metric-blue" style={{ marginBottom: 12 }}>
              <div className="metric-value">{summary.avg_platform_rating?.toFixed(1)} / 5.0</div>
              <div className="metric-label">Platform Rating</div>
              <div className="metric-sub">{summary.total_responses} responses · {summary.overall_health}</div>
            </div>
            <div className="sentiment-bars">
              {Object.entries(summary.sentiment_pct || {}).map(([sent, pct]) => (
                <div key={sent} className="sentiment-row">
                  <span className="sent-label">{sent}</span>
                  <div className="sent-bar"><div className="sent-fill" style={{ width: `${pct}%`, background: sent === 'Positive' ? '#22c55e' : sent === 'Negative' ? '#ef4444' : '#94a3b8' }}></div></div>
                  <span className="sent-pct">{pct}%</span>
                </div>
              ))}
            </div>
            {summary.top_rated_faculty?.length > 0 && (
              <div style={{ marginTop: 12 }}>
                <div className="section-sub">Top Rated Faculty</div>
                {summary.top_rated_faculty.map((f, i) => (
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
    ]).then(([r, a, m]) => { setRecs(r); setAll(a); setMyMentors(m); }).finally(() => setLoading(false));
  };

  useEffect(() => { loadData(); }, [student]);

  const requestMentorship = async (alumniId, name) => {
    try {
      await apiFetch('/alumni/request-mentorship', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: student.student_id, alumni_id: alumniId, message: 'Hi, I would love to connect and learn from your experience!', goal: 'Career Guidance' })
      });
      setMsg(`Mentorship request sent to ${name}`);
      loadData();
    } catch { setMsg('Request already pending or error'); }
    setTimeout(() => setMsg(''), 4000);
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
        <div className="alumni-skills">{a.skills?.slice(0, 4).map(s => <Badge key={s} text={s} color="purple" />)}</div>
        {a.expertise_areas?.slice(0, 3).map(e => <Badge key={e} text={e} />)}
      </div>
      <button className="btn-sm" onClick={() => requestMentorship(a.id, a.name)}>Connect</button>
    </div>
  );

  return (
    <div className="page">
      <div className="page-header"><h2>Alumni Connect Agent</h2><p className="page-sub">Connect with industry mentors and alumni.</p></div>
      {msg && <div className="toast">{msg}</div>}
      <div className="tab-row">
        {[['recommended', 'Recommended'], ['all', 'All Alumni'], ['mentors', 'My Mentors']].map(([t, l]) => (
          <button key={t} className={`tab-btn ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>{l}</button>
        ))}
      </div>
      <div className="alumni-grid">
        {tab === 'recommended' && recs.map((a, i) => <AlumniCard key={i} a={a} />)}
        {tab === 'all' && all.slice(0, 20).map((a, i) => <AlumniCard key={i} a={a} />)}
        {tab === 'mentors' && myMentors.map((m, i) => (
          <div key={i} className="mentor-request-card">
            <div className="alumni-name">{m.alumni_name}</div>
            <div className="alumni-role">{m.alumni_role} @ {m.alumni_company}</div>
            <div className="mentor-meta">Goal: {m.goal} · <Badge text={m.status} color={m.status === 'Accepted' ? 'green' : m.status === 'Pending' ? 'orange' : 'red'} /></div>
          </div>
        ))}
        {!recs.length && tab === 'recommended' ? <EmptyState icon={<Users className="w-8 h-8 text-slate-500" />} msg="No mentor matches. Add skills in Placement first." /> : null}
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
//  OFFICE
// ════════════════════════════════════════════════════════════════════════════════
function Office({ student }) {
  const [feeInfo, setFeeInfo] = useState(null);
  const [certificates, setCertificates] = useState([]);
  const [requests, setRequests] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [announcements, setAnnouncements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('fees');

  const [certType, setCertType] = useState('Bonafide Certificate');
  const [reqType, setReqType] = useState('ID Card Reissue');
  const [reqRemarks, setReqRemarks] = useState('');

  const [toastMsg, setToastMsg] = useState('');

  const loadData = () => {
    Promise.all([
      apiFetch(`/office/fees/${student.student_id}`),
      apiFetch(`/office/certificates/${student.student_id}`),
      apiFetch(`/office/requests/${student.student_id}`),
      apiFetch(`/office/documents/${student.student_id}`),
      apiFetch('/office/announcements')
    ]).then(([f, c, r, d, a]) => {
      setFeeInfo(f);
      setCertificates(c);
      setRequests(r);
      setDocuments(d);
      setAnnouncements(a);
    }).catch(err => {
      console.error("Failed to load Office data:", err);
    }).finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
  }, [student]);

  const handleApplyCertificate = async (e) => {
    e.preventDefault();
    try {
      const res = await apiFetch('/office/certificate-request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: student.student_id, certificate_type: certType })
      });
      setToastMsg(res.message || 'Certificate requested successfully!');
      loadData();
    } catch (err) {
      setToastMsg('Failed to request certificate.');
    }
    setTimeout(() => setToastMsg(''), 4000);
  };

  const handleApplyRequest = async (e) => {
    e.preventDefault();
    try {
      const res = await apiFetch('/office/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: student.student_id, request_type: reqType, remarks: reqRemarks })
      });
      setToastMsg(res.message || 'Request submitted successfully!');
      setReqRemarks('');
      loadData();
    } catch (err) {
      setToastMsg('Failed to submit request.');
    }
    setTimeout(() => setToastMsg(''), 4000);
  };

  const handleDownload = (docName) => {
    setToastMsg(`Downloading: ${docName}...`);
    setTimeout(() => setToastMsg(''), 3000);
  };

  if (loading) return <Loading />;

  return (
    <div className="page">
      <div className="page-header">
        <h2>Office & Student Services</h2>
        <p className="page-sub">Fee Ledger Statements, Academic Certificates, and Official Requests</p>
      </div>

      {toastMsg && <div className="toast">{toastMsg}</div>}

      <div className="tab-row">
        {[
          ['fees', 'Fees & Receipts'],
          ['certificates', 'Certificates'],
          ['requests', 'Office Requests'],
          ['documents', 'Academic Documents'],
          ['announcements', 'Announcements']
        ].map(([t, l]) => (
          <button
            key={t}
            className={`tab-btn ${activeTab === t ? 'active' : ''}`}
            onClick={() => setActiveTab(t)}
          >
            {l}
          </button>
        ))}
      </div>

      <div className="office-content">
        {activeTab === 'fees' && feeInfo && (
          <div className="flex flex-col gap-6">
            <div className="metric-grid">
              <div className="metric-card metric-blue">
                <div className="metric-icon"><Calendar className="w-5 h-5 text-blue-600" /></div>
                <div className="metric-value">₹{feeInfo.total_fee?.toLocaleString()}</div>
                <div className="metric-label">Total Semester Fee</div>
              </div>
              <div className="metric-card metric-green">
                <div className="metric-icon"><CheckCircle className="w-5 h-5 text-green-600" /></div>
                <div className="metric-value">₹{feeInfo.paid_amount?.toLocaleString()}</div>
                <div className="metric-label">Amount Paid</div>
              </div>
              <div className="metric-card metric-orange">
                <div className="metric-icon"><AlertTriangle className="w-5 h-5 text-amber-600" /></div>
                <div className="metric-value">₹{feeInfo.pending_balance?.toLocaleString()}</div>
                <div className="metric-label">Pending Balance</div>
              </div>
              <div className="metric-card metric-purple">
                <div className="metric-icon"><Clock className="w-5 h-5 text-purple-600" /></div>
                <div className="metric-value">{feeInfo.due_date}</div>
                <div className="metric-label">Payment Due Date</div>
              </div>
            </div>

            <div className="two-col">
              <div className="card">
                <div className="card-header">
                  <FileText className="w-5 h-5" />
                  <h3 className="card-title">Fee Breakdown</h3>
                </div>
                <div className="flex flex-col gap-3">
                  {Object.entries(feeInfo.fee_breakdown || {}).map(([key, val]) => (
                    <div key={key} className="flex justify-between border-b pb-2 text-slate-700">
                      <span className="font-semibold">{key}</span>
                      <span>₹{val?.toLocaleString()}</span>
                    </div>
                  ))}
                  {feeInfo.late_fee > 0 && (
                    <div className="flex justify-between border-b pb-2 text-red-600 font-bold">
                      <span>Late Fee</span>
                      <span>₹{feeInfo.late_fee?.toLocaleString()}</span>
                    </div>
                  )}
                  <div className="flex justify-between pt-2 text-blue-900 font-extrabold text-base">
                    <span>Grand Total</span>
                    <span>₹{((feeInfo.total_fee || 0) + (feeInfo.late_fee || 0))?.toLocaleString()}</span>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="card-header">
                  <Clock className="w-5 h-5" />
                  <h3 className="card-title">Payment History</h3>
                </div>
                {feeInfo.payment_history?.length === 0 ? (
                  <EmptyState msg="No transactions recorded." />
                ) : (
                  <div className="flex flex-col gap-3">
                    {feeInfo.payment_history?.map((p, i) => (
                      <div key={i} className="flex justify-between items-center p-3 bg-slate-50 border rounded-lg">
                        <div>
                          <div className="font-bold text-slate-800">{p.receipt_no}</div>
                          <div className="text-xs text-slate-500">{p.date} · {p.mode}</div>
                        </div>
                        <div className="text-green-700 font-extrabold">₹{p.amount?.toLocaleString()}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'certificates' && (
          <div className="two-col">
            <div className="card">
              <div className="card-header">
                <FileText className="w-5 h-5" />
                <h3 className="card-title">Request Academic Certificate</h3>
              </div>
              <form onSubmit={handleApplyCertificate} className="flex flex-col gap-4">
                <div className="form-group">
                  <label className="form-label">Certificate Type</label>
                  <select
                    className="form-select"
                    value={certType}
                    onChange={e => setCertType(e.target.value)}
                  >
                    {[
                      'Bonafide Certificate',
                      'Study Certificate',
                      'Conduct Certificate',
                      'Transfer Certificate Request',
                      'Course Completion Certificate',
                      'Internship Letter',
                      'No Dues Certificate',
                      'Fee Paid Certificate',
                      'Enrollment Certificate'
                    ].map(c => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                </div>
                <button type="submit" className="btn-primary w-full">Apply Now</button>
              </form>
            </div>

            <div className="card">
              <div className="card-header">
                <Clock className="w-5 h-5" />
                <h3 className="card-title">Requested Certificates Log</h3>
              </div>
              {certificates.length === 0 ? (
                <EmptyState msg="No active certificate applications." />
              ) : (
                <div className="flex flex-col gap-3 max-h-[400px] overflow-y-auto pr-1">
                  {certificates.map((c, i) => (
                    <div key={i} className="p-3 border rounded-lg flex justify-between items-start gap-4 text-sm">
                      <div className="flex flex-col gap-1">
                        <div className="font-bold text-slate-800">{c.certificate_type}</div>
                        <div className="text-xs text-slate-500">App ID: {c.application_number} · Applied: {c.created_date}</div>
                        {c.estimated_completion_date && (
                          <div className="text-xs text-blue-700 font-bold mt-1">Est. Completion: {c.estimated_completion_date}</div>
                        )}
                        {c.remarks && <div className="text-[11px] text-slate-600 mt-0.5 border-t pt-1 font-semibold">{c.remarks}</div>}
                      </div>
                      <Badge
                        text={c.status}
                        color={
                          c.status === 'Approved' || c.status === 'Ready for Collection'
                            ? 'green'
                            : c.status === 'Rejected'
                              ? 'red'
                              : 'orange'
                        }
                      />
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'requests' && (
          <div className="two-col">
            <div className="card">
              <div className="card-header">
                <FileText className="w-5 h-5" />
                <h3 className="card-title">Submit Administrative Request</h3>
              </div>
              <form onSubmit={handleApplyRequest} className="flex flex-col gap-4">
                <div className="form-group">
                  <label className="form-label">Request Type</label>
                  <select
                    className="form-select"
                    value={reqType}
                    onChange={e => setReqType(e.target.value)}
                  >
                    {[
                      'ID Card Reissue',
                      'Bus Pass Request',
                      'Hostel Change Request',
                      'Name Correction',
                      'Address Update',
                      'Scholarship Verification',
                      'Exam Hall Ticket Issue',
                      'Semester Registration',
                      'Document Verification',
                      'Duplicate Marksheet Request'
                    ].map(r => (
                      <option key={r} value={r}>{r}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Remarks / Description</label>
                  <textarea
                    className="form-textarea"
                    rows="3"
                    placeholder="Enter additional details..."
                    value={reqRemarks}
                    onChange={e => setReqRemarks(e.target.value)}
                    required
                  ></textarea>
                </div>
                <button type="submit" className="btn-primary w-full">Submit Request</button>
              </form>
            </div>

            <div className="card">
              <div className="card-header">
                <Clock className="w-5 h-5" />
                <h3 className="card-title">Request History</h3>
              </div>
              {requests.length === 0 ? (
                <EmptyState msg="No office requests recorded." />
              ) : (
                <div className="flex flex-col gap-3 max-h-[400px] overflow-y-auto pr-1">
                  {requests.map((r, i) => (
                    <div key={i} className="p-3 border rounded-lg flex justify-between items-start gap-4 text-sm">
                      <div className="flex flex-col gap-1">
                        <div className="font-bold text-slate-800">{r.request_type}</div>
                        <div className="text-xs text-slate-500">Req No: {r.request_number} · Created: {r.created_date}</div>
                        {r.remarks && <div className="text-xs text-slate-600 font-semibold mt-1">Remarks: {r.remarks}</div>}
                      </div>
                      <Badge
                        text={r.status}
                        color={r.status === 'Approved' ? 'green' : r.status === 'Rejected' ? 'red' : 'orange'}
                      />
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'documents' && (
          <div className="card">
            <div className="card-header">
              <FileText className="w-5 h-5" />
              <h3 className="card-title">Academic & Fee Documents</h3>
            </div>
            {documents.length === 0 ? (
              <EmptyState msg="No downloadable documents available." />
            ) : (
              <div className="flex flex-col border rounded-lg overflow-hidden">
                {documents.map((d, i) => (
                  <div key={i} className="document-row flex justify-between items-center p-4 border-b last:border-0 hover:bg-slate-50 transition">
                    <div className="flex items-center gap-3">
                      <FileText className="w-5 h-5 text-blue-600" />
                      <div>
                        <div className="font-bold text-slate-800">{d.document_name}</div>
                        <div className="text-xs text-slate-500">{d.document_type} · Available since {d.created_date}</div>
                      </div>
                    </div>
                    <button
                      className="btn-primary py-1.5 px-4 text-xs font-semibold"
                      onClick={() => handleDownload(d.document_name)}
                    >
                      Download PDF
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'announcements' && (
          <div className="card">
            <div className="card-header">
              <Bell className="w-5 h-5" />
              <h3 className="card-title">Office Announcements & Deadlines</h3>
            </div>
            {announcements.length === 0 ? (
              <EmptyState msg="No announcements." />
            ) : (
              <div className="flex flex-col gap-4">
                {announcements.map((a, i) => (
                  <div key={i} className="p-4 border-l-4 border-blue-600 bg-slate-50 rounded-r-lg flex flex-col gap-2">
                    <div className="flex justify-between items-start gap-4">
                      <h4 className="font-extrabold text-slate-800 text-base leading-snug">{a.title}</h4>
                      <Badge text={a.announcement_type} color={a.announcement_type === 'Holiday' ? 'red' : a.announcement_type === 'Deadline' ? 'orange' : 'blue'} />
                    </div>
                    <p className="text-sm text-slate-600 leading-relaxed">{a.content}</p>
                    <div className="text-[11px] text-slate-400 mt-1 font-semibold">Published: {a.publish_date} {a.expiry_date ? `· Expires: ${a.expiry_date}` : ''}</div>
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
      <div className="page-header"><h2>Smart Campus AI Assistant</h2><p className="page-sub">Ask anything about your campus.</p></div>
      <div className="chat-wrap">
        <div className="chat-messages">
          {messages.map((m, i) => (
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
          {SUGGESTIONS.slice(0, 5).map((s, i) => (
            <button key={i} className="suggestion-chip" onClick={() => send(s)}>{s}</button>
          ))}
        </div>
        <div className="chat-input-row">
          <input
            className="chat-input"
            placeholder="Ask about timetable, exams, hackathons, food, hostel..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && send()}
          />
          <button className="btn-send" onClick={() => send()} disabled={loading} aria-label="Send message">
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
    { id: 'overview', keywords: ['overview', 'dashboard', 'home', 'main'] },
    { id: 'timetable', keywords: ['timetable', 'schedule', 'class', 'classes', 'today'] },
    { id: 'attendance', keywords: ['attendance', 'present', 'absent', 'percentage', 'risk', 'atten'] },
    { id: 'navigation', keywords: ['navigation', 'map', 'route', 'building', 'buildings', 'campus', 'nav'] },
    { id: 'hostel', keywords: ['hostel', 'room', 'mess', 'warden', 'complaint', 'host'] },
    { id: 'cafeteria', keywords: ['cafeteria', 'canteen', 'food', 'veg', 'menu', 'cafe'] },
    { id: 'placement', keywords: ['placement', 'jobs', 'careers', 'companies', 'readiness', 'skills', 'plac'] },
    { id: 'exam', keywords: ['exams', 'exam', 'results', 'hall ticket', 'ticket', 'grade'] },
    { id: 'hackathon', keywords: ['hackathons', 'hackathon', 'recommend', 'recs', 'platform', 'team', 'reg'] },
    { id: 'transport', keywords: ['transport', 'bus', 'buses', 'route', 'delay', 'driver', 'trans'] },
    { id: 'feedback', keywords: ['feedback', 'rating', 'sentiment', 'faculty', 'textblob'] },
    { id: 'alumni', keywords: ['alumni', 'mentor', 'mentors', 'mentorship', 'connect', 'graduation'] },
    { id: 'office', keywords: ['fee', 'office', 'certificate', 'bonafide', 'receipt', 'payment', 'statement', 'ledger', 'announcement', 'circular', 'deadline', 'id card', 'bus pass'] },
    { id: 'assistant', keywords: ['ai assistant', 'assistant', 'chat', 'chatbot', 'ai', 'graph', 'orchestrator'] },
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
    overview: <Overview student={student} />,
    timetable: <Timetable student={student} />,
    attendance: <Attendance student={student} />,
    navigation: <Navigation student={student} />,
    hostel: <Hostel student={student} />,
    cafeteria: <Cafeteria student={student} />,
    placement: <Placement student={student} />,
    exam: <Exam student={student} />,
    hackathon: <Hackathon student={student} />,
    transport: <Transport student={student} />,
    feedback: <Feedback student={student} />,
    alumni: <Alumni student={student} />,
    office: <Office student={student} />,
    assistant: <Assistant student={student} />,
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
        <div className="sidebar-logo flex items-center gap-3" onClick={() => setCollapsed(c => !c)}>
          <SECELogo className="logo-mark w-7 h-7" onlyCrest={true} />
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
        <button className="sidebar-logout" onClick={() => setStudent(null)} title="Logout">
          <LogOut className="w-4 h-4" />{!collapsed && ' Logout'}
        </button>
      </aside>
      <main className="main-content">
        <header className="top-bar">
          <div className="top-bar-left flex items-center gap-3">
            <SECELogo className="w-9 h-9" light={true} onlyCrest={true} />
            <div className="flex flex-col">
              <span className="text-white font-extrabold text-lg leading-none tracking-tight">Smart Campus AI</span>
              <span className="text-white/80 text-[10px] uppercase font-bold tracking-wider mt-0.5">{pageTitle}</span>
            </div>
          </div>
          <div className="top-bar-right">
            <div className="top-bar-search">
              <Search className="w-4 h-4 search-icon text-white/80" />
              <input
                type="text"
                placeholder="Quick search..."
                className="search-input"
                value={searchQuery}
                onChange={handleSearchChange}
              />
            </div>
            <div className="top-bar-date">
              <Calendar className="w-4 h-4 text-white" />
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
            <button className="icon-btn header-logout text-white" onClick={() => setStudent(null)} title="Logout">
              <LogOut className="w-4 h-4" />
            </button>
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
