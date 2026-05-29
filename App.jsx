import { useState } from "react";
import { DATA } from "./data";
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, RadarChart, Radar, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis
} from "recharts";
import {
  BarChart2, TrendingUp, AlertTriangle, Activity,
  MessageSquare, Star, Info, ChevronDown, ChevronUp,
  Award, Scale, BookOpen, Users
} from "lucide-react";

// ─── COLOURS ──────────────────────────────────────────────────────────────────
const C = {
  pos: "#16a34a",
  neu: "#d97706",
  neg: "#dc2626",
  posLight: "#dcfce7",
  neuLight: "#fef9c3",
  negLight: "#fee2e2",
  bg: "#f8fafc",
  card: "#ffffff",
  border: "#e2e8f0",
  text: "#1e293b",
  textMuted: "#64748b",
  green: "#0C3D2E",
};

// ─── HELPERS ──────────────────────────────────────────────────────────────────
const pct = (v, total) => ((v / total) * 100).toFixed(1);
const fmt = (n) => n.toLocaleString("id-ID");

// ─── SUB-COMPONENTS ───────────────────────────────────────────────────────────
function Badge({ children, color = "#e2e8f0", text = C.textMuted }) {
  return (
    <span style={{
      background: color, color: text, fontSize: 11, fontWeight: 600,
      padding: "2px 10px", borderRadius: 20, letterSpacing: "0.4px"
    }}>{children}</span>
  );
}

function Card({ children, style = {} }) {
  return (
    <div style={{
      background: C.card, border: `1px solid ${C.border}`,
      borderRadius: 12, padding: "20px 22px",
      boxShadow: "0 1px 3px rgba(0,0,0,0.06)", ...style
    }}>{children}</div>
  );
}

function SectionTitle({ icon: Icon, children }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8, margin: "28px 0 14px" }}>
      <Icon size={16} color={C.green} />
      <span style={{ fontSize: 11, fontWeight: 700, color: C.textMuted, textTransform: "uppercase", letterSpacing: "0.8px" }}>
        {children}
      </span>
      <div style={{ flex: 1, height: 1, background: C.border }} />
    </div>
  );
}

function KPICard({ label, value, sub, color = C.text, bgColor }) {
  return (
    <div style={{
      background: bgColor || "#f8fafc", borderRadius: 10, padding: "14px 16px",
      border: `1px solid ${C.border}`
    }}>
      <div style={{ fontSize: 12, color: C.textMuted, marginBottom: 4 }}>{label}</div>
      <div style={{ fontSize: 26, fontWeight: 700, color, lineHeight: 1 }}>{value}</div>
      {sub && <div style={{ fontSize: 11, color: C.textMuted, marginTop: 4 }}>{sub}</div>}
    </div>
  );
}

function TabBar({ tabs, active, onChange }) {
  return (
    <div style={{ display: "flex", gap: 6, marginBottom: 16, flexWrap: "wrap" }}>
      {tabs.map((t) => (
        <button
          key={t.value}
          onClick={() => onChange(t.value)}
          style={{
            fontSize: 12, padding: "5px 14px", borderRadius: 20, cursor: "pointer",
            border: `1px solid ${active === t.value ? C.green : C.border}`,
            background: active === t.value ? C.green : "transparent",
            color: active === t.value ? "#fff" : C.textMuted,
            fontWeight: active === t.value ? 600 : 400, transition: "all .15s"
          }}
        >{t.label}</button>
      ))}
    </div>
  );
}

