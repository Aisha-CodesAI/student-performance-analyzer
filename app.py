import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="🎓",
    layout="wide",
)

# ── Constants ──────────────────────────────────────────────────────────────────
REQUIRED_COLUMNS = ["Name", "Math", "Science", "English", "Computer"]
SUBJECTS = ["Math", "Science", "English", "Computer"]

# ── Helper functions ───────────────────────────────────────────────────────────

def assign_grade(avg: float) -> str:
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    elif avg >= 40:
        return "E"
    else:
        return "F"


def analyze(df: pd.DataFrame, passing_mark: int) -> pd.DataFrame:
    df = df.copy()
    df["Total"]      = df[SUBJECTS].sum(axis=1)
    df["Average"]    = df[SUBJECTS].mean(axis=1).round(2)
    df["Percentage"] = ((df["Total"] / (len(SUBJECTS) * 100)) * 100).round(2)
    df["Grade"]      = df["Average"].apply(assign_grade)
    df["Status"]     = df[SUBJECTS].min(axis=1).apply(
        lambda m: "Pass" if m >= passing_mark else "Fail"
    )
    df["Weakest Subject"] = df[SUBJECTS].idxmin(axis=1)
    return df


def validate(df: pd.DataFrame):
    """Return list of error strings (empty = valid)."""
    errors = []
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        errors.append(f"Missing columns: {', '.join(missing)}")
        return errors          # can't validate marks without columns

    for col in SUBJECTS:
        if not pd.api.types.is_numeric_dtype(df[col]):
            errors.append(f"Column '{col}' must contain numeric values.")
        else:
            out_of_range = df[(df[col] < 0) | (df[col] > 100)]
            if not out_of_range.empty:
                errors.append(
                    f"Column '{col}' has marks outside 0–100 "
                    f"(rows: {list(out_of_range.index + 2)})."
                )
    if df["Name"].isnull().any():
        errors.append("Some rows have empty student names.")
    return errors


def subject_bar_chart(series: pd.Series, student_name: str):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
    bars = ax.bar(series.index, series.values, color=colors, edgecolor="white", linewidth=0.8)
    ax.set_ylim(0, 110)
    ax.set_ylabel("Marks", fontsize=10)
    ax.set_title(f"{student_name} — Subject Marks", fontsize=11, fontweight="bold")
    ax.axhline(y=40, color="red", linestyle="--", linewidth=1, label="Pass line (40)")
    for bar, val in zip(bars, series.values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 2,
                str(int(val)), ha="center", va="bottom", fontsize=9)
    ax.legend(fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    return fig


def grade_distribution_chart(df: pd.DataFrame):
    grade_order = ["A+", "A", "B", "C", "D", "E", "F"]
    counts = df["Grade"].value_counts().reindex(grade_order, fill_value=0)
    colors = ["#2ecc71", "#27ae60", "#3498db", "#f39c12", "#e67e22", "#e74c3c", "#c0392b"]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(counts.index, counts.values, color=colors, edgecolor="white", linewidth=0.8)
    ax.set_xlabel("Grade", fontsize=10)
    ax.set_ylabel("Number of Students", fontsize=10)
    ax.set_title("Grade Distribution", fontsize=12, fontweight="bold")
    for bar, val in zip(bars, counts.values):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, val + 0.1,
                    str(val), ha="center", va="bottom", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.tight_layout()
    return fig


def subject_avg_chart(df: pd.DataFrame):
    avgs = df[SUBJECTS].mean().round(2)
    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(avgs.index, avgs.values, color=colors, edgecolor="white", linewidth=0.8)
    ax.set_ylim(0, 110)
    ax.set_ylabel("Average Marks", fontsize=10)
    ax.set_title("Subject-wise Class Average", fontsize=12, fontweight="bold")
    ax.axhline(y=40, color="red", linestyle="--", linewidth=1, label="Pass line (40)")
    for bar, val in zip(bars, avgs.values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1,
                f"{val:.1f}", ha="center", va="bottom", fontsize=9)
    ax.legend(fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    return fig


def pass_fail_pie(df: pd.DataFrame):
    counts = df["Status"].value_counts()
    colors = {"Pass": "#2ecc71", "Fail": "#e74c3c"}
    clrs   = [colors.get(s, "#aaa") for s in counts.index]
    fig, ax = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=clrs,
        startangle=90,
        wedgeprops=dict(edgecolor="white", linewidth=1.5),
    )
    for t in texts:
        t.set_fontsize(11)
    for at in autotexts:
        at.set_fontsize(10)
    ax.set_title("Pass / Fail Distribution", fontsize=12, fontweight="bold")
    plt.tight_layout()
    return fig


def performance_insights(df: pd.DataFrame, passing_mark: int) -> list[str]:
    insights = []
    class_avg = df["Average"].mean()
    weakest_subject = df[SUBJECTS].mean().idxmin()
    strongest_subject = df[SUBJECTS].mean().idxmax()
    pass_pct = (df["Status"] == "Pass").mean() * 100
    fail_pct = 100 - pass_pct

    if class_avg >= 75:
        insights.append(f"✅ Class performance is **excellent** — overall average is **{class_avg:.1f}**.")
    elif class_avg >= 60:
        insights.append(f"👍 Class performance is **good** — overall average is **{class_avg:.1f}**.")
    elif class_avg >= 50:
        insights.append(f"⚠️ Class performance is **average** — overall average is **{class_avg:.1f}**. There is room for improvement.")
    else:
        insights.append(f"🚨 Class performance **needs serious improvement** — overall average is only **{class_avg:.1f}**.")

    insights.append(f"📉 **Weakest subject** across the class: **{weakest_subject}** "
                    f"(avg {df[weakest_subject].mean():.1f}).")
    insights.append(f"📈 **Strongest subject** across the class: **{strongest_subject}** "
                    f"(avg {df[strongest_subject].mean():.1f}).")

    if fail_pct > 30:
        insights.append(f"⚠️ **{fail_pct:.1f}%** of students failed — targeted intervention is recommended.")
    else:
        insights.append(f"✅ Only **{fail_pct:.1f}%** of students failed — the class is performing well overall.")

    top_student = df.loc[df["Average"].idxmax(), "Name"]
    insights.append(f"🏆 Top performer: **{top_student}** with an average of **{df['Average'].max():.1f}**.")

    return insights


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🎓 Student Performance Analyzer")
    st.markdown("---")
    st.subheader("📂 Upload Data")
    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"],
        help="CSV must have columns: Name, Math, Science, English, Computer",
    )
    st.markdown("---")
    st.subheader("⚙️ Settings")
    passing_mark = st.slider(
        "Passing Mark",
        min_value=0,
        max_value=60,
        value=40,
        step=1,
        help="Minimum marks required in every subject to pass.",
    )
    st.markdown("---")
    st.caption("📋 **Expected CSV format:**")
    st.code("Name,Math,Science,English,Computer\nAlice,85,90,78,92", language="csv")

# ── Main content ───────────────────────────────────────────────────────────────
st.title("🎓 Student Performance Analyzer")
st.markdown("Upload a CSV file with student marks to get a full performance breakdown.")

if uploaded_file is None:
    st.info("👈 Upload a CSV file from the sidebar to get started. "
            "You can use the **sample_students.csv** included in the project.")
    st.stop()

# ── Load & validate ────────────────────────────────────────────────────────────
try:
    raw_df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"❌ Could not read the file: {e}")
    st.stop()

errors = validate(raw_df)
if errors:
    st.error("❌ **File validation failed:**")
    for err in errors:
        st.markdown(f"- {err}")
    st.stop()

df = analyze(raw_df, passing_mark)

# ── Summary metrics ────────────────────────────────────────────────────────────
st.markdown("## 📊 Class Summary")
total_students = len(df)
class_avg      = df["Average"].mean()
highest_avg    = df["Average"].max()
pass_count     = (df["Status"] == "Pass").sum()
fail_count     = (df["Status"] == "Fail").sum()
pass_pct       = (pass_count / total_students) * 100
fail_pct       = (fail_count / total_students) * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("👥 Total Students",  total_students)
col2.metric("📈 Class Average",   f"{class_avg:.1f}")
col3.metric("🏆 Highest Average", f"{highest_avg:.1f}")
col4.metric("✅ Pass Rate",       f"{pass_pct:.1f}%")
col5.metric("❌ Fail Rate",       f"{fail_pct:.1f}%")