function ConfusionMatrix({ matrix, accuracy, macroF1, perClass, title }) {
  const labels = ["Negatif", "Netral", "Positif"];
  const colorsMap = { Negatif: C.neg, Netral: C.neu, Positif: C.pos };
  return (
    <Card>
      <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 4 }}>{title}</div>
      <div style={{ display: "flex", gap: 12, marginBottom: 14, flexWrap: "wrap" }}>
        <Badge color={C.posLight} text={C.pos}>Akurasi: {(accuracy * 100).toFixed(1)}%</Badge>
        <Badge color="#dbeafe" text="#1d4ed8">Macro F1: {macroF1.toFixed(4)}</Badge>
      </div>
      {/* Matrix */}
      <div style={{ overflowX: "auto" }}>
        <table style={{ borderCollapse: "separate", borderSpacing: 3, fontSize: 12, marginBottom: 14 }}>
          <thead>
            <tr>
              <th style={{ padding: "6px 10px", color: C.textMuted, fontWeight: 500 }}>Aktual ↓ / Pred →</th>
              {labels.map((l) => (
                <th key={l} style={{ padding: "6px 10px", textAlign: "center", color: colorsMap[l], fontWeight: 600 }}>
                  {l}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.map((row, i) => (
              <tr key={i}>
                <td style={{ padding: "6px 10px", fontWeight: 600, color: colorsMap[labels[i]], textAlign: "right" }}>
                  {labels[i]}
                </td>
                {row.map((val, j) => (
                  <td key={j} style={{
                    padding: "8px 14px", textAlign: "center", borderRadius: 6, fontWeight: 600,
                    background: i === j ? (i === 0 ? "#fee2e2" : i === 1 ? "#fef9c3" : "#dcfce7")
                      : "#f1f5f9",
                    color: i === j ? (i === 0 ? C.neg : i === 1 ? C.neu : C.pos) : C.textMuted
                  }}>{val}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Per-class metrics */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 8 }}>
        {labels.map((l) => (
          <div key={l} style={{
            background: "#f8fafc", borderRadius: 8, padding: "10px 12px",
            borderLeft: `3px solid ${colorsMap[l]}`
          }}>
            <div style={{ fontSize: 11, fontWeight: 700, color: colorsMap[l], marginBottom: 6 }}>{l}</div>
            {["precision", "recall", "f1"].map((m) => (
              <div key={m} style={{ display: "flex", justifyContent: "space-between", fontSize: 11, marginBottom: 2 }}>
                <span style={{ color: C.textMuted, textTransform: "capitalize" }}>{m}</span>
                <span style={{ fontWeight: 600, color: C.text }}>{(perClass[l][m] * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        ))}
      </div>
    </Card>
  );
}

function SampleReviews({ data }) {
  const [active, setActive] = useState("Positif");
  const [expanded, setExpanded] = useState(null);
  const colorMap = { Positif: C.pos, Negatif: C.neg, Netral: C.neu };
  const bgMap = { Positif: C.posLight, Negatif: C.negLight, Netral: C.neuLight };
  return (
    <Card>
      <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 14 }}>Contoh Ulasan per Sentimen</div>
      <TabBar
        tabs={["Positif", "Netral", "Negatif"].map((v) => ({ value: v, label: v }))}
        active={active}
        onChange={(v) => { setActive(v); setExpanded(null); }}
      />
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {(data[active] || []).map((r, i) => (
          <div key={i} style={{
            borderRadius: 8, border: `1px solid ${C.border}`,
            overflow: "hidden", cursor: "pointer",
          }} onClick={() => setExpanded(expanded === i ? null : i)}>
            <div style={{
              padding: "10px 14px", display: "flex", alignItems: "center",
              gap: 10, background: expanded === i ? bgMap[active] : "#fff"
            }}>
              <span style={{ fontSize: 13, color: "#f59e0b" }}>{"⭐".repeat(r.stars)}</span>
              <span style={{ fontSize: 11, color: C.textMuted }}>{r.date}</span>
              <span style={{ flex: 1, fontSize: 12, color: C.text, overflow: "hidden",
                textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{r.text}</span>
              {expanded === i ? <ChevronUp size={14} color={C.textMuted} /> : <ChevronDown size={14} color={C.textMuted} />}
            </div>
            {expanded === i && (
              <div style={{ padding: "12px 14px", borderTop: `1px solid ${C.border}`,
                fontSize: 13, color: C.text, lineHeight: 1.6, background: bgMap[active] + "88" }}>
                {r.text}
              </div>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
}

// ─── MAIN APP ─────────────────────────────────────────────────────────────────
export default function App() {
  const [trendMode, setTrendMode] = useState("orig");
  const [wordClass, setWordClass] = useState("Positif");

  const totalSentimen = DATA.distribution.sentiment.Positif
    + DATA.distribution.sentiment.Netral
    + DATA.distribution.sentiment.Negatif;

  // Build yearly stacked data
  const yearlyData = DATA.yearly.years.map((yr, i) => {
    const src = trendMode === "orig" ? DATA.yearly.sentiment_orig : DATA.yearly.sentiment_weighted;
    return {
      year: yr, Positif: src.Positif[i],
      Netral: src.Netral[i], Negatif: src.Negatif[i],
      count: DATA.yearly.count[i], avgRating: DATA.yearly.avg_rating[i]
    };
  });

  // Monthly 2024
  const monthly2024 = DATA.monthly_2024.months.map((m, i) => ({
    name: DATA.monthly_2024.month_names[i],
    Positif: DATA.monthly_2024.Positif[i],
    Netral: DATA.monthly_2024.Netral[i],
    Negatif: DATA.monthly_2024.Negatif[i]
  }));

  // Donut
  const donutData = [
    { name: "Positif", value: DATA.distribution.sentiment.Positif, color: C.pos },
    { name: "Netral",  value: DATA.distribution.sentiment.Netral,  color: C.neu },
    { name: "Negatif", value: DATA.distribution.sentiment.Negatif, color: C.neg }
  ];

  // Radar comparison
  const radarData = ["Negatif", "Netral", "Positif"].map((cls) => ({
    class: cls,
    "Recall (tanpa bobot)": +(DATA.model_no_weight.per_class[cls].recall * 100).toFixed(1),
    "Recall (berbobot)": +(DATA.model_weighted.per_class[cls].recall * 100).toFixed(1),
  }));

  // Neg themes
  const themesData = Object.entries(DATA.neg_themes)
    .sort((a, b) => b[1] - a[1])
    .map(([name, value]) => ({ name, value }));
  const maxTheme = Math.max(...themesData.map((t) => t.value));

  // Weight visual
  const weightData = [
    { class: "Negatif", bobot: DATA.model_weighted.weights.Negatif, color: C.neg },
    { class: "Netral",  bobot: DATA.model_weighted.weights.Netral,  color: C.neu },
    { class: "Positif", bobot: DATA.model_weighted.weights.Positif, color: C.pos }
  ];

  // Top words
  const wordData = (DATA.top_words[wordClass] || []).slice(0, 12);
  const maxWord = Math.max(...wordData.map((w) => w.count));

  const colorMap = { Positif: C.pos, Negatif: C.neg, Netral: C.neu };

  return (
    <div style={{ background: C.bg, minHeight: "100vh", fontFamily: "'Inter','Segoe UI',sans-serif", color: C.text }}>
      <div style={{ maxWidth: 960, margin: "0 auto", padding: "24px 16px 48px" }}>

        {/* ── HEADER ── */}
        <div style={{
          background: C.green, borderRadius: 16, padding: "28px 32px",
          marginBottom: 24, position: "relative", overflow: "hidden"
        }}>
          <div style={{
            position: "absolute", right: -40, top: -40, width: 200, height: 200,
            borderRadius: "50%", background: "rgba(255,255,255,0.04)"
          }} />
          <div style={{
            position: "absolute", right: 60, bottom: -50, width: 140, height: 140,
            borderRadius: "50%", background: "rgba(255,255,255,0.03)"
          }} />
          <Badge color="rgba(255,255,255,0.15)" text="#9FE1CB">
            Laporan Analisis Sentimen · Google Maps
          </Badge>
          <h1 style={{ color: "#fff", fontSize: 22, fontWeight: 600, margin: "10px 0 4px", lineHeight: 1.3 }}>
            Analisis Sentimen Ulasan Wisata<br />D'Las Lembah Asri Serang, Purbalingga
          </h1>
          <p style={{ color: "rgba(255,255,255,0.55)", fontSize: 13, margin: "0 0 20px" }}>
            Metode Complement Naive Bayes + TF-IDF + Class Weight Balancing
          </p>
          <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
            {[
              ["Total Ulasan", fmt(DATA.meta.total_data)],
              ["Periode", DATA.meta.period],
              ["Model", "Complement NB"],
              ["Split", "80% Train / 20% Test"],
              ["Fitur", "TF-IDF 5.000"]
            ].map(([l, v]) => (
              <div key={l}>
                <div style={{ fontSize: 11, color: "rgba(255,255,255,0.5)" }}>{l}</div>
                <div style={{ fontSize: 13, color: "#9FE1CB", fontWeight: 600 }}>{v}</div>
              </div>
            ))}
          </div>
        </div>

        {/* ── KPI GRID ── */}
        <SectionTitle icon={BarChart2}>Ringkasan Data</SectionTitle>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(130px,1fr))", gap: 10 }}>
          <KPICard label="Total Ulasan" value={fmt(totalSentimen)} sub="Setelah filter & preprocessing" />
          <KPICard label="Positif (⭐4–5)" value={fmt(DATA.distribution.sentiment.Positif)}
            sub={pct(DATA.distribution.sentiment.Positif, totalSentimen) + "% dari total"}
            color={C.pos} bgColor={C.posLight} />
          <KPICard label="Netral (⭐3)" value={fmt(DATA.distribution.sentiment.Netral)}
            sub={pct(DATA.distribution.sentiment.Netral, totalSentimen) + "% dari total"}
            color={C.neu} bgColor={C.neuLight} />
          <KPICard label="Negatif (⭐1–2)" value={fmt(DATA.distribution.sentiment.Negatif)}
            sub={pct(DATA.distribution.sentiment.Negatif, totalSentimen) + "% dari total"}
            color={C.neg} bgColor={C.negLight} />
          <KPICard label="Rata-rata Rating" value="4,31" sub="Skala 1–5" />
          <KPICard label="Akurasi (tanpa bobot)" value="85,9%" sub="Complement NB" />
          <KPICard label="Akurasi (berbobot)" value="81,5%" sub="Recall minority ↑" color="#1d4ed8" />
        </div>

        {/* ── DISTRIBUSI ── */}
        <SectionTitle icon={Star}>Distribusi Bintang & Sentimen</SectionTitle>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>

          {/* Donut */}
          <Card>
            <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>Distribusi Sentimen</div>
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie data={donutData} cx="50%" cy="50%" innerRadius={55} outerRadius={85}
                  paddingAngle={3} dataKey="value">
                  {donutData.map((d, i) => <Cell key={i} fill={d.color} />)}
                </Pie>
                <Tooltip formatter={(v, n) => [fmt(v) + " ulasan", n]} />
              </PieChart>
            </ResponsiveContainer>
            <div style={{ display: "flex", justifyContent: "center", gap: 16 }}>
              {donutData.map((d) => (
                <div key={d.name} style={{ display: "flex", alignItems: "center", gap: 5, fontSize: 12 }}>
                  <span style={{ width: 10, height: 10, borderRadius: 2, background: d.color, display: "inline-block" }} />
                  <span style={{ color: C.textMuted }}>{d.name} {pct(d.value, totalSentimen)}%</span>
                </div>
              ))}
            </div>
          </Card>

          {/* Stars bar */}
          <Card>
            <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 14 }}>Sebaran Bintang</div>
            {[5, 4, 3, 2, 1].map((s) => {
              const v = DATA.distribution.stars[String(s)];
              const starsColors = { 5: C.pos, 4: "#22c55e", 3: C.neu, 2: "#f97316", 1: C.neg };
              return (
                <div key={s} style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
                  <span style={{ fontSize: 12, color: C.textMuted, width: 38 }}>⭐ {s}</span>
                  <div style={{ flex: 1, background: "#f1f5f9", borderRadius: 4, height: 18 }}>
                    <div style={{
                      width: pct(v, totalSentimen) + "%", height: "100%",
                      background: starsColors[s], borderRadius: 4,
                      transition: "width .5s ease"
                    }} />
                  </div>
                  <span style={{ fontSize: 11, color: C.textMuted, width: 70, textAlign: "right" }}>
                    {fmt(v)} ({pct(v, totalSentimen)}%)
                  </span>
                </div>
              );
            })}
            <div style={{
              marginTop: 10, fontSize: 12, color: "#7c3aed",
              padding: "8px 12px", background: "#ede9fe", borderRadius: 8
            }}>
              ⚠️ Data sangat imbalanced — Positif 83% vs Negatif 4,8%. Class weight wajib digunakan.
            </div>
          </Card>
        </div>

        {/* ── TREN TAHUNAN ── */}
        <SectionTitle icon={TrendingUp}>Tren & Pola Per Tahun</SectionTitle>
        <Card>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 14 }}>
            Jumlah Ulasan per Sentimen per Tahun
          </div>
          <TabBar
            tabs={[
              { value: "orig", label: "Label Asli (Bintang)" },
              { value: "weighted", label: "Prediksi Model Berbobot" }
            ]}
            active={trendMode}
            onChange={setTrendMode}
          />
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={yearlyData} margin={{ top: 0, right: 0, bottom: 0, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="year" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip
                formatter={(v, n) => [fmt(v), n]}
                contentStyle={{ fontSize: 12, borderRadius: 8 }}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="Positif" stackId="a" fill={C.pos} />
              <Bar dataKey="Netral" stackId="a" fill={C.neu} />
              <Bar dataKey="Negatif" stackId="a" fill={C.neg} radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <div style={{
            marginTop: 12, fontSize: 12, color: C.textMuted, padding: "8px 12px",
            background: "#f8fafc", borderRadius: 8, lineHeight: 1.6
          }}>
            <strong style={{ color: C.text }}>Catatan perbedaan:</strong> Model berbobot mendeteksi lebih banyak ulasan Negatif & Netral
            yang sebelumnya salah diklasifikasi sebagai Positif akibat dominasi kelas mayoritas.
          </div>
        </Card>

        {/* Rating trend */}
        <Card style={{ marginTop: 14 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 14 }}>
            Rata-rata Rating & Volume Ulasan per Tahun
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={yearlyData} margin={{ top: 0, right: 20, bottom: 0, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="year" tick={{ fontSize: 11 }} />
              <YAxis yAxisId="rating" domain={[3.4, 4.7]} tick={{ fontSize: 11 }} />
              <YAxis yAxisId="count" orientation="right" tick={{ fontSize: 11 }} />
              <Tooltip contentStyle={{ fontSize: 12, borderRadius: 8 }}
                formatter={(v, n) => n === "avgRating" ? [v.toFixed(2), "Avg Rating"] : [fmt(v), "Jumlah Ulasan"]} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Line yAxisId="rating" type="monotone" dataKey="avgRating"
                stroke={C.green} strokeWidth={2.5} dot={{ r: 4, fill: C.green }}
                name="Avg Rating" />
              <Bar yAxisId="count" dataKey="count" fill="#e2e8f0" radius={[3, 3, 0, 0]} name="Jumlah Ulasan" />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Monthly 2024 */}
        <Card style={{ marginTop: 14 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 6 }}>Tren Bulanan 2024</div>
          <div style={{ fontSize: 12, color: C.textMuted, marginBottom: 14 }}>
            Catatan: Oktober 2024 ada lonjakan negatif (14 ulasan) — ada keluhan wahana berbayar lagi & animal abuse.
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={monthly2024} margin={{ top: 0, right: 0, bottom: 0, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip contentStyle={{ fontSize: 12, borderRadius: 8 }} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="Positif" stackId="a" fill={C.pos} />
              <Bar dataKey="Netral" stackId="a" fill={C.neu} />
              <Bar dataKey="Negatif" stackId="a" fill={C.neg} radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* ── KLASIFIKASI NB ── */}
        <SectionTitle icon={Activity}>Klasifikasi Naive Bayes — Perbandingan Model</SectionTitle>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          <ConfusionMatrix
            title="Tanpa Pembobotan"
            matrix={DATA.model_no_weight.confusion_matrix}
            accuracy={DATA.model_no_weight.accuracy}
            macroF1={DATA.model_no_weight.macro_f1}
            perClass={DATA.model_no_weight.per_class}
          />
          <ConfusionMatrix
            title="Dengan Pembobotan Seimbang"
            matrix={DATA.model_weighted.confusion_matrix}
            accuracy={DATA.model_weighted.accuracy}
            macroF1={DATA.model_weighted.macro_f1}
            perClass={DATA.model_weighted.per_class}
          />
        </div>

        {/* Radar comparison */}
        <Card style={{ marginTop: 14 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 14 }}>
            Perbandingan Recall per Kelas — Sebelum vs Sesudah Bobot
          </div>
          <ResponsiveContainer width="100%" height={240}>
            <RadarChart data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="class" tick={{ fontSize: 12 }} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 10 }} />
              <Radar name="Recall (tanpa bobot)" dataKey="Recall (tanpa bobot)"
                stroke="#94a3b8" fill="#94a3b8" fillOpacity={0.3} />
              <Radar name="Recall (berbobot)" dataKey="Recall (berbobot)"
                stroke={C.green} fill={C.green} fillOpacity={0.3} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Tooltip contentStyle={{ fontSize: 12, borderRadius: 8 }}
                formatter={(v) => [v + "%"]} />
            </RadarChart>
          </ResponsiveContainer>
        </Card>

        {/* ── CLASS WEIGHT ── */}
        <SectionTitle icon={Scale}>Pembobotan Kelas (Class Weight Balancing)</SectionTitle>
        <Card>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 8 }}>Bobot per Kelas — Balanced Strategy</div>
          <div style={{ fontSize: 12, color: C.textMuted, marginBottom: 16, lineHeight: 1.6 }}>
            Formula: <code style={{
              fontFamily: "monospace", fontSize: 11,
              background: "#f1f5f9", padding: "2px 8px", borderRadius: 4
            }}>n_samples / (n_classes × count_class)</code>
            {" "}— Kelas minoritas diberi bobot lebih tinggi agar model tidak bias ke mayoritas.
          </div>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginBottom: 20 }}>
            {weightData.map((w) => (
              <div key={w.class} style={{
                display: "flex", alignItems: "center", gap: 8,
                padding: "8px 16px", borderRadius: 20, fontWeight: 600, fontSize: 13,
                background: w.class === "Negatif" ? C.negLight : w.class === "Netral" ? C.neuLight : C.posLight,
                color: w.color
              }}>
                {w.class}: ×{w.bobot.toFixed(4)}
              </div>
            ))}
          </div>
          <ResponsiveContainer width="100%" height={120}>
            <BarChart data={weightData} layout="vertical" margin={{ top: 0, right: 20, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis type="number" tick={{ fontSize: 11 }} tickFormatter={(v) => "×" + v.toFixed(1)} />
              <YAxis type="category" dataKey="class" tick={{ fontSize: 12 }} width={60} />
              <Tooltip formatter={(v) => ["×" + v.toFixed(4), "Bobot"]}
                contentStyle={{ fontSize: 12, borderRadius: 8 }} />
              <Bar dataKey="bobot" radius={[0, 6, 6, 0]}>
                {weightData.map((w, i) => <Cell key={i} fill={w.color} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div style={{
            marginTop: 14, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, fontSize: 12
          }}>
            <div style={{ background: C.negLight, borderRadius: 8, padding: "10px 14px" }}>
              <strong style={{ color: C.neg }}>Recall Negatif:</strong>
              <span style={{ color: C.textMuted }}> 52,9% → </span>
              <strong style={{ color: C.pos }}>82,4% ↑</strong>
              <div style={{ color: C.textMuted, marginTop: 2 }}>Ulasan negatif jauh lebih terdeteksi</div>
            </div>
            <div style={{ background: C.neuLight, borderRadius: 8, padding: "10px 14px" }}>
              <strong style={{ color: C.neu }}>Recall Netral:</strong>
              <span style={{ color: C.textMuted }}> 53,5% → </span>
              <strong style={{ color: C.pos }}>75,6% ↑</strong>
              <div style={{ color: C.textMuted, marginTop: 2 }}>Ulasan netral lebih teridentifikasi</div>
            </div>
          </div>
        </Card>

        {/* ── PENYEBAB NEGATIF ── */}
        <SectionTitle icon={AlertTriangle}>Analisis Penyebab Rating Rendah</SectionTitle>
        <Card>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 14 }}>
            Tema Keluhan Utama pada Ulasan Bintang 1–2
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {themesData.map((t, i) => (
              <div key={t.name} style={{ display: "flex", alignItems: "center", gap: 12 }}>
                <div style={{ width: 170, fontSize: 12, color: C.textMuted, textAlign: "right", flexShrink: 0 }}>
                  {t.name}
                </div>
                <div style={{ flex: 1, background: "#f1f5f9", borderRadius: 4, height: 20 }}>
                  <div style={{
                    width: (t.value / maxTheme * 100) + "%", height: "100%", borderRadius: 4,
                    background: i === 0 ? C.neg : i < 3 ? "#f97316" : C.neu,
                    transition: "width .5s ease"
                  }} />
                </div>
                <span style={{ fontSize: 12, fontWeight: 600, color: C.text, width: 24 }}>{t.value}</span>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 16, display: "flex", flexDirection: "column", gap: 8 }}>
            {[
              { icon: "💸", title: "Wahana Berbayar Lagi", desc: "Wisatawan merasa tiket masuk seharusnya sudah include semua wahana. Ini keluhan terbanyak." },
              { icon: "😠", title: "Pelayanan Buruk", desc: "Karyawan kurang ramah, petugas foto yang memaksa membeli, dan layanan yang tidak memuaskan." },
              { icon: "🐾", title: "Animal Abuse", desc: "Burung dirantai kakinya di kebun binatang mini — memicu ulasan bintang 1 yang kuat." }
            ].map((item) => (
              <div key={item.title} style={{
                display: "flex", gap: 10, padding: "10px 14px",
                background: "#f8fafc", borderRadius: 8, fontSize: 12
              }}>
                <span style={{ fontSize: 18 }}>{item.icon}</span>
                <div>
                  <strong style={{ color: C.text }}>{item.title}</strong>
                  <div style={{ color: C.textMuted, marginTop: 2 }}>{item.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* ── TOP KEYWORDS ── */}
        <SectionTitle icon={MessageSquare}>Kata Kunci Dominan per Sentimen</SectionTitle>
        <Card>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 14 }}>Top Kata per Kelas Sentimen</div>
          <TabBar
            tabs={["Positif", "Netral", "Negatif"].map((v) => ({ value: v, label: v }))}
            active={wordClass}
            onChange={setWordClass}
          />
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {wordData.map((w) => (
              <div key={w.word} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{ fontSize: 12, color: C.textMuted, width: 90, textAlign: "right" }}>{w.word}</span>
                <div style={{ flex: 1, background: "#f1f5f9", borderRadius: 4, height: 18 }}>
                  <div style={{
                    width: (w.count / maxWord * 100) + "%", height: "100%",
                    background: colorMap[wordClass] + "cc", borderRadius: 4
                  }} />
                </div>
                <span style={{ fontSize: 11, color: C.textMuted, width: 50 }}>{fmt(w.count)}</span>
              </div>
            ))}
          </div>
        </Card>

        {/* ── SAMPLE REVIEWS ── */}
        <SectionTitle icon={Users}>Contoh Ulasan</SectionTitle>
        <SampleReviews data={DATA.samples} />

        {/* ── METHODOLOGY ── */}
        <SectionTitle icon={BookOpen}>Metodologi & Pipeline</SectionTitle>
        <Card>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
            <div>
              <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 10 }}>Pipeline Preprocessing</div>
              {[
                "Lowercase & hapus karakter non-huruf",
                "Stopword removal (Bahasa Indonesia)",
                "Filter token pendek (< 3 karakter)",
                "TF-IDF Vectorizer — Unigram + Bigram",
                "Max features: 5.000",
                "Labeling: ⭐1-2 Negatif, ⭐3 Netral, ⭐4-5 Positif"
              ].map((s) => (
                <div key={s} style={{ display: "flex", gap: 8, marginBottom: 6, fontSize: 12, color: C.textMuted }}>
                  <span style={{ color: C.pos, flexShrink: 0 }}>✓</span> {s}
                </div>
              ))}
            </div>
            <div>
              <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 10 }}>Parameter Model</div>
              {[
                "Algoritma: Complement Naive Bayes",
                "Split: 80% train / 20% test",
                "Stratified sampling (menjaga proporsi kelas)",
                "Class weight: balanced (via sample_weight)",
                "Bobot Negatif: ×6.92 | Netral: ×2.77 | Positif: ×0.40",
                "Evaluasi: Accuracy, Precision, Recall, F1-Score"
              ].map((s) => (
                <div key={s} style={{ display: "flex", gap: 8, marginBottom: 6, fontSize: 12, color: C.textMuted }}>
                  <span style={{ color: "#3b82f6", flexShrink: 0 }}>✓</span> {s}
                </div>
              ))}
            </div>
          </div>
          {/* Imbalance warning explanation */}
          <div style={{
            marginTop: 16, padding: "14px 16px", background: "#fef3c7",
            borderRadius: 10, borderLeft: "4px solid #f59e0b", fontSize: 12, lineHeight: 1.7
          }}>
            <strong>Kenapa akurasi turun setelah pembobotan?</strong>
            <br />
            Tanpa bobot: akurasi 85,9% tapi recall Negatif hanya 52,9% — model "malas" mendeteksi minoritas.
            Dengan bobot: akurasi turun ke 81,5% tapi recall Negatif naik ke 82,4% dan Netral ke 75,6%.
            Untuk kasus imbalanced, <strong>Macro F1 lebih penting</strong> daripada akurasi keseluruhan —
            dan Macro F1 justru naik dari 0,6496 → 0,6612.
          </div>
        </Card>

        {/* ── INSIGHT ── */}
        <SectionTitle icon={Award}>Temuan & Rekomendasi</SectionTitle>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {[
            { icon: "📈", title: "Rating Meningkat Konsisten", desc: "Dari 3,74 (2017) → 4,45 (2024). Pengelola berhasil memperbaiki kualitas wisata secara bertahap, terutama signifikan sejak 2021." },
            { icon: "💰", title: "Keluhan Utama: Wahana Berbayar Lagi", desc: "Penyebab utama rating 1-2. Wisatawan merasa tidak fair harus bayar lagi per wahana setelah bayar tiket masuk." },
            { icon: "📅", title: "Lonjakan Negatif Oktober 2024", desc: "14 ulasan negatif di Oktober 2024 — perlu investigasi: mungkin ada perubahan kebijakan tiket atau kejadian khusus." },
            { icon: "⚖️", title: "Pembobotan Efektif untuk Data Imbalanced", desc: "Class weight balanced meningkatkan recall Negatif dari 52,9% → 82,4%. Ini penting agar sistem bisa mendeteksi keluhan yang sebenarnya." },
            { icon: "🐾", title: "Isu Animal Welfare Perlu Ditangani", desc: "Meskipun jumlah kecil (5 ulasan), keluhan animal abuse menghasilkan bintang 1 yang kuat dan berdampak pada citra wisata." }
          ].map((item) => (
            <div key={item.title} style={{
              display: "flex", gap: 12, padding: "12px 16px",
              background: C.card, border: `1px solid ${C.border}`,
              borderRadius: 10, boxShadow: "0 1px 3px rgba(0,0,0,0.04)"
            }}>
              <span style={{ fontSize: 20, flexShrink: 0 }}>{item.icon}</span>
              <div>
                <div style={{ fontSize: 13, fontWeight: 600, color: C.text }}>{item.title}</div>
                <div style={{ fontSize: 12, color: C.textMuted, marginTop: 3, lineHeight: 1.6 }}>{item.desc}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div style={{ marginTop: 40, textAlign: "center", fontSize: 11, color: C.textMuted }}>
          Analisis Sentimen D'Las Lembah Asri Serang Purbalingga · Data Google Maps · Complement Naive Bayes
        </div>
      </div>
    </div>
  );
}