st.markdown("---")

# ── Performance insights ───────────────────────────────────────────────────────
st.markdown("## 💡 Performance Insights")
for insight in performance_insights(df, passing_mark):
    st.markdown(insight)

st.markdown("---")

# ── Charts row ─────────────────────────────────────────────────────────────────
st.markdown("## 📉 Visual Analytics")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.pyplot(subject_avg_chart(df))

with chart_col2:
    st.pyplot(grade_distribution_chart(df))

chart_col3, chart_col4 = st.columns([1, 1])
with chart_col3:
    st.pyplot(pass_fail_pie(df))

st.markdown("---")

# ── Top 5 students ─────────────────────────────────────────────────────────────
st.markdown("## 🏆 Top 5 Students")
top5 = (
    df[["Name", "Total", "Average", "Percentage", "Grade", "Status"]]
    .sort_values("Average", ascending=False)
    .head(5)
    .reset_index(drop=True)
)
top5.index += 1
st.dataframe(top5, use_container_width=True)

st.markdown("---")

# ── Subject-wise averages ──────────────────────────────────────────────────────
st.markdown("## 📚 Subject-wise Class Averages")
subj_avg = df[SUBJECTS].mean().round(2).reset_index()
subj_avg.columns = ["Subject", "Average Marks"]
st.dataframe(subj_avg, use_container_width=True, hide_index=True)

st.markdown("---")

# ── Full analyzed table ────────────────────────────────────────────────────────
st.markdown("## 📋 Complete Student Results")
display_cols = ["Name"] + SUBJECTS + ["Total", "Average", "Percentage", "Grade", "Status"]

def style_status(val):
    if val == "Pass":
        return "color: green; font-weight: bold"
    elif val == "Fail":
        return "color: red; font-weight: bold"
    return ""

styled = df[display_cols].style.map(style_status, subset=["Status"])
st.dataframe(styled, use_container_width=True, hide_index=True)

st.markdown("---")

# ── Search student ─────────────────────────────────────────────────────────────
st.markdown("## 🔍 Search Student")
search_query = st.text_input("Enter student name to search:", placeholder="e.g. Alice")
if search_query.strip():
    results = df[df["Name"].str.contains(search_query.strip(), case=False, na=False)]
    if results.empty:
        st.warning(f"No student found matching **'{search_query}'**.")
    else:
        st.success(f"Found **{len(results)}** result(s):")
        st.dataframe(results[display_cols].reset_index(drop=True), use_container_width=True, hide_index=True)

st.markdown("---")

# ── Individual student profile ─────────────────────────────────────────────────
st.markdown("## 👤 Student Profile")
student_names = df["Name"].tolist()
selected_name = st.selectbox("Select a student:", ["— Select a student —"] + student_names)

if selected_name != "— Select a student —":
    row = df[df["Name"] == selected_name].iloc[0]

    p1, p2, p3, p4, p5 = st.columns(5)
    p1.metric("📊 Average",    f"{row['Average']:.1f}")
    p2.metric("📝 Total",      int(row["Total"]))
    p3.metric("📈 Percentage", f"{row['Percentage']:.1f}%")
    p4.metric("🎖️ Grade",      row["Grade"])
    p5.metric("✅ Status",     row["Status"])

    st.markdown(f"**📉 Weakest Subject:** {row['Weakest Subject']} "
                f"({int(row[row['Weakest Subject']])} marks)")

    st.pyplot(subject_bar_chart(row[SUBJECTS], selected_name))

st.markdown("---")

# ── Download button ────────────────────────────────────────────────────────────
st.markdown("## 💾 Download Results")
download_cols = ["Name"] + SUBJECTS + ["Total", "Average", "Percentage", "Grade", "Status", "Weakest Subject"]
csv_buffer = io.StringIO()
df[download_cols].to_csv(csv_buffer, index=False)
st.download_button(
    label="⬇️ Download Analyzed Results as CSV",
    data=csv_buffer.getvalue(),
    file_name="student_results_analyzed.csv",
    mime="text/csv",
)

st.markdown("---")
st.caption("🎓 Student Performance Analyzer — built with Streamlit, Pandas & Matplotlib.")
